"""Doc file rendering: module models into Markdown doc files."""

from __future__ import annotations

from typing import TYPE_CHECKING

from repodoc.models import Class, Function
from repodoc.render import markdown, paths

if TYPE_CHECKING:
    from repodoc.filters import Filters, RenderConfig
    from repodoc.models import Module

Member = Function | Class

# Indentation step mirroring one class-nesting level inside a code block.
_INDENT = "    "

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

    The doc file states the source path as a heading, renders the module
    docstring in full as a blockquote, then outlines the visible members in
    model order.
    """
    sections = [markdown.heading(module.source_path, 1)]
    if module.docstring is not None:
        sections.append(markdown.blockquote(module.docstring))
    for member in filters.visible_members(module.members):
        sections += _member_sections(member, config, 0)
    return "\n\n".join(sections) + "\n"


def _member_sections(member: Member, config: RenderConfig, classes: int) -> list[str]:
    """Render one member and its nested members as sections of a doc file.

    A section is a heading naming the member, its docstring as a blockquote,
    then its source as a fenced Python block when `file_include_signatures` is
    on. The heading level grows with the number of enclosing classes, clamped
    at H6; the source block carries one indentation step per level, mirroring
    the source. `file_member_depth` caps the outline: a member below the cap
    renders nowhere, its nested members included. Members arrive already
    filtered; rendering applies no visibility logic.
    """
    depth = config.file_member_depth
    if depth is not None and classes + 1 > depth:
        return []
    sections = [markdown.heading(member.name, _heading_level(classes))]
    if member.docstring is not None:
        sections.append(markdown.blockquote(member.docstring))
    if config.file_include_signatures:
        sections.append(markdown.code_block(_member_src(member, classes)))
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


def _member_src(member: Member, classes: int) -> str:
    """Return the member's source lines: decorators above the signature.

    The model stores decorator expressions without their `@` sigil; rendering
    restores it so the block shows the decorators as written in the source.
    """
    indent = _INDENT * classes
    code_lines = [f"{indent}@{decorator}" for decorator in member.decorators]
    code_lines.append(indent + member.signature)
    return "\n".join(code_lines)
