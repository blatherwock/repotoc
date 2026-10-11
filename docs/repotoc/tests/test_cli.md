# tests/test_cli.py

> Tests for the command line interface.

## test_cli_generates_the_artifact_under_the_default_output

> Positional sources regenerate the artifact under docs/repotoc.

```python
def test_cli_generates_the_artifact_under_the_default_output(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
```

## test_cli_runs_from_config_alone_with_no_arguments

> A zero-argument run generates from the config sources.

```python
def test_cli_runs_from_config_alone_with_no_arguments(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
```

## test_cli_values_win_over_config_values

> When the CLI and the config both set a value, the CLI value wins.

```python
def test_cli_values_win_over_config_values(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
```

## test_cli_sources_replace_config_sources

> CLI sources replace config sources instead of merging with them.

```python
def test_cli_sources_replace_config_sources(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
```

## test_cli_flags_reach_collection_and_rendering

> Every presentation flag and `--exclude` reach the run.

```python
def test_cli_flags_reach_collection_and_rendering(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
```

## test_cli_check_exits_zero_when_fresh

> `--check` against a freshly generated artifact exits 0.

```python
def test_cli_check_exits_zero_when_fresh(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
```

## test_cli_check_exits_one_and_lists_missing_differing_and_extra_files

> A stale check exits 1 listing every offending file.

```python
def test_cli_check_exits_one_and_lists_missing_differing_and_extra_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
```

## test_cli_check_with_no_output_directory_lists_every_file_missing

> `--check` before any generation lists every rendered file as missing.

```python
def test_cli_check_with_no_output_directory_lists_every_file_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
```

## test_cli_without_sources_exits_two_with_a_usage_message

> No sources from the CLI or config exits 2 with a usage message.

```python
def test_cli_without_sources_exits_two_with_a_usage_message(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
```

## test_cli_invalid_config_exits_two_naming_the_offense

> A config that fails to load exits 2 with the error on stderr.

```python
def test_cli_invalid_config_exits_two_naming_the_offense(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
```

## test_cli_wrongly_typed_config_value_exits_two_naming_the_key

> A wrongly typed config value exits 2 naming the key.

```python
def test_cli_wrongly_typed_config_value_exits_two_naming_the_key(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
```

## test_cli_usage_errors_exit_two_for_bad_flag_values

> A non-integer or non-positive depth value exits 2 as a usage error.

```python
def test_cli_usage_errors_exit_two_for_bad_flag_values(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
```

## test_cli_missing_root_exits_two_with_the_exception_message

> A missing collection root exits 2 with the error on stderr.

```python
def test_cli_missing_root_exits_two_with_the_exception_message(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
```

## test_cli_parse_error_exits_two_with_the_exception_message

> A source file with a syntax error exits 2 with the error on stderr.

```python
def test_cli_parse_error_exits_two_with_the_exception_message(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
```

## test_cli_generation_error_exits_two_with_the_exception_message

> A filesystem error from generation exits 2 with the error on stderr.

```python
def test_cli_generation_error_exits_two_with_the_exception_message(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
```

## test_cli_filesystem_error_during_check_exits_two

> A filesystem error while checking exits 2 with the error on stderr.

```python
def test_cli_filesystem_error_during_check_exits_two(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
```
