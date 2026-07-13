import pytest

from dna_toolkit.analysis.gc_content import calculate_gc_content
from dna_toolkit.io.fasta_parser import parse_fasta
from dna_toolkit.models.sequence import Sequence


def test_all_gc() -> None:
    seq = Sequence(id="s", bases="GGCC")
    assert calculate_gc_content(seq) == 100.0


def test_no_gc() -> None:
    seq = Sequence(id="s", bases="ATAT")
    assert calculate_gc_content(seq) == 0.0


def test_known_percentage() -> None:
    seq = Sequence(id="s", bases="ATGC")
    assert calculate_gc_content(seq) == 50.0


def test_demo_sequence_gc_content() -> None:
    records = parse_fasta("data/examples/demo_seq_1.fasta")
    gc = calculate_gc_content(records[0])
    # demo_seq_1.fasta has 21 G/C bases out of 45 total.
    assert gc == pytest.approx(46.6667, abs=1e-4)
