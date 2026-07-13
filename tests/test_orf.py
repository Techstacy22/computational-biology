from dna_toolkit.analysis.orf import ORF, find_orfs
from dna_toolkit.models.sequence import Sequence

DEMO_BASES = "ATGGCTGATCGTACGGAATTCGCTTGGTAAGGATCCGAATTCTAG"


def test_finds_expected_orf_in_demo_sequence() -> None:
    seq = Sequence(id="demo", bases=DEMO_BASES)

    orfs = find_orfs(seq, both_strands=False)

    expected = ORF(
        start=0,
        end=30,
        strand="+",
        frame=0,
        bases="ATGGCTGATCGTACGGAATTCGCTTGGTAA",
    )
    assert expected in orfs


def test_min_length_filters_short_orfs() -> None:
    seq = Sequence(id="demo", bases=DEMO_BASES)

    orfs = find_orfs(seq, min_length=31, both_strands=False)

    assert all(o.end - o.start >= 31 for o in orfs)
    assert not any((o.start, o.end) == (0, 30) for o in orfs)


def test_reverse_strand_orf_detection() -> None:
    # These forward bases are the reverse complement of "ATGAAATAA" (a
    # minimal start-codon/one-codon/stop-codon ORF), so it's only found
    # when the reverse strand is scanned.
    seq = Sequence(id="demo", bases="TTATTTCAT")

    forward_only = find_orfs(seq, both_strands=False)
    assert forward_only == []

    both = find_orfs(seq, both_strands=True)
    assert len(both) == 1
    orf = both[0]
    assert orf.strand == "-"
    assert (orf.start, orf.end) == (0, 9)
    assert orf.bases == "ATGAAATAA"


def test_no_start_codon_returns_no_orfs() -> None:
    seq = Sequence(id="demo", bases="CCCCCCCCC")
    assert find_orfs(seq, both_strands=True) == []
