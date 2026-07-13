"""Open Reading Frame (ORF) detection."""

from dataclasses import dataclass

from dna_toolkit.models.sequence import Sequence
from dna_toolkit.utils.helpers import reverse_complement_str

START_CODON = "ATG"
STOP_CODONS = frozenset({"TAA", "TAG", "TGA"})


@dataclass(frozen=True)
class ORF:
    """A candidate protein-coding region: start codon ... stop codon, no internal stops.

    start/end are 0-based, half-open coordinates into the sequence's
    forward-strand bases (mirroring MotifMatch's convention), spanning from
    the start codon through the stop codon inclusive. `frame` is 0, 1, or 2:
    how many bases into the strand this reading frame begins. `bases` is the
    actual coding-strand sequence (already reverse-complemented for '-'
    strand ORFs), ready to hand to translate_sequence() later.

    Note: an ORF is only a *candidate* gene region -- real gene prediction
    also needs promoter/regulatory evidence, splice sites, and more. This is
    just "a stretch that could plausibly encode a protein."
    """

    start: int
    end: int
    strand: str  # "+" or "-"
    frame: int  # 0, 1, or 2
    bases: str


def find_orfs(sequence: Sequence, min_length: int = 1, both_strands: bool = True) -> list[ORF]:
    """Find all open reading frames in `sequence`.

    Scans each of the 3 forward reading frames for start_codon ... stop_codon
    runs with no internal stop codon; by default (`both_strands=True`) also
    scans the 3 reverse-strand frames, for 6 total. `min_length` filters out
    ORFs shorter than that many bases (start codon through stop, inclusive).
    """
    orfs = _find_orfs_on_strand(sequence.bases, strand="+", min_length=min_length)

    if both_strands:
        rc_bases = reverse_complement_str(sequence.bases)
        seq_len = len(sequence.bases)
        for orf in _find_orfs_on_strand(rc_bases, strand="-", min_length=min_length):
            # Translate coordinates in the reverse-complemented string back
            # into the original forward-strand coordinate frame.
            orfs.append(
                ORF(
                    start=seq_len - orf.end,
                    end=seq_len - orf.start,
                    strand=orf.strand,
                    frame=orf.frame,
                    bases=orf.bases,
                )
            )

    orfs.sort(key=lambda o: (o.start, o.strand))
    return orfs


def _find_orfs_on_strand(bases: str, strand: str, min_length: int) -> list[ORF]:
    orfs = []
    for frame in range(3):
        orfs.extend(_scan_frame(bases, frame, strand, min_length))
    return orfs


def _scan_frame(bases: str, frame: int, strand: str, min_length: int) -> list[ORF]:
    orfs = []
    orf_start: int | None = None

    for i in range(frame, len(bases) - 2, 3):
        codon = bases[i : i + 3]
        if orf_start is None:
            if codon == START_CODON:
                orf_start = i
        elif codon in STOP_CODONS:
            orf_end = i + 3
            if orf_end - orf_start >= min_length:
                orfs.append(
                    ORF(
                        start=orf_start,
                        end=orf_end,
                        strand=strand,
                        frame=frame,
                        bases=bases[orf_start:orf_end],
                    )
                )
            orf_start = None

    return orfs
