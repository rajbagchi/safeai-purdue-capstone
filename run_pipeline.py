"""
Complete production pipeline for WHO Malaria Guidelines
with multi-pass extraction, validation, chunking, and two-brain Q&A.

Entry point: run from project root with:
  python run_pipeline.py
  python -m pipeline   # alternative
"""

import warnings
warnings.filterwarnings("ignore")

from pipeline.cli import main

if __name__ == "__main__":
    main()
