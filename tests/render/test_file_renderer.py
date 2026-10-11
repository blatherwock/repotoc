"""Tests for doc file rendering."""

from __future__ import annotations

from typing import TYPE_CHECKING

from builders import function, klass, module

from repotoc.filters import Filters, RenderConfig
from repotoc.render import file_renderer

if TYPE_CHECKING:
    from repotoc.models import Class, Function, Module


def _render_doc(doc: Module, config: RenderConfig | None = None) -> str:
    """Render one module doc file with the given config, or the default one."""
    if config is None:
        config = RenderConfig(output="out")
    return file_renderer.render_doc(doc, Filters(config), config)


def test_has_doc_is_true_for_plain_modules() -> None:
    """Every module but `__init__.py` renders a doc file."""
    filters = Filters(RenderConfig(output="out"))

    assert file_renderer.has_doc(module("mod.py"), filters) is True


def test_has_doc_is_true_for_inits_with_visible_members() -> None:
    """An `__init__.py` with members renders a doc file."""
    filters = Filters(RenderConfig(output="out"))
    init = module("pkg/__init__.py", members=[function("run")])

    assert file_renderer.has_doc(init, filters) is True


def test_has_doc_is_false_for_memberless_inits() -> None:
    """A docstring-only `__init__.py` renders no doc file."""
    filters = Filters(RenderConfig(output="out"))
    init = module("pkg/__init__.py", docstring="Package doc.")

    assert file_renderer.has_doc(init, filters) is False


def test_has_doc_uses_the_privates_flag_for_private_only_inits() -> None:
    """A private-only `__init__.py` emits only with the private flag."""
    init = module("pkg/__init__.py", members=[function("_helper")])

    assert file_renderer.has_doc(init, Filters(RenderConfig(output="out"))) is False
    config = RenderConfig(output="out", file_include_privates=True)
    assert file_renderer.has_doc(init, Filters(config)) is True


def test_doc_file_states_the_source_path() -> None:
    """The doc file opens with a heading carrying the source path."""
    assert _render_doc(module("src/pkg/mod.py")).startswith("# src/pkg/mod.py\n")


def test_doc_file_renders_the_module_docstring_in_full() -> None:
    """The module docstring renders in full as a blockquote."""
    doc = module("mod.py", docstring="First.\n\nSecond.")

    assert "# mod.py\n\n> First.\n>\n> Second.\n" in _render_doc(doc)


def test_members_render_in_model_order() -> None:
    """Members render in the order the model lists them."""
    members = [function("first"), klass("Second"), function("third")]
    text = _render_doc(module("mod.py", members=members))

    assert text.index("def first():") < text.index("class Second:")
    assert text.index("class Second:") < text.index("def third():")


def test_decorators_render_above_the_signature_in_source_order() -> None:
    """Decorator lines sit above the signature line inside the code block."""
    run = function("run", decorators=["functools.cache", "staticmethod"])
    text = _render_doc(module("mod.py", members=[run]))

    assert "```python\n@functools.cache\n@staticmethod\ndef run():\n```" in text


def test_undocumented_members_render_as_bare_signature_blocks() -> None:
    """A member without a docstring renders its heading and source block only."""
    text = _render_doc(module("mod.py", members=[function("run", docstring=None)]))

    assert text == "# mod.py\n\n## run\n\n```python\ndef run():\n```\n"


def test_docstring_renders_as_a_blockquote_above_the_src_block() -> None:
    """A member's section is heading, docstring blockquote, then source block."""
    text = _render_doc(module("mod.py", members=[function("run")]))

    assert text == "# mod.py\n\n## run\n\n> Doc.\n\n```python\ndef run():\n```\n"


def test_visibility_filter_applies_during_rendering() -> None:
    """Private members are omitted and constructors render by default."""
    members = [
        function("public"),
        function("_hidden"),
        klass("Thing", members=[function("__init__"), function("_secret")]),
    ]
    text = _render_doc(module("mod.py", members=members))

    assert "def public():" in text
    assert "_hidden" not in text
    assert "def __init__():" in text
    assert "_secret" not in text


def test_file_include_privates_renders_private_members() -> None:
    """With the private flag, underscore-prefixed members render too."""
    config = RenderConfig(output="out", file_include_privates=True)
    text = _render_doc(module("mod.py", members=[function("_helper")]), config)

    assert "def _helper():" in text


def test_nested_members_render_under_deeper_headings() -> None:
    """Class members render after their class, one heading level deeper."""
    thing = klass("Thing", members=[function("method")])
    text = _render_doc(module("mod.py", members=[thing]))

    assert text == (
        "# mod.py\n"
        "\n"
        "## Thing\n"
        "\n"
        "> Class doc.\n"
        "\n"
        "```python\n"
        "class Thing:\n"
        "```\n"
        "\n"
        "### method\n"
        "\n"
        "> Doc.\n"
        "\n"
        "```python\n"
        "    def method():\n"
        "```\n"
    )


def test_heading_level_mirrors_nesting_depth() -> None:
    """Members of a nested class render one heading level deeper still."""
    inner = klass("Inner", members=[function("inner_method")])
    thing = klass("Thing", members=[function("method"), inner])
    text = _render_doc(module("mod.py", members=[thing]))

    assert "## Thing\n" in text
    assert "### method\n" in text
    assert "### Inner\n" in text
    assert "#### inner_method\n" in text


def test_heading_level_bottoms_out_at_h6() -> None:
    """Members beyond H6 depth reuse H6 rather than growing further."""
    leaf: Function | Class = function("leaf", docstring=None)
    for name in ("L6", "L5", "L4", "L3", "L2", "L1"):
        leaf = klass(name, members=[leaf])
    text = _render_doc(module("mod.py", members=[leaf]))

    assert "###### L6\n" in text
    assert "###### leaf\n" in text
    assert "#######" not in text


def test_member_depth_one_renders_module_level_members_only() -> None:
    """Depth one renders classes without their bodies."""
    config = RenderConfig(output="out", file_member_depth=1)
    thing = klass("Thing", members=[function("method")])
    text = _render_doc(module("mod.py", members=[thing]), config)

    assert "## Thing\n" in text
    assert "### method" not in text
    assert "def method():" not in text


def test_member_depth_caps_nested_members_entirely() -> None:
    """Members below the cap render nowhere, nested members included."""
    config = RenderConfig(output="out", file_member_depth=2)
    inner = klass("Inner", members=[function("deep")])
    thing = klass("Thing", members=[function("method"), inner])
    text = _render_doc(module("mod.py", members=[thing]), config)

    assert "### method\n" in text
    assert "### Inner\n" in text
    assert "#### deep" not in text
    assert "def deep():" not in text


def test_signatures_off_renders_headings_and_docstrings_only() -> None:
    """Without signatures, documented members render heading and docstring."""
    config = RenderConfig(output="out", file_include_signatures=False)
    members: list[Function | Class] = [
        function("run"),
        function("bare", docstring=None),
    ]
    text = _render_doc(module("mod.py", members=members), config)

    assert text == "# mod.py\n\n## run\n\n> Doc.\n\n## bare\n"


def test_docstring_passes_through_unchanged_inside_the_blockquote() -> None:
    """Markdown constructs and backticks in a docstring are not transformed."""
    run = function("run", docstring="Use `run`.\n\nNot *italics*.")
    text = _render_doc(module("mod.py", members=[run]))

    assert "> Use `run`.\n>\n> Not *italics*." in text


def test_fence_extends_past_backtick_runs_in_the_src_block() -> None:
    """The source fence grows beyond the longest backtick run in the text."""
    run = function("run", decorators=['tag("```code```")'])
    text = _render_doc(module("mod.py", members=[run]))

    assert '````python\n@tag("```code```")\ndef run():\n````' in text


def test_fence_extends_past_the_longest_of_several_runs() -> None:
    """The fence exceeds the longest backtick run, not just any run."""
    run = function("run", decorators=['tag("`tick` ``double``")'])
    text = _render_doc(module("mod.py", members=[run]))

    assert '```python\n@tag("`tick` ``double``")\ndef run():\n```' in text
