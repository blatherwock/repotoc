"""Model dataclasses for collected modules, classes, and functions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Function:
    """A collected function or method definition.

    Attributes:
        name: The function name as written in source.
        signature: The normalized source form of the definition line.
        docstring: The dedented docstring, stripped of surrounding whitespace, or None
            when the function has none.
        decorators: The decorator expressions as written, in source order.
    """

    name: str
    signature: str
    docstring: str | None
    decorators: list[str]


@dataclass(frozen=True)
class Class:
    """A collected class definition.

    Attributes:
        name: The class name as written in source.
        signature: The normalized source form of the definition line.
        docstring: The dedented docstring, stripped of surrounding whitespace, or None
            when the class has none.
        decorators: The decorator expressions as written, in source order.
        members: The classes and functions defined in the class body, in source order.
    """

    name: str
    signature: str
    docstring: str | None
    decorators: list[str]
    members: list[Function | Class]


@dataclass(frozen=True)
class Module:
    """A collected module.

    Attributes:
        source_path: The path to the source file.
        docstring: The dedented module docstring, stripped of surrounding whitespace, or
            None when the module has none.
        members: The classes and functions defined at module level, in source order.
    """

    source_path: str
    docstring: str | None
    members: list[Function | Class]
