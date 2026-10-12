# `tests/test_cli.py`

> Tests for the command line interface.

## `def test_cli_generates_the_artifact_under_the_default_output(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:`

> Positional sources regenerate the artifact under docs/repotoc.

---

## `def test_cli_runs_from_config_alone_with_no_arguments(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:`

> A zero-argument run generates from the config sources.

---

## `def test_cli_values_win_over_config_values(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:`

> When the CLI and the config both set a value, the CLI value wins.

---

## `def test_cli_sources_replace_config_sources(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:`

> CLI sources replace config sources instead of merging with them.

---

## `def test_cli_flags_reach_collection_and_rendering(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:`

> Every presentation flag and `--exclude` reach the run.

---

## `def test_cli_check_exits_zero_when_fresh(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:`

> `--check` against a freshly generated artifact exits 0.

---

## `def test_cli_check_exits_one_and_lists_missing_differing_and_extra_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:`

> A stale check exits 1 listing every offending file.

---

## `def test_cli_check_with_no_output_directory_lists_every_file_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:`

> `--check` before any generation lists every rendered file as missing.

---

## `def test_cli_without_sources_exits_two_with_a_usage_message(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:`

> No sources from the CLI or config exits 2 with a usage message.

---

## `def test_cli_invalid_config_exits_two_naming_the_offense(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:`

> A config that fails to load exits 2 with the error on stderr.

---

## `def test_cli_wrongly_typed_config_value_exits_two_naming_the_key(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:`

> A wrongly typed config value exits 2 naming the key.

---

## `def test_cli_usage_errors_exit_two_for_bad_flag_values(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:`

> A non-integer or non-positive depth value exits 2 as a usage error.

---

## `def test_cli_missing_root_exits_two_with_the_exception_message(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:`

> A missing collection root exits 2 with the error on stderr.

---

## `def test_cli_parse_error_exits_two_with_the_exception_message(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:`

> A source file with a syntax error exits 2 with the error on stderr.

---

## `def test_cli_generation_error_exits_two_with_the_exception_message(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:`

> A filesystem error from generation exits 2 with the error on stderr.

---

## `def test_cli_filesystem_error_during_check_exits_two(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:`

> A filesystem error while checking exits 2 with the error on stderr.
