"""Command-line interface for the DNA Analysis Toolkit."""

import argparse
import sys
from collections.abc import Sequence as Args

from dna_toolkit import __version__
from dna_toolkit.io.fasta_parser import FastaParseError
from dna_toolkit.services.analysis_service import AnalysisService
from dna_toolkit.utils.logging import get_logger, set_verbosity
from dna_toolkit.utils.validation import SequenceValidationError

logger = get_logger("dna_toolkit")

# Errors we expect from bad user input (as opposed to bugs) get turned into
# a short, friendly message instead of a raw traceback.
_USER_FACING_ERRORS = (FastaParseError, SequenceValidationError, OSError)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dna-toolkit",
        description="A modular toolkit for analyzing DNA sequences.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"dna-toolkit {__version__}",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="enable verbose (debug) logging",
    )

    subparsers = parser.add_subparsers(dest="command")

    gc_parser = subparsers.add_parser(
        "gc-content",
        help="calculate the percentage of G and C bases in each sequence",
    )
    gc_parser.add_argument("file", help="path to a FASTA file")

    motif_parser = subparsers.add_parser(
        "motif-search",
        help="find occurrences of a short DNA pattern (e.g. a restriction site)",
    )
    motif_parser.add_argument("file", help="path to a FASTA file")
    motif_parser.add_argument(
        "--motif",
        required=True,
        help="the DNA pattern to search for (case-insensitive, e.g. GAATTC)",
    )
    motif_parser.add_argument(
        "--forward-only",
        action="store_true",
        help="only search the forward (+) strand; by default both strands are searched",
    )

    return parser


def _run_gc_content(args: argparse.Namespace) -> int:
    sequences = AnalysisService.load_sequences(args.file)
    logger.debug("loaded %d sequence(s) from %s", len(sequences), args.file)

    if not sequences:
        print("No sequences found in file.")
        return 0

    for seq, (_, gc_pct) in zip(sequences, AnalysisService.gc_content(sequences), strict=True):
        print(f"Sequence: {seq.id} ({len(seq)} bp)")
        print(f"GC Content: {gc_pct:.2f}%")

    return 0


def _run_motif_search(args: argparse.Namespace) -> int:
    sequences = AnalysisService.load_sequences(args.file)
    logger.debug("loaded %d sequence(s) from %s", len(sequences), args.file)

    if not sequences:
        print("No sequences found in file.")
        return 0

    both_strands = not args.forward_only
    for seq in sequences:
        matches = AnalysisService.motif_search(seq, args.motif, both_strands=both_strands)
        print(f"Sequence: {seq.id} ({len(seq)} bp)")
        if not matches:
            print(f"  No matches for '{args.motif.upper()}' found.")
            continue
        for m in matches:
            print(f"  {m.strand} strand, position {m.start}-{m.end}: {seq.bases[m.start:m.end]}")

    return 0


def run(argv: Args[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    set_verbosity(logger, args.verbose)
    logger.debug("parsed args: %s", args)

    if args.command is None:
        parser.print_help()
        return 0

    try:
        if args.command == "gc-content":
            return _run_gc_content(args)
        if args.command == "motif-search":
            return _run_motif_search(args)
    except _USER_FACING_ERRORS as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0
