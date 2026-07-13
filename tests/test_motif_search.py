from dna_toolkit.analysis.motif_search import find_motif
from dna_toolkit.models.sequence import Sequence

DEMO_BASES = "ATGGCTGATCGTACGGAATTCGCTTGGTAAGGATCCGAATTCTAG"


def test_finds_both_occurrences_of_palindromic_motif() -> None:
    seq = Sequence(id="demo", bases=DEMO_BASES)

    matches = find_motif(seq, "GAATTC", both_strands=False)

    assert [(m.start, m.end) for m in matches] == [(15, 21), (36, 42)]
    assert all(m.strand == "+" for m in matches)


def test_both_strands_finds_reverse_strand_match() -> None:
    # "AAAT" doesn't appear forward, but its reverse complement "ATTT" does
    # -- meaning "AAAT" occurs on the reverse strand at that position.
    seq = Sequence(id="demo", bases="GGCATTTGG")

    forward_only = find_motif(seq, "AAAT", both_strands=False)
    assert forward_only == []

    both = find_motif(seq, "AAAT", both_strands=True)
    assert len(both) == 1
    assert both[0].strand == "-"
    assert (both[0].start, both[0].end) == (3, 7)


def test_no_match_returns_empty_list() -> None:
    seq = Sequence(id="demo", bases="ATGCATGCATGC")
    assert find_motif(seq, "GGGGG", both_strands=False) == []


def test_motif_search_is_case_insensitive() -> None:
    seq = Sequence(id="demo", bases=DEMO_BASES)

    matches = find_motif(seq, "gaattc", both_strands=False)

    assert len(matches) == 2
