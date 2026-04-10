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
from .config import medical_source_for_config
from .response import (
    ResponseFormat,
    ResponseOrchestrator,
    infer_triage_from_query,
)
from .retriever import HybridRetriever
from .clinical_verifier import ClinicalVerifier


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
        self._retriever: Optional[HybridRetriever] = None
        self._response_orchestrator: Optional[ResponseOrchestrator] = None
        self._verifier: Optional[ClinicalVerifier] = None

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
        children = chunker.create_child_chunks(
            doc_title=getattr(self.config, "document_title", "")
        )
        # Use children for retrieval when available (richer contextual_content);
        # fall back to parent chunks when child generation produces nothing.
        retrieval_units = children if children else self.chunks
        self._retriever = HybridRetriever(
            retrieval_units,
            drug_keywords=getattr(self.config, "drug_keywords", None),
            condition_patterns=getattr(self.config, "condition_patterns", None),
        )

        print("\n" + "=" * 70)
        print("STEP 4: STAGE 4b — CLINICAL VERIFICATION PACKAGE")
        print("=" * 70)

        self._verifier = ClinicalVerifier(self.chunks, self.config)
        self._verifier.generate(
            output_dir=self.output_dir,
            doc_title=getattr(self.config, "document_title", ""),
            source_pdf=getattr(self.config, "pdf_path", ""),
        )

        print("\n" + "=" * 70)
        print("STEP 5: INITIALIZING GUARDRAIL BRAIN")
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
                "images": len(self.extraction_result.get("images", [])),
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
        children = chunker.create_child_chunks(
            doc_title=getattr(self.config, "document_title", "")
        )
        retrieval_units = children if children else self.chunks
        self._retriever = HybridRetriever(
            retrieval_units,
            drug_keywords=getattr(self.config, "drug_keywords", None),
            condition_patterns=getattr(self.config, "condition_patterns", None),
        )

        self._verifier = ClinicalVerifier(self.chunks, self.config)
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
        BM25 answers are evidence excerpts. Append sections required by
        MedicalGuardrailBrain. Triage line uses infer_triage_from_query (RED /
        YELLOW / GREEN) so it matches the response layer.
        """
        from .config import TriageLevel as TL

        pages = sorted({int(s["page"]) for s in sources if "page" in s})
        pages_str = ", ".join(f"Page {p}" for p in pages) if pages else "N/A"
        level, _reasons = infer_triage_from_query(query)
        if level == TL.RED:
            triage = (
                "Triage Level: RED (query may indicate danger signs — urgent "
                "assessment and referral per local protocol; excerpts are supportive "
                "information only)\n\n"
            )
        elif level == TL.YELLOW:
            triage = (
                "Triage Level: YELLOW (time-sensitive symptoms — assess at health "
                "facility today per local protocol; excerpts are supportive only)\n\n"
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

    def _retrieve_top_k(self, query: str, k: int = 5) -> tuple[List[int], List[Dict], List[Dict]]:
        """
        Hybrid top-k retrieval (dense + BM25 + RRF when deps available, else BM25-only).
        Returns: indices (best-effort), slim sources {page, heading}, full chunk dicts.
        """
        assert self.chunks is not None
        assert self._retriever is not None
        chunk_dicts = self._retriever.retrieve(query, k)
        sources: List[Dict] = [
            {"page": c["page"], "heading": c.get("heading", "")}
            for c in chunk_dicts
        ]
        # Build index list for callers that use positional indices.
        id_to_idx = {c["chunk_id"]: i for i, c in enumerate(self.chunks)}
        indices = [id_to_idx.get(c["chunk_id"], -1) for c in chunk_dicts]
        return indices, sources, chunk_dicts

    def answer(self, query: str) -> Dict:
        """Answer a medical query with guardrail validation."""
        assert self.guardrail is not None

        _, sources, chunks_top = self._retrieve_top_k(query, 5)

        response = f"**{self.config.document_title}**\n\n"
        response += f"**Question:** {query}\n\n"

        for i, (s, chunk) in enumerate(zip(sources, chunks_top), 1):
            response += f"### {i}. {s['heading']}\n\n"
            response += chunk["text"][:500] + "...\n\n"
            response += f"📄 **Reference:** Page {s['page']}\n\n"

        response += self._guardrail_evidence_footer(sources, query)

        validation = self.guardrail.validate_response(query, response, chunks_top)

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

    def _response_orch(self) -> ResponseOrchestrator:
        if self._response_orchestrator is None:
            self._response_orchestrator = ResponseOrchestrator()
        return self._response_orchestrator

    # ------------------------------------------------------------------
    # Offline query preprocessing
    # ------------------------------------------------------------------

    @staticmethod
    def _preprocess_query(query: str) -> str:
        """
        Rewrite a conversational query into a retrieval-optimised form.
        Runs entirely offline — no API calls, no internet access.

        Two steps:
        1. Strip conversational framing ("A lady has...", "My child is...")
           so the retriever sees clinical terms, not pronouns and filler.
        2. Expand key medical terms with synonyms so BM25 and dense
           retrieval find relevant chunks even when the user's phrasing
           differs from the guideline's vocabulary.
        """
        _CONV_INTRO = re.compile(
            r"^(?:a |an |the )?"
            r"(?:patient|lady|woman|child|infant|baby|man|boy|girl|person|mother|"
            r"male|female|adult|toddler|neonate|newborn)\s+"
            r"(?:has |have |is |was |presents?\s+(?:with\s+)?|"
            r"comes?\s+in\s+(?:with\s+)?|complains?\s+of\s+)?",
            re.IGNORECASE,
        )
        # Synonym map: only entries where the user's term is genuinely different
        # from the document's term in a way the embedding model cannot bridge.
        # Do NOT add per-symptom or per-condition entries — for normal medical
        # vocabulary BM25 handles exact matching and the cross-encoder handles
        # semantic matching without help.  US↔British spelling is handled
        # separately by HybridRetriever._normalize_medical_spelling().
        _SYNONYMS: List[tuple] = [
            # Lay / consumer terms whose clinical equivalents look completely different
            (r"\bappendicitis\b",   "appendicitis acute abdomen right iliac fossa"),
            (r"\bheart attack\b",   "heart attack myocardial infarction cardiac"),
            (r"\bstroke\b",         "stroke cerebrovascular accident CVA"),
            (r"\bhigh blood pressure\b", "high blood pressure hypertension"),
        ]

        q = query.strip()
        # Strip conversational introduction
        q_stripped = _CONV_INTRO.sub("", q).strip()
        if len(q_stripped) >= 8:  # only use stripped version if something remains
            q = q_stripped

        # Append synonyms for matched terms
        for pattern, expansion in _SYNONYMS:
            if re.search(pattern, q, re.IGNORECASE):
                for syn in expansion.split():
                    if syn.lower() not in q.lower():
                        q = q + " " + syn

        return q if q.strip() else query

    def answer_with_response(self, query: str) -> Dict[str, Any]:
        """
        Full pipeline output: BM25 + guardrail + VHT response layer (standard,
        quick, referral note) + structured ResponseContent.
        """
        assert self.guardrail is not None

        # Preprocess the query offline before retrieval (strips conversational
        # framing, expands medical synonyms).  The original query is kept for
        # triage inference, response formatting, and display.
        retrieval_query = self._preprocess_query(query)
        _, sources, retrieved_chunks = self._retrieve_top_k(retrieval_query, 5)

        response = f"**{self.config.document_title}**\n\n"
        response += f"**Question:** {query}\n\n"
        for i, (s, chunk) in enumerate(zip(sources, retrieved_chunks), 1):
            response += f"### {i}. {s['heading']}\n\n"
            response += chunk["text"][:500] + "...\n\n"
            response += f"📄 **Reference:** Page {s['page']}\n\n"

        response += self._guardrail_evidence_footer(sources, query)
        validation = self.guardrail.validate_response(query, response, retrieved_chunks)

        if not validation["passed"] or validation["warnings"]:
            response += "\n---\n**🧪 Guardrail Brain Validation:**\n\n"
            if validation["errors"]:
                response += "**❌ SAFETY ERRORS - DO NOT USE:**\n"
                for e in validation["errors"]:
                    response += f"• ⚠️ {e}\n"
            if validation["warnings"]:
                response += "**⚠️ Warnings:**\n"
                for w in validation["warnings"]:
                    response += f"• {w}\n"
        elif validation["passed"]:
            response += "\n---\n**🧪 Guardrail Brain Validation:** ✅ Passed\n"

        triage, triage_reasons = infer_triage_from_query(query)
        med_src = medical_source_for_config(self.config)
        orch = self._response_orch()
        structured = orch.create(
            query=query,
            triage=triage,
            triage_reasons=triage_reasons,
            guardrail_output=validation,
            retrieved_chunks=retrieved_chunks,
            source=med_src,
            dosage_info=None,
        )

        return {
            "query": query,
            "response": response,
            "sources": sources,
            "validation": validation,
            "validation_passed": validation["passed"],
            "triage": triage,
            "triage_reasons": triage_reasons,
            "vht_response": structured.to_vht_format(),
            "referral_note": orch.formatter.format(structured, ResponseFormat.REFERRAL),
            "quick_summary": orch.formatter.format(structured, ResponseFormat.VHT_QUICK),
            "structured": structured,
            # Raw retrieved chunks — used by chat.py for "no match" detection
            # via the _ce_best_raw field set by the retriever.
            "_retrieved_chunks": retrieved_chunks,
        }
