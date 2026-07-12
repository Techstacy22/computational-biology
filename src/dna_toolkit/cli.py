"""Command-line interface for the DNA Analysis Toolkit."""

import argparse
from collections.abc import Sequence

from dna_toolkit import __version__


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
    return parser


def run(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    parser.parse_args(argv)
    return 0
