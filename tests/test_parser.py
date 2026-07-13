from pathlib import Path

import pytest

from dna_toolkit.io.fasta_parser import FastaParseError, parse_fasta
from dna_toolkit.io.writer import write_fasta
from dna_toolkit.models.sequence import Sequence


def test_parse_single_record(tmp_path: Path) -> None:
    fasta_file = tmp_path / "single.fasta"
    fasta_file.write_text(">seq1 a test sequence\nATGC\nGGTA\n")

    records = parse_fasta(fasta_file)

    assert len(records) == 1
    assert records[0].id == "seq1"
    assert records[0].description == "a test sequence"
    assert records[0].bases == "ATGCGGTA"


def test_parse_multi_record(tmp_path: Path) -> None:
    fasta_file = tmp_path / "multi.fasta"
    fasta_file.write_text(">seq_a\nATGC\n>seq_b\nGGTA\n")

    records = parse_fasta(fasta_file)

    assert [r.id for r in records] == ["seq_a", "seq_b"]
    assert [r.bases for r in records] == ["ATGC", "GGTA"]


def test_lowercase_bases_are_normalized(tmp_path: Path) -> None:
    fasta_file = tmp_path / "lower.fasta"
    fasta_file.write_text(">seq1\natgc\n")

    records = parse_fasta(fasta_file)

    assert records[0].bases == "ATGC"


def test_malformed_file_raises_with_line_number(tmp_path: Path) -> None:
    fasta_file = tmp_path / "bad.fasta"
    fasta_file.write_text("ATGC\n>seq1\nGGTA\n")

    with pytest.raises(FastaParseError, match="line 1"):
        parse_fasta(fasta_file)


def test_empty_file_returns_empty_list(tmp_path: Path) -> None:
    fasta_file = tmp_path / "empty.fasta"
    fasta_file.write_text("")

    assert parse_fasta(fasta_file) == []


def test_round_trip(tmp_path: Path) -> None:
    original = [
        Sequence(id="seq1", bases="ATGCGGTACC", description="round trip test"),
        Sequence(id="seq2", bases="TTGGCCAAGG"),
    ]
    fasta_file = tmp_path / "roundtrip.fasta"

    write_fasta(original, fasta_file)
    parsed = parse_fasta(fasta_file)

    assert [(s.id, s.bases, s.description) for s in parsed] == [
        (s.id, s.bases, s.description) for s in original
    ]


def test_writer_wraps_long_sequences(tmp_path: Path) -> None:
    seq = Sequence(id="long", bases="A" * 130)
    fasta_file = tmp_path / "long.fasta"

    write_fasta([seq], fasta_file, line_width=60)

    lines = fasta_file.read_text().splitlines()
    assert lines[0] == ">long"
    assert [len(line) for line in lines[1:]] == [60, 60, 10]


def test_demo_example_file_parses() -> None:
    records = parse_fasta("data/examples/demo_seq_1.fasta")

    assert len(records) == 1
    assert records[0].id == "demo_seq_1"
    assert records[0].bases == "ATGGCTGATCGTACGGAATTCGCTTGGTAAGGATCCGAATTCTAG"


def test_demo_multi_example_file_parses() -> None:
    records = parse_fasta("data/examples/demo_multi.fasta")

    assert [r.id for r in records] == ["seq_a", "seq_b"]
