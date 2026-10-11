# src/repotoc/render/paths.py

> Doc paths, source links, and directory chains for the artifact layout.

## is_init

> Return whether the source path is a package `__init__.py` file.

```python
def is_init(source_path: str) -> bool:
```

## doc_path

> Return the output doc path mirroring the source path.

```python
def doc_path(source_path: str) -> str:
```

## index_path

> Return the index path inside the output directory.

```python
def index_path(directory: str) -> str:
```

## parent

> Return the path's parent directory; `.` for a top-level path.

```python
def parent(path: str) -> str:
```

## directory_chain

> Return the directory and every ancestor directory, including the root.

```python
def directory_chain(directory: str) -> set[str]:
```

## within_output

> Return the path relative to the directory, both inside the output tree.

```python
def within_output(path: str, directory: str) -> str:
```

## source_link

> Return the filesystem-relative link from the base directory to the target.

```python
def source_link(base: str, target: str) -> str:
```
