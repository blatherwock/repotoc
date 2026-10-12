"""Doc file rendering: module models into Markdown doc files."""

from __future__ import annotations

from typing import TYPE_CHECKING

from repotoc.models import Class, Function
from repotoc.render import markdown, paths

if TYPE_CHECKING:
    from repotoc.filters import Filters, RenderConfig
    from repotoc.models import Module

Member = Function | Class

# Deepest heading Markdown defines; members at deeper nesting reuse it.
_MAX_HEADING = 6


def has_doc(module: Module, filters: Filters) -> bool:
    """Return whether the module renders a doc file.

    Every module renders one except `__init__.py` without visible members: a
    docstring-only or import-only package file surfaces its docstring in the
    indexes instead, and definitions are what make a doc file worthwhile. The
    criterion is visible members, so `file_include_privates` decides whether a
    private-only `__init__.py` emits.
    """
    if not paths.is_init(module.source_path):
        return True
    return bool(filters.visible_members(module.members))


def render_doc(module: Module, filters: Filters, config: RenderConfig) -> str:
    """Render one module model into its doc file text.

    The doc file states the source path as a monospaced heading, renders the
    module docstring in full as a blockquote, then outlines the visible
    members in model order, a thematic break between top-level members.
    """
    sections = [markdown.heading(f"`{module.source_path}`", 1)]
    if module.docstring is not None:
        sections.append(markdown.blockquote(module.docstring))
    for index, member in enumerate(filters.visible_members(module.members)):
        if index:
            sections.append(markdown.horizontal_rule())
        sections += _member_sections(member, config, 0)
    return "\n\n".join(sections) + "\n"


def _member_sections(member: Member, config: RenderConfig, classes: int) -> list[str]:
    """Render one member and its nested members as sections of a doc file.

    A section is a heading naming the member, its docstring as a blockquote,
    and nothing else. With `file_include_signatures` the heading carries the
    member's full signature line, `def`/`class` prefix included; without it,
    the prefix, the name, and a collapsed argument list: `()` when the member
    takes no arguments, `(...)` when it does, none when a class declares no
    bases. The heading level grows with the number of enclosing classes,
    clamped at H6. `file_member_depth` caps the outline: a member below the
    cap renders nowhere, its nested members included. Members arrive already
    filtered; rendering applies no visibility logic.
    """
    depth = config.file_member_depth
    if depth is not None and classes + 1 > depth:
        return []
    sections = [
        markdown.heading(_member_heading(member, config), _heading_level(classes))
    ]
    if member.docstring is not None:
        sections.append(markdown.blockquote(member.docstring))
    if isinstance(member, Class):
        for child in member.members:
            sections += _member_sections(child, config, classes + 1)
    return sections


def _heading_level(classes: int) -> int:
    """Return the heading level mirroring the member's nesting depth.

    Module-level members render H2, one step past the module's H1; each
    enclosing class adds one level, clamped at H6.
    """
    return min(classes + 2, _MAX_HEADING)


def _member_heading(member: Member, config: RenderConfig) -> str:
    """Return the member's monospaced heading text.

    Signatures on, the text is the normalized signature line as collected;
    signatures off, it is the line with its argument list collapsed: `()`
    when empty, `(...)` when arguments or bases exist, the bare head and
    colon when a class declares neither, so a hidden signature never
    suggests an arity.
    """
    if config.file_include_signatures:
        return f"`{member.signature}`"
    return f"`{_short_signature(member.signature)}`"


def _short_signature(signature: str) -> str:
    """Return the definition line with its argument list collapsed.

    The head keeps the `def`/`class` prefix and the name; the argument list
    becomes `()` when empty or `(...)` otherwise, and the line closes with
    the colon alone: the return annotation, like the rest of the signature
    detail, renders only with signatures on. A class without bases has no
    parenthesis pair and keeps its whole line.
    """
    open_index = signature.find("(")
    if open_index == -1:
        return signature
    parens = "()" if signature[open_index + 1] == ")" else "(...)"
    return signature[:open_index] + parens + ":"
