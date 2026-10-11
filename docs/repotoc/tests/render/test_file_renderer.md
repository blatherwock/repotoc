# tests/render/test_file_renderer.py

> Tests for doc file rendering.

## test_has_doc_is_true_for_plain_modules

> Every module but `__init__.py` renders a doc file.

```python
def test_has_doc_is_true_for_plain_modules() -> None:
```

## test_has_doc_is_true_for_inits_with_visible_members

> An `__init__.py` with members renders a doc file.

```python
def test_has_doc_is_true_for_inits_with_visible_members() -> None:
```

## test_has_doc_is_false_for_memberless_inits

> A docstring-only `__init__.py` renders no doc file.

```python
def test_has_doc_is_false_for_memberless_inits() -> None:
```

## test_has_doc_uses_the_privates_flag_for_private_only_inits

> A private-only `__init__.py` emits only with the private flag.

```python
def test_has_doc_uses_the_privates_flag_for_private_only_inits() -> None:
```

## test_doc_file_states_the_source_path

> The doc file opens with a heading carrying the source path.

```python
def test_doc_file_states_the_source_path() -> None:
```

## test_doc_file_renders_the_module_docstring_in_full

> The module docstring renders in full as a blockquote.

```python
def test_doc_file_renders_the_module_docstring_in_full() -> None:
```

## test_members_render_in_model_order

> Members render in the order the model lists them.

```python
def test_members_render_in_model_order() -> None:
```

## test_decorators_render_above_the_signature_in_source_order

> Decorator lines sit above the signature line inside the code block.

```python
def test_decorators_render_above_the_signature_in_source_order() -> None:
```

## test_undocumented_members_render_as_bare_signature_blocks

> A member without a docstring renders its heading and source block only.

```python
def test_undocumented_members_render_as_bare_signature_blocks() -> None:
```

## test_docstring_renders_as_a_blockquote_above_the_src_block

> A member's section is heading, docstring blockquote, then source block.

```python
def test_docstring_renders_as_a_blockquote_above_the_src_block() -> None:
```

## test_visibility_filter_applies_during_rendering

> Private members are omitted and constructors render by default.

```python
def test_visibility_filter_applies_during_rendering() -> None:
```

## test_file_include_privates_renders_private_members

> With the private flag, underscore-prefixed members render too.

```python
def test_file_include_privates_renders_private_members() -> None:
```

## test_nested_members_render_under_deeper_headings

> Class members render after their class, one heading level deeper.

```python
def test_nested_members_render_under_deeper_headings() -> None:
```

## test_heading_level_mirrors_nesting_depth

> Members of a nested class render one heading level deeper still.

```python
def test_heading_level_mirrors_nesting_depth() -> None:
```

## test_heading_level_bottoms_out_at_h6

> Members beyond H6 depth reuse H6 rather than growing further.

```python
def test_heading_level_bottoms_out_at_h6() -> None:
```

## test_member_depth_one_renders_module_level_members_only

> Depth one renders classes without their bodies.

```python
def test_member_depth_one_renders_module_level_members_only() -> None:
```

## test_member_depth_caps_nested_members_entirely

> Members below the cap render nowhere, nested members included.

```python
def test_member_depth_caps_nested_members_entirely() -> None:
```

## test_signatures_off_renders_headings_and_docstrings_only

> Without signatures, documented members render heading and docstring.

```python
def test_signatures_off_renders_headings_and_docstrings_only() -> None:
```

## test_docstring_passes_through_unchanged_inside_the_blockquote

> Markdown constructs and backticks in a docstring are not transformed.

```python
def test_docstring_passes_through_unchanged_inside_the_blockquote() -> None:
```

## test_fence_extends_past_backtick_runs_in_the_src_block

> The source fence grows beyond the longest backtick run in the text.

```python
def test_fence_extends_past_backtick_runs_in_the_src_block() -> None:
```

## test_fence_extends_past_the_longest_of_several_runs

> The fence exceeds the longest backtick run, not just any run.

```python
def test_fence_extends_past_the_longest_of_several_runs() -> None:
```
