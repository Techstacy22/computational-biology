"""Normalization and validation for raw DNA sequence strings."""

from dna_toolkit.config import DNA_ALPHABET, VALID_BASES


class SequenceValidationError(ValueError):
    """Raised when a string isn't a valid DNA sequence."""


def normalize_sequence(seq: str) -> str:
    """Strip surrounding whitespace and uppercase a raw sequence string."""
    return seq.strip().upper()


def validate_dna_sequence(seq: str, allow_ambiguous: bool = True) -> None:
    """Raise SequenceValidationError if `seq` isn't a valid DNA sequence.

    Args:
        seq: An already-normalized (uppercase) sequence string.
        allow_ambiguous: If True (default), IUPAC ambiguity codes such as
            'N' are accepted in addition to the unambiguous bases A, C, G, T.
    """
    if not seq:
        raise SequenceValidationError("sequence must not be empty")

    valid_bases = VALID_BASES if allow_ambiguous else DNA_ALPHABET
    for position, base in enumerate(seq, start=1):
        if base not in valid_bases:
            raise SequenceValidationError(
                f"invalid character {base!r} at position {position} "
                f"(expected one of: {''.join(sorted(valid_bases))})"
            )
