"""Small shared helper functions used across the toolkit."""

from dna_toolkit.config import COMPLEMENT_MAP


def reverse_complement_str(bases: str) -> str:
    """Return the reverse complement of a raw, already-normalized base string.

    Unlike Sequence.reverse_complement(), this works on plain strings
    (motifs, ORF candidates, etc.) without the overhead of constructing a
    new validated Sequence.
    """
    return "".join(COMPLEMENT_MAP[base] for base in reversed(bases))
