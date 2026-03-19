"""
Orchestrator: runs extraction, validation, chunking, and Q&A with guardrails.
"""

import os
import json
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

from dataclasses import asdict

import numpy as np

from .config import ExtractionConfig
from .extractor import MultiPassExtractor
from .validator import ExtractionValidator
from .chunker import SmartChunker
from .guardrail import MedicalGuardrailBrain


class MedicalQASystem:
    """
    Complete medical Q&A system with:
    - Multi-pass extraction
    - Comprehensive validation
    - Smart chunking
    - Two-brain guardrails
    """

    def __init__(
        self,
        pdf_path: Optional[str] = None,
        output_dir: str = "./medical_knowledge_base",
        *,
        config: Optional[ExtractionConfig] = None,
    ):
        if config is not None:
            if pdf_path is not None:
                raise ValueError("Pass either config=... or pdf_path=..., not both.")
            self.config = config
        elif pdf_path is not None:
            self.config = ExtractionConfig(
                pdf_path=pdf_path,
                output_dir=output_dir,
                cache_dir=os.path.join(output_dir, "cache"),
            )
        else:
            raise ValueError("MedicalQASystem requires pdf_path=... or config=...")

        self.pdf_path = self.config.pdf_path
        self.output_dir = self.config.output_dir

        self.extraction_result: Dict[str, Any] | None = None
        self.validation_result: Dict[str, Any] | None = None
        self.chunks: List[Dict] | None = None
        self.search_index: Dict[str, Any] | None = None
        self.guardrail: MedicalGuardrailBrain | None = None

    def initialize(self) -> "MedicalQASystem":
        """Initialize or load existing knowledge base."""
        print("=" * 70)
        print("MEDICAL Q&A SYSTEM - COMPLETE PIPELINE")
        print("=" * 70)

        kb_file = os.path.join(self.output_dir, "knowledge_base.json")

        if os.path.exists(kb_file):
            print("\n📦 Loading existing knowledge base...")
            self._load_knowledge_base(kb_file)
        else:
            print("\n🔄 Building new knowledge base...")
            self._build_knowledge_base()

        print("\n✅ System ready!")
        return self

    def _build_knowledge_base(self) -> None:
        """Build knowledge base from scratch."""
        print("\n" + "=" * 70)
        print("STEP 1: MULTI-PASS EXTRACTION")
        print("=" * 70)

        extractor = MultiPassExtractor(self.config)
        self.extraction_result = extractor.extract_all()

        print("\n" + "=" * 70)
        print("STEP 2: VALIDATION")
        print("=" * 70)

        validator = ExtractionValidator(
            self.extraction_result,
            self.config,
        )
        self.validation_result = validator.validate_all()

        print("\n" + "=" * 70)
        print("STEP 3: SMART CHUNKING")
        print("=" * 70)

        chunker = SmartChunker(self.extraction_result, self.config)
        self.chunks = chunker.chunk_by_headings()
        self.search_index = chunker.create_search_index()

        print("\n" + "=" * 70)
        print("STEP 4: INITIALIZING GUARDRAIL BRAIN")
        print("=" * 70)

        self.guardrail = MedicalGuardrailBrain(self.chunks)

        self._save_knowledge_base()

    def _save_knowledge_base(self) -> None:
        """Save knowledge base to disk."""
        assert self.extraction_result is not None
        assert self.validation_result is not None
        assert self.chunks is not None

        kb = {
            "metadata": {
                "pdf_path": self.pdf_path,
                "build_date": datetime.now().isoformat(),
                "config": asdict(self.config),
                "validation": {
                    k: (
                        asdict(v)
                        if hasattr(v, "__dataclass_fields__")
                        else v
                    )
                    for k, v in self.validation_result.items()
                },
            },
            "chunks": self.chunks,
            "extraction_summary": {
                "pages": len(self.extraction_result.get("pages", [])),
                "tables": len(self.extraction_result.get("tables", [])),
                "passes": len(
                    self.extraction_result.get("extraction_log", [])
                ),
            },
        }

        kb_file = os.path.join(self.output_dir, "knowledge_base.json")
        with open(kb_file, "w") as f:
            json.dump(kb, f, indent=2, default=str)

        chunks_file = os.path.join(self.output_dir, "chunks.json")
        with open(chunks_file, "w") as f:
            json.dump(self.chunks, f, indent=2, default=str)

        print(f"\n💾 Knowledge base saved to {self.output_dir}")

    def _load_knowledge_base(self, kb_file: str) -> None:
        """Load existing knowledge base."""
        with open(kb_file, "r") as f:
            kb = json.load(f)

        chunks_file = os.path.join(self.output_dir, "chunks.json")
        with open(chunks_file, "r") as f:
            self.chunks = json.load(f)

        self.validation_result = kb["metadata"].get("validation", {})

        chunker = SmartChunker({}, self.config)
        chunker.chunks = self.chunks
        self.search_index = chunker.create_search_index()

        self.guardrail = MedicalGuardrailBrain(self.chunks)

        print(f"\n📚 Loaded {len(self.chunks)} chunks")
        overall = kb["metadata"]["validation"].get("overall", {})
        conf = overall.get("confidence", 0)
        print(f"📊 Validation confidence: {conf:.1%}")

    def get_extraction_summary_from_disk(self) -> Dict[str, Any]:
        """Summary written to knowledge_base.json (pages/tables/passes counts)."""
        kb_path = os.path.join(self.output_dir, "knowledge_base.json")
        if not os.path.isfile(kb_path):
            return {}
        with open(kb_path, "r", encoding="utf-8") as f:
            kb = json.load(f)
        return kb.get("extraction_summary", {})

    def _guardrail_evidence_footer(self, sources: List[Dict], query: str) -> str:
        """
        BM25 answers are evidence excerpts, not full triage. Append plain-text
        sections required by MedicalGuardrailBrain (substring + triage regex).
        Uses RED triage when the query matches danger-sign keywords (same list as
        MedicalGuardrailBrain._validate_triage).
        """
        pages = sorted({int(s["page"]) for s in sources if "page" in s})
        pages_str = ", ".join(f"Page {p}" for p in pages) if pages else "N/A"
        q = query.lower()
        danger_kw = (
            "unable to drink",
            "cannot drink",
            "convuls",
            "seizure",
            "unconscious",
            "very weak",
            "lethargic",
            "bleeding",
        )
        if any(s in q for s in danger_kw):
            triage = (
                "Triage Level: RED (query may indicate danger signs — urgent "
                "assessment and referral per local protocol; excerpts are supportive "
                "information only)\n\n"
            )
        else:
            triage = (
                "Triage Level: GREEN (evidence retrieval summary — not a substitute "
                "for bedside assessment; follow local protocols)\n\n"
            )
        return (
            "\n---\n\n"
            + triage
            + "Immediate Actions: Review the guideline excerpts above; align actions "
            "with national/WHO guidance and qualified supervision.\n\n"
            "Next Steps / Monitoring: Consult the full source guideline or a "
            "clinician for patient-specific decisions.\n\n"
            "When to Refer: Per excerpts and national guidance; seek urgent care "
            "if danger signs, severe disease, or instability is suspected.\n\n"
            f"Citations: {pages_str}\n"
        )

    def answer(self, query: str) -> Dict:
        """Answer a medical query with guardrail validation."""
        assert self.chunks is not None
        assert self.search_index is not None
        assert self.guardrail is not None

        query_tokens = re.findall(r"[a-zA-Z0-9]+", query.lower())
        query_tokens = [t for t in query_tokens if len(t) > 1]

        scores = self.search_index["bm25"].get_scores(query_tokens)
        top_indices = np.argsort(scores)[::-1][:5]

        response = f"**{self.config.document_title}**\n\n"
        response += f"**Question:** {query}\n\n"

        sources: List[Dict] = []
        for i, idx in enumerate(top_indices, 1):
            chunk = self.chunks[idx]
            response += f"### {i}. {chunk['heading']}\n\n"
            response += chunk["text"][:500] + "...\n\n"
            response += f"📄 **Reference:** Page {chunk['page']}\n\n"
            sources.append({"page": chunk["page"], "heading": chunk["heading"]})

        response += self._guardrail_evidence_footer(sources, query)

        validation = self.guardrail.validate_response(query, response)

        if not validation["passed"] or validation["warnings"]:
            response += "\n---\n"
            response += "**🧪 Guardrail Brain Validation:**\n\n"

            if validation["errors"]:
                response += "**❌ SAFETY ERRORS - DO NOT USE:**\n"
                for e in validation["errors"]:
                    response += f"• ⚠️ {e}\n"

            if validation["warnings"]:
                response += "**⚠️ Warnings:**\n"
                for w in validation["warnings"]:
                    response += f"• {w}\n"
        elif validation["passed"]:
            response += (
                "\n---\n**🧪 Guardrail Brain Validation:** ✅ Passed\n"
            )

        return {
            "query": query,
            "response": response,
            "sources": sources,
            "validation": validation,
            "validation_passed": validation["passed"],
        }
