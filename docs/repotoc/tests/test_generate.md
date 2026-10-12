# `tests/test_generate.py`

> Tests for generating the artifact into the output directory.

## `def test_generation_writes_the_file_set_creating_the_output_directory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:`

> Generation creates the missing output directory and writes every file.

---

## `def test_generation_prunes_stale_markdown_and_keeps_other_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:`

> Generation deletes unproduced .md files and leaves other suffixes.

---

## `def test_generation_without_modules_writes_only_the_output_directory(tmp_path: Path) -> None:`

> An empty module set writes nothing and prunes every .md file.

---

## `def test_generation_is_idempotent(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:`

> A second run writes the same set and deletes nothing.

---

## `def test_generation_fails_when_the_output_path_is_a_file(tmp_path: Path) -> None:`

> A file where the output directory belongs fails naming the path.

---

## `def test_generation_fails_when_a_doc_path_is_a_directory(tmp_path: Path) -> None:`

> A directory where a doc file belongs fails naming the path.

---

## `def test_generation_fails_when_a_stale_markdown_path_is_a_directory(tmp_path: Path) -> None:`

> A directory squatting on a stale .md path fails naming the path.
