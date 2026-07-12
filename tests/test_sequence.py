import pytest

from dna_toolkit.models.sequence import Sequence
from dna_toolkit.utils.validation import SequenceValidationError


def test_valid_construction() -> None:
    seq = Sequence(id="demo", bases="ATGC")
    assert seq.bases == "ATGC"
    assert len(seq) == 4


def test_lowercase_input_is_normalized() -> None:
    seq = Sequence(id="demo", bases="atgGCTa")
    assert seq.bases == "ATGGCTA"


def test_whitespace_is_stripped() -> None:
    seq = Sequence(id="demo", bases="  ATGC\n")
    assert seq.bases == "ATGC"


def test_invalid_character_raises_with_position() -> None:
    with pytest.raises(SequenceValidationError, match="position 3"):
        Sequence(id="demo", bases="ATXG")


def test_empty_sequence_raises() -> None:
    with pytest.raises(SequenceValidationError):
        Sequence(id="demo", bases="")


def test_ambiguity_code_allowed_by_default() -> None:
    seq = Sequence(id="demo", bases="ATGN")
    assert seq.bases == "ATGN"


def test_reverse_complement() -> None:
    seq = Sequence(id="demo", bases="ATGC")
    rc = seq.reverse_complement()
    assert rc.bases == "GCAT"
    assert rc.id == "demo_revcomp"
    assert len(rc) == 4


def test_reverse_complement_handles_ambiguity_codes() -> None:
    seq = Sequence(id="demo", bases="ATGN")
    assert seq.reverse_complement().bases == "NCAT"


def test_reverse_complement_is_involutive() -> None:
    seq = Sequence(id="demo", bases="ATGGCTGATCG")
    assert seq.reverse_complement().reverse_complement().bases == seq.bases
