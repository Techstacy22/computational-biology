"""Shared constants for representing DNA sequences."""

DNA_ALPHABET = frozenset("ACGT")

# IUPAC nucleotide ambiguity codes: symbols standing in for "one of several
# possible bases," used when a base can't be called with full confidence
# (e.g. raw sequencer output, low-quality regions of a reference genome).
IUPAC_AMBIGUITY_CODES: dict[str, frozenset[str]] = {
    "A": frozenset("A"),
    "C": frozenset("C"),
    "G": frozenset("G"),
    "T": frozenset("T"),
    "R": frozenset("AG"),  # puRine
    "Y": frozenset("CT"),  # pYrimidine
    "S": frozenset("GC"),  # Strong (3 hydrogen bonds)
    "W": frozenset("AT"),  # Weak (2 hydrogen bonds)
    "K": frozenset("GT"),  # Keto
    "M": frozenset("AC"),  # aMino
    "B": frozenset("CGT"),  # not A
    "D": frozenset("AGT"),  # not C
    "H": frozenset("ACT"),  # not G
    "V": frozenset("ACG"),  # not T
    "N": frozenset("ACGT"),  # aNy base
}

VALID_BASES = frozenset(IUPAC_AMBIGUITY_CODES)

# Watson-Crick (and IUPAC-ambiguity) complements, for reverse_complement().
COMPLEMENT_MAP: dict[str, str] = {
    "A": "T",
    "T": "A",
    "C": "G",
    "G": "C",
    "R": "Y",
    "Y": "R",
    "S": "S",
    "W": "W",
    "K": "M",
    "M": "K",
    "B": "V",
    "D": "H",
    "H": "D",
    "V": "B",
    "N": "N",
}
