"""Entry point for the dna-toolkit console script."""

import sys

from dna_toolkit.cli import run


def main() -> int:
    return run(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
