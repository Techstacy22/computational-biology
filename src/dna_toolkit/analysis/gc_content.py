"""GC content analysis."""

from dna_toolkit.models.sequence import Sequence


def calculate_gc_content(sequence: Sequence) -> float:
    """Return the percentage of G and C bases in a sequence.

    G-C base pairs are held together by three hydrogen bonds (versus two for
    A-T), so GC-rich DNA tends to be more thermally and chemically stable.
    GC content varies characteristically between species, and even across
    regions of a single genome, making it a basic fingerprint of DNA
    composition.
    """
    gc_count = sum(1 for base in sequence.bases if base in ("G", "C"))
    return (gc_count / len(sequence)) * 100
