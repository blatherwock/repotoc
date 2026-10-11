# tests/test_generate.py

> Tests for generating the artifact into the output directory.

## test_generation_writes_the_file_set_creating_the_output_directory

> Generation creates the missing output directory and writes every file.

```python
def test_generation_writes_the_file_set_creating_the_output_directory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
```

## test_generation_prunes_stale_markdown_and_keeps_other_files

> Generation deletes unproduced .md files and leaves other suffixes.

```python
def test_generation_prunes_stale_markdown_and_keeps_other_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
```

## test_generation_without_modules_writes_only_the_output_directory

> An empty module set writes nothing and prunes every .md file.

```python
def test_generation_without_modules_writes_only_the_output_directory(tmp_path: Path) -> None:
```

## test_generation_is_idempotent

> A second run writes the same set and deletes nothing.

```python
def test_generation_is_idempotent(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
```

## test_generation_fails_when_the_output_path_is_a_file

> A file where the output directory belongs fails naming the path.

```python
def test_generation_fails_when_the_output_path_is_a_file(tmp_path: Path) -> None:
```

## test_generation_fails_when_a_doc_path_is_a_directory

> A directory where a doc file belongs fails naming the path.

```python
def test_generation_fails_when_a_doc_path_is_a_directory(tmp_path: Path) -> None:
```

## test_generation_fails_when_a_stale_markdown_path_is_a_directory

> A directory squatting on a stale .md path fails naming the path.

```python
def test_generation_fails_when_a_stale_markdown_path_is_a_directory(tmp_path: Path) -> None:
```
