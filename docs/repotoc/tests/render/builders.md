# tests/render/builders.py

> Model builders shared by the rendering tests.

## function

> Build a function model with the given name.

```python
def function(name: str, docstring: str | None='Doc.', decorators: list[str] | None=None) -> Function:
```

## klass

> Build a class model with the given name.

```python
def klass(name: str, members: list[Function | Class] | None=None, docstring: str | None='Class doc.', decorators: list[str] | None=None) -> Class:
```

## module

> Build a module model with the given source path.

```python
def module(source_path: str, docstring: str | None=None, members: list[Function | Class] | None=None) -> Module:
```
