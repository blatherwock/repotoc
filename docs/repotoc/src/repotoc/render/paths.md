# `src/repotoc/render/paths.py`

> Doc paths, source links, and directory chains for the artifact layout.

## `def is_init(source_path: str) -> bool:`

> Return whether the source path is a package `__init__.py` file.

---

## `def doc_path(source_path: str) -> str:`

> Return the output doc path mirroring the source path.

---

## `def index_path(directory: str) -> str:`

> Return the index path inside the output directory.

---

## `def parent(path: str) -> str:`

> Return the path's parent directory; `.` for a top-level path.

---

## `def directory_chain(directory: str) -> set[str]:`

> Return the directory and every ancestor directory, including the root.

---

## `def within_output(path: str, directory: str) -> str:`

> Return the path relative to the directory, both inside the output tree.

---

## `def source_link(base: str, target: str) -> str:`

> Return the filesystem-relative link from the base directory to the target.
