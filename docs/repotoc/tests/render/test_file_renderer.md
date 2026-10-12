# `tests/render/test_file_renderer.py`

> Tests for doc file rendering.

## `def test_has_doc_is_true_for_plain_modules() -> None:`

> Every module but `__init__.py` renders a doc file.

---

## `def test_has_doc_is_true_for_inits_with_visible_members() -> None:`

> An `__init__.py` with members renders a doc file.

---

## `def test_has_doc_is_false_for_memberless_inits() -> None:`

> A docstring-only `__init__.py` renders no doc file.

---

## `def test_has_doc_uses_the_privates_flag_for_private_only_inits() -> None:`

> A private-only `__init__.py` emits only with the private flag.

---

## `def test_doc_file_states_the_source_path() -> None:`

> The doc file opens with a monospaced heading carrying the source path.

---

## `def test_doc_file_renders_the_module_docstring_in_full() -> None:`

> The module docstring renders in full as a blockquote.

---

## `def test_members_render_in_model_order() -> None:`

> Members render in the order the model lists them.

---

## `def test_decorators_do_not_render() -> None:`

> Decorator expressions appear nowhere in the rendered doc file.

---

## `def test_undocumented_members_render_as_a_bare_heading() -> None:`

> A member without a docstring renders its heading alone.

---

## `def test_docstring_renders_as_a_blockquote_under_the_heading() -> None:`

> A member's section is its signature heading, then its docstring.

---

## `def test_visibility_filter_applies_during_rendering() -> None:`

> Private members are omitted and constructors render by default.

---

## `def test_file_include_privates_renders_private_members() -> None:`

> With the private flag, underscore-prefixed members render too.

---

## `def test_nested_members_render_under_deeper_headings() -> None:`

> Class members render after their class, one heading level deeper.

---

## `def test_heading_level_mirrors_nesting_depth() -> None:`

> Members of a nested class render one heading level deeper still.

---

## `def test_heading_level_bottoms_out_at_h6() -> None:`

> Members beyond H6 depth reuse H6 rather than growing further.

---

## `def test_member_depth_one_renders_module_level_members_only() -> None:`

> Depth one renders classes without their bodies.

---

## `def test_member_depth_caps_nested_members_entirely() -> None:`

> Members below the cap render nowhere, nested members included.

---

## `def test_signatures_off_collapses_empty_argument_lists() -> None:`

> Without signatures, an empty argument list renders as `()`.

---

## `def test_thematic_breaks_separate_top_level_members() -> None:`

> A break sits between top-level members, not after the last or inside.

---

## `def test_a_single_member_renders_no_thematic_break() -> None:`

> With one top-level member no thematic break renders at all.

---

## `def test_signatures_off_collapses_arguments_into_an_ellipsis() -> None:`

> Without signatures, a populated argument list renders as `(...)`.
>
> A hidden signature must not suggest an arity, so nested parentheses in
> defaults collapse the same as plain arguments; the return annotation
> renders only with signatures on.

---

## `def test_signatures_off_collapses_class_bases_into_an_ellipsis() -> None:`

> Without signatures, class bases render as `(...)` in the heading.

---

## `def test_docstring_passes_through_unchanged_inside_the_blockquote() -> None:`

> Markdown constructs and backticks in a docstring are not transformed.
