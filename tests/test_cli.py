from pathlib import Path

import pytest

from dna_toolkit import __version__
from dna_toolkit.cli import run


def test_version_flag(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        run(["--version"])

    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert __version__ in captured.out


def test_no_args_returns_zero() -> None:
    assert run([]) == 0


def test_gc_content_command(capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
    fasta_file = tmp_path / "seq.fasta"
    fasta_file.write_text(">seq1\nATGC\n")

    exit_code = run(["gc-content", str(fasta_file)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "seq1" in captured.out
    assert "GC Content: 50.00%" in captured.out


def test_gc_content_command_missing_file_is_friendly(
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = run(["gc-content", "does_not_exist.fasta"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert captured.err.startswith("Error:")
    assert "Traceback" not in captured.err


def test_gc_content_command_malformed_file_is_friendly(
    capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    fasta_file = tmp_path / "bad.fasta"
    fasta_file.write_text("ATGC\n>seq1\nGGTA\n")

    exit_code = run(["gc-content", str(fasta_file)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.err.startswith("Error:")


def test_motif_search_command(capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
    fasta_file = tmp_path / "seq.fasta"
    fasta_file.write_text(">seq1\nATGGAATTCGG\n")

    exit_code = run(["motif-search", str(fasta_file), "--motif", "GAATTC"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "+ strand, position 3-9: GAATTC" in captured.out


def test_motif_search_command_no_match(capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
    fasta_file = tmp_path / "seq.fasta"
    fasta_file.write_text(">seq1\nATGGGG\n")

    exit_code = run(["motif-search", str(fasta_file), "--motif", "TTTT"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "No matches for 'TTTT' found." in captured.out
