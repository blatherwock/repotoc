"""Model builders shared by the rendering tests."""

from repotoc.models import Class, Function, Module


def function(
    name: str,
    docstring: str | None = "Doc.",
    decorators: list[str] | None = None,
) -> Function:
    """Build a function model with the given name."""
    return Function(
        name=name,
        signature=f"def {name}():",
        docstring=docstring,
        decorators=decorators or [],
    )


def klass(
    name: str,
    members: list[Function | Class] | None = None,
    docstring: str | None = "Class doc.",
    decorators: list[str] | None = None,
) -> Class:
    """Build a class model with the given name."""
    return Class(
        name=name,
        signature=f"class {name}:",
        docstring=docstring,
        decorators=decorators or [],
        members=members or [],
    )


def module(
    source_path: str,
    docstring: str | None = None,
    members: list[Function | Class] | None = None,
) -> Module:
    """Build a module model with the given source path."""
    return Module(source_path=source_path, docstring=docstring, members=members or [])
