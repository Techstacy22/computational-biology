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
