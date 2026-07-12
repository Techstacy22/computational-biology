"""The core DNA sequence data model used throughout the toolkit."""

from dataclasses import dataclass

from dna_toolkit.config import COMPLEMENT_MAP
from dna_toolkit.utils.validation import normalize_sequence, validate_dna_sequence


@dataclass(frozen=True)
class Sequence:
    """An immutable, validated DNA sequence.

    Attributes:
        id: A short identifier (e.g. a FASTA header's first token).
        bases: The nucleotide string, normalized to uppercase on construction.
        description: Optional free-text description (e.g. rest of a FASTA header).
    """

    id: str
    bases: str
    description: str = ""

    def __post_init__(self) -> None:
        normalized = normalize_sequence(self.bases)
        validate_dna_sequence(normalized)
        # The dataclass is frozen (immutable) everywhere except here, where we
        # still need to store the normalized bases computed above.
        object.__setattr__(self, "bases", normalized)

    def __len__(self) -> int:
        return len(self.bases)

    def reverse_complement(self) -> "Sequence":
        """Return the reverse complement: the sequence on the other strand."""
        complemented = "".join(COMPLEMENT_MAP[base] for base in reversed(self.bases))
        return Sequence(
            id=f"{self.id}_revcomp",
            bases=complemented,
            description=self.description,
        )
