"""Coordinates loading sequences and running analyses on them.

This is the layer the CLI talks to: it knows how to load sequences and
which analysis functions to call, but contains no parsing or analysis logic
itself. Each new analysis feature gets one more method here.
"""

from dna_toolkit.analysis.gc_content import calculate_gc_content
from dna_toolkit.io.fasta_parser import parse_fasta
from dna_toolkit.models.sequence import Sequence


class AnalysisService:
    @staticmethod
    def load_sequences(path: str) -> list[Sequence]:
        return parse_fasta(path)

    @staticmethod
    def gc_content(sequences: list[Sequence]) -> list[tuple[str, float]]:
        return [(seq.id, calculate_gc_content(seq)) for seq in sequences]
