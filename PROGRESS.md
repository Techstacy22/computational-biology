# DNA Analysis Toolkit — Progress

## Session Handoff (update every session)
- Last completed phase: Phase 0 — Project Scaffolding & Packaging
- Next action: Start Phase 1 — clean up `protein-function-prediction/` and
  migrate its roadmap notes into `docs/roadmap.md`
- Open decisions / questions: none

## Phase Checklist
- [x] Phase 0 — Scaffolding & Packaging
- [ ] Phase 1 — protein-function-prediction Cleanup
- [ ] Phase 2 — Sequence Model & Validation
- [ ] Phase 3 — FASTA I/O
- [ ] Phase 4 — CLI Wiring + GC Content
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
