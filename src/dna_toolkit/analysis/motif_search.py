"""Motif search: finding short, biologically meaningful patterns in DNA."""

from dataclasses import dataclass

from dna_toolkit.models.sequence import Sequence
from dna_toolkit.utils.helpers import reverse_complement_str
from dna_toolkit.utils.validation import normalize_sequence, validate_dna_sequence


@dataclass(frozen=True)
class MotifMatch:
    """A single motif occurrence.

    start/end are 0-based, half-open coordinates into the sequence's
    forward-strand bases, i.e. `sequence.bases[start:end]` gives the
    matched text as it reads on the '+' strand (for a '-' strand match,
    that's the reverse complement of what the motif actually spells out on
    the reverse strand).
    """

    start: int
    end: int
    strand: str  # "+" or "-"


def find_motif(sequence: Sequence, motif: str, both_strands: bool = True) -> list[MotifMatch]:
    """Find all occurrences of `motif` in `sequence`.

    Motifs are short, biologically meaningful DNA patterns -- e.g.
    restriction enzyme recognition sites (GAATTC for EcoRI) or transcription
    factor binding sites. Because DNA is double-stranded, a motif can also
    occur on the reverse strand; when `both_strands` is True (the default),
    this additionally searches the forward bases for the motif's reverse
    complement and reports those hits with strand='-'. Note that most real
    restriction sites are palindromic (equal to their own reverse
    complement), so they typically show up at the same position on both
    strands.

    Matching is case-insensitive, exact substring search -- fine at the
    scale of a single gene, though whole-genome scans call for smarter
    algorithms (e.g. Boyer-Moore, KMP, or suffix arrays).
    """
    motif = normalize_sequence(motif)
    validate_dna_sequence(motif, allow_ambiguous=False)

    matches = _find_substring_matches(sequence.bases, motif, strand="+")

    if both_strands:
        rc_motif = reverse_complement_str(motif)
        matches += _find_substring_matches(sequence.bases, rc_motif, strand="-")

    matches.sort(key=lambda m: (m.start, m.strand))
    return matches


def _find_substring_matches(bases: str, pattern: str, strand: str) -> list[MotifMatch]:
    matches = []
    start = bases.find(pattern)
    while start != -1:
        matches.append(MotifMatch(start=start, end=start + len(pattern), strand=strand))
        start = bases.find(pattern, start + 1)
    return matches
