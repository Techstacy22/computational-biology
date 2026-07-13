"""Parsing for the FASTA sequence file format."""

from pathlib import Path

from dna_toolkit.models.sequence import Sequence


class FastaParseError(ValueError):
    """Raised when a FASTA file is malformed."""


def _build_record(id_: str, description: str, bases_parts: list[str]) -> Sequence:
    return Sequence(id=id_, bases="".join(bases_parts), description=description)


def parse_fasta(path: str | Path) -> list[Sequence]:
    """Parse a FASTA file into a list of Sequence objects.

    Each `>` line starts a new record; its first whitespace-separated token
    becomes the id, and the rest of the line becomes the description.
    Following lines are concatenated as that record's bases until the next
    `>` line or end of file.

    Raises:
        FastaParseError: if sequence data appears before any `>` header,
            naming the offending line number.
    """
    path = Path(path)
    records: list[Sequence] = []

    current_id: str | None = None
    current_description = ""
    current_bases: list[str] = []

    with path.open() as f:
        for line_number, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            if not line:
                continue

            if line.startswith(">"):
                if current_id is not None:
                    records.append(_build_record(current_id, current_description, current_bases))
                header = line[1:].strip()
                parts = header.split(maxsplit=1)
                current_id = parts[0] if parts else ""
                current_description = parts[1] if len(parts) > 1 else ""
                current_bases = []
            elif current_id is None:
                raise FastaParseError(f"sequence data before any header at line {line_number}")
            else:
                current_bases.append(line)

    if current_id is not None:
        records.append(_build_record(current_id, current_description, current_bases))

    return records
