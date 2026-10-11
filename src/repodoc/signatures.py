"""Normalized source form of function and class definition lines."""

import ast
import copy
import sys

# Prefixes that a normalized definition line starts with.
_DEFINITION_PREFIXES = ("def ", "async def ", "class ")


def signature(
    node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef,
) -> str:
    """Return the normalized source form of a definition line."""
    text = _unparse_definition(node)
    if text is not None:
        return text
    return _reconstruct_signature(node)


def _unparse_definition(
    node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef,
) -> str | None:
    """Unparse a definition without its body or decorators, or None if malformed."""
    clone = copy.copy(node)
    clone.body = []
    clone.decorator_list = []
    text = ast.unparse(clone)
    if text.startswith(_DEFINITION_PREFIXES):
        return text
    return None


def _reconstruct_signature(
    node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef,
) -> str:
    """Build a definition line from its argument and base nodes."""
    type_params = _format_type_params(node)
    if isinstance(node, ast.ClassDef):
        arguments = [ast.unparse(base) for base in node.bases]
        arguments.extend(ast.unparse(keyword) for keyword in node.keywords)
        head = f"class {node.name}{type_params}"
        if arguments:
            head = f"{head}({', '.join(arguments)})"
        return f"{head}:"
    head = f"def {node.name}{type_params}({ast.unparse(node.args)})"
    if node.returns is not None:
        head = f"{head} -> {ast.unparse(node.returns)}"
    if isinstance(node, ast.AsyncFunctionDef):
        head = f"async {head}"
    return f"{head}:"


def _format_type_params(
    node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef,
) -> str:
    """Return PEP 695 type parameters as a source string, or empty when absent.

    The `type_params` attribute exists from Python 3.12; on 3.11 no node
    carries type parameters.
    """
    if sys.version_info < (3, 12):  # pragma: no cover
        return ""
    if node.type_params:
        return f"[{', '.join(ast.unparse(param) for param in node.type_params)}]"
    return ""
