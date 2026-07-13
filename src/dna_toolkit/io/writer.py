"""Writing Sequence objects back out to the FASTA format."""

from pathlib import Path

from dna_toolkit.models.sequence import Sequence


def write_fasta(sequences: list[Sequence], path: str | Path, line_width: int = 60) -> None:
    """Write a list of Sequence objects to a FASTA file.

    Sequence lines are wrapped at `line_width` characters, matching the
    conventional FASTA formatting used by most bioinformatics tools.
    """
    path = Path(path)
    with path.open("w") as f:
        for seq in sequences:
            header = seq.id if not seq.description else f"{seq.id} {seq.description}"
            f.write(f">{header}\n")
            for i in range(0, len(seq.bases), line_width):
                f.write(seq.bases[i : i + line_width] + "\n")
