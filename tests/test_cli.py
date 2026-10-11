"""Tests for the command line interface."""

from __future__ import annotations

from pathlib import Path

import pytest

from repotoc.cli import main

# The CLI exit codes: success, stale check, and error.
_EXIT_SUCCESS = 0
_EXIT_STALE = 1
_EXIT_ERROR = 2


def _write(root: Path, name: str, source: str = '"""Doc."""\n') -> Path:
    """Write a source file under a root, creating parent directories."""
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")
    return path


def _write_pyproject(tmp_path: Path, section: str) -> None:
    """Write a pyproject file with a `[tool.repotoc]` section."""
    (tmp_path / "pyproject.toml").write_text(
        f"[tool.repotoc]\n{section}", encoding="utf-8"
    )


def _exit_code(argv: list[str]) -> int:
    """Run the CLI in-process and return its exit code."""
    with pytest.raises(SystemExit) as info:
        main(argv)
    code = info.value.code
    assert isinstance(code, int)
    return code


def test_cli_generates_the_artifact_under_the_default_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Positional sources regenerate the artifact under docs/repotoc."""
    monkeypatch.chdir(tmp_path)
    _write(tmp_path, "src/mod.py", '"""Does things."""\n')

    code = _exit_code(["src"])

    assert code == _EXIT_SUCCESS
    assert (tmp_path / "docs" / "repotoc" / "src" / "mod.md").read_text(
        encoding="utf-8"
    ) == "# src/mod.py\n\n> Does things.\n"


def test_cli_runs_from_config_alone_with_no_arguments(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A zero-argument run generates from the config sources."""
    monkeypatch.chdir(tmp_path)
    _write(tmp_path, "src/mod.py")
    _write_pyproject(tmp_path, 'sources = ["src"]\noutput = "docs/api"\n')

    code = _exit_code([])

    assert code == _EXIT_SUCCESS
    assert (tmp_path / "docs" / "api" / "src" / "mod.md").is_file()


def test_cli_values_win_over_config_values(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """When the CLI and the config both set a value, the CLI value wins."""
    monkeypatch.chdir(tmp_path)
    _write(tmp_path, "src/mod.py")
    _write_pyproject(tmp_path, 'sources = ["src"]\noutput = "config-out"\n')

    code = _exit_code(["src", "--output", "cli-out"])

    assert code == _EXIT_SUCCESS
    assert (tmp_path / "cli-out" / "src" / "mod.md").is_file()
    assert not (tmp_path / "config-out").exists()


def test_cli_sources_replace_config_sources(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """CLI sources replace config sources instead of merging with them."""
    monkeypatch.chdir(tmp_path)
    _write(tmp_path, "cfg-src/a.py")
    _write(tmp_path, "src/b.py")
    _write_pyproject(tmp_path, 'sources = ["cfg-src"]\n')

    code = _exit_code(["src"])

    assert code == _EXIT_SUCCESS
    assert (tmp_path / "docs" / "repotoc" / "src" / "b.md").is_file()
    assert not (tmp_path / "docs" / "repotoc" / "cfg-src").exists()


def test_cli_flags_reach_collection_and_rendering(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Every presentation flag and `--exclude` reach the run."""
    monkeypatch.chdir(tmp_path)
    _write(tmp_path, "src/generated/junk.py")
    _write(
        tmp_path,
        "src/mod.py",
        '''"""Doc."""

def _private():
    """Private."""

def public(a):
    """Public."""
''',
    )

    code = _exit_code(
        [
            "src",
            "--file-member-depth",
            "1",
            "--file-include-privates",
            "--no-file-include-signatures",
            "--toc-max-depths",
            "4",
            "2",
            "--exclude",
            "generated",
        ]
    )

    assert code == _EXIT_SUCCESS
    text = (tmp_path / "docs" / "repotoc" / "src" / "mod.md").read_text(
        encoding="utf-8"
    )
    assert "_private" in text
    assert "def public(a)" not in text
    assert not (tmp_path / "docs" / "repotoc" / "src" / "generated").exists()


def test_cli_check_exits_zero_when_fresh(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """`--check` against a freshly generated artifact exits 0."""
    monkeypatch.chdir(tmp_path)
    _write(tmp_path, "src/mod.py")
    assert _exit_code(["src"]) == _EXIT_SUCCESS

    code = _exit_code(["src", "--check"])

    assert code == _EXIT_SUCCESS
    assert capsys.readouterr().out == ""


def test_cli_check_exits_one_and_lists_missing_differing_and_extra_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A stale check exits 1 listing every offending file."""
    monkeypatch.chdir(tmp_path)
    _write(tmp_path, "src/mod.py")
    assert _exit_code(["src"]) == _EXIT_SUCCESS
    output = tmp_path / "docs" / "repotoc"
    (output / "src" / "mod.md").write_text("changed", encoding="utf-8")
    (output / "src" / "repotoc_index.md").unlink()
    (output / "extra.md").write_text("extra", encoding="utf-8")

    code = _exit_code(["src", "--check"])

    assert code == _EXIT_STALE
    assert capsys.readouterr().out.splitlines() == [
        "extra: extra.md",
        "differing: src/mod.md",
        "missing: src/repotoc_index.md",
    ]


def test_cli_check_with_no_output_directory_lists_every_file_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """`--check` before any generation lists every rendered file as missing."""
    monkeypatch.chdir(tmp_path)
    _write(tmp_path, "src/mod.py")

    code = _exit_code(["src", "--check"])

    assert code == _EXIT_STALE
    assert capsys.readouterr().out.splitlines() == [
        "missing: repotoc_index.md",
        "missing: src/mod.md",
        "missing: src/repotoc_index.md",
    ]


def test_cli_without_sources_exits_two_with_a_usage_message(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """No sources from the CLI or config exits 2 with a usage message."""
    monkeypatch.chdir(tmp_path)

    code = _exit_code([])

    assert code == _EXIT_ERROR
    assert "usage: repotoc" in capsys.readouterr().err


def test_cli_invalid_config_exits_two_naming_the_offense(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A config that fails to load exits 2 with the error on stderr."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "pyproject.toml").write_text("[tool.repotoc\n", encoding="utf-8")

    code = _exit_code([])

    assert code == _EXIT_ERROR
    assert "invalid TOML" in capsys.readouterr().err


def test_cli_wrongly_typed_config_value_exits_two_naming_the_key(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A wrongly typed config value exits 2 naming the key."""
    monkeypatch.chdir(tmp_path)
    _write_pyproject(tmp_path, 'sources = ["src"]\nfile_member_depth = "2"\n')

    code = _exit_code([])

    assert code == _EXIT_ERROR
    assert "file_member_depth" in capsys.readouterr().err


def test_cli_usage_errors_exit_two_for_bad_flag_values(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A non-integer or non-positive depth value exits 2 as a usage error."""
    monkeypatch.chdir(tmp_path)
    _write(tmp_path, "src/mod.py")

    assert _exit_code(["src", "--file-member-depth", "two"]) == _EXIT_ERROR
    assert _exit_code(["src", "--file-member-depth", "0"]) == _EXIT_ERROR
    assert _exit_code(["src", "--toc-max-depths", "0"]) == _EXIT_ERROR


def test_cli_missing_root_exits_two_with_the_exception_message(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A missing collection root exits 2 with the error on stderr."""
    monkeypatch.chdir(tmp_path)

    code = _exit_code(["missing"])

    assert code == _EXIT_ERROR
    assert "collection root does not exist" in capsys.readouterr().err


def test_cli_parse_error_exits_two_with_the_exception_message(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A source file with a syntax error exits 2 with the error on stderr."""
    monkeypatch.chdir(tmp_path)
    _write(tmp_path, "src/mod.py", "def broken(:\n")

    code = _exit_code(["src"])

    assert code == _EXIT_ERROR
    assert "mod.py" in capsys.readouterr().err


def test_cli_generation_error_exits_two_with_the_exception_message(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A filesystem error from generation exits 2 with the error on stderr."""
    monkeypatch.chdir(tmp_path)
    _write(tmp_path, "src/mod.py")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "repotoc").write_text("occupied", encoding="utf-8")

    code = _exit_code(["src"])

    assert code == _EXIT_ERROR
    assert "docs/repotoc" in capsys.readouterr().err


def test_cli_filesystem_error_during_check_exits_two(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A filesystem error while checking exits 2 with the error on stderr."""
    monkeypatch.chdir(tmp_path)
    _write(tmp_path, "src/mod.py")
    assert _exit_code(["src"]) == _EXIT_SUCCESS

    def fail_read_bytes(self: Path) -> bytes:  # noqa: ARG001
        message = "read failed"
        raise OSError(message)

    monkeypatch.setattr(Path, "read_bytes", fail_read_bytes)
    code = _exit_code(["src", "--check"])

    assert code == _EXIT_ERROR
    assert "read failed" in capsys.readouterr().err
