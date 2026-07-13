# DNA Analysis Toolkit — Progress

## Session Handoff (update every session)
- Last completed phase: Phase 4 — CLI Wiring + GC Content
- Next action: Start Phase 5 — motif search (`analysis/motif_search.py`,
  `MotifMatch` dataclass, `dna-toolkit motif-search <file> --motif <seq>
  [--both-strands]`)
- Open decisions / questions: none

## Phase Checklist
- [x] Phase 0 — Scaffolding & Packaging
- [x] Phase 1 — protein-function-prediction Cleanup
- [x] Phase 2 — Sequence Model & Validation
- [x] Phase 3 — FASTA I/O
- [x] Phase 4 — CLI Wiring + GC Content
- [ ] Phase 5 — Motif Search
- [ ] Phase 6 — ORF Detection
- [ ] Phase 7 — Translation
- [ ] Phase 8 — Codon Usage Analysis
- [ ] Phase 9 — Nucleotide Statistics & K-mers
- [ ] Phase 10 — Hamming & Edit Distance
- [ ] Phase 11 — Needleman-Wunsch Alignment
- [ ] Phase 12 — Smith-Waterman Alignment
- [ ] Phase 13 — Visualization I
- [ ] Phase 14 — Visualization II
- [ ] Phase 15 — Final Polish & v1.0.0 Release

## Decisions Log
- 2026-07-12: repo root is the toolkit root (no nested subfolder).
- 2026-07-12: argparse over Click/Typer — stdlib, more transparent for learning.
- 2026-07-12: MIT license; hatchling build backend.
- 2026-07-12: Phase 0 complete — `src/dna_toolkit` package installable via
  `pip install -e ".[dev]"`, `dna-toolkit --version` works, CI configured.
- 2026-07-12: Phase 1 complete — removed stray `protein-function-prediction/
  src/io` file, migrated its misfiled roadmap notes to `docs/roadmap.md`,
  added a parked-status README to `protein-function-prediction/`.
- 2026-07-12: Phase 2 complete — added `Sequence` frozen dataclass
  (`models/sequence.py`) with validation, normalization, and
  `reverse_complement()`; DNA alphabet/IUPAC constants in `config.py`;
  `utils/validation.py` raises `SequenceValidationError` naming the bad
  character and 1-based position.
- 2026-07-12: Phase 3 complete — `io/fasta_parser.py` (`parse_fasta`,
  raises `FastaParseError` with line number) and `io/writer.py`
  (`write_fasta`, wraps at 60 chars by default); added
  `data/examples/demo_seq_1.fasta` (the shared tutorial sequence used from
  here on) and `data/examples/demo_multi.fasta`.
- 2026-07-12: Phase 4 complete — first end-to-end pipeline. Added
  `analysis/gc_content.py`, `services/analysis_service.py` (thin
  orchestration layer, extended by every later analysis phase), and
  `utils/logging.py` (`--verbose`/`-v`). CLI gained
  `dna-toolkit gc-content <file>`; FastaParseError/SequenceValidationError/
  OSError are caught at the CLI boundary and printed as one-line `Error: ...`
  messages instead of raw tracebacks.
