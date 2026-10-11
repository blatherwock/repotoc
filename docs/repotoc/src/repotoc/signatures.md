# src/repotoc/signatures.py

> Normalized source form of function and class definition lines.

## signature

> Return the normalized source form of a definition line.

```python
def signature(node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) -> str:
```
