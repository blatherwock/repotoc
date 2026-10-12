# `src/repotoc/models.py`

> Model dataclasses for collected modules, classes, and functions.

## `class Function:`

> A collected function or method definition.
>
> Attributes:
>     name: The function name as written in source.
>     signature: The normalized source form of the definition line.
>     docstring: The dedented docstring, stripped of surrounding whitespace, or None
>         when the function has none.
>     decorators: The decorator expressions as written, in source order.

---

## `class Class:`

> A collected class definition.
>
> Attributes:
>     name: The class name as written in source.
>     signature: The normalized source form of the definition line.
>     docstring: The dedented docstring, stripped of surrounding whitespace, or None
>         when the class has none.
>     decorators: The decorator expressions as written, in source order.
>     members: The classes and functions defined in the class body, in source order.

---

## `class Module:`

> A collected module.
>
> Attributes:
>     source_path: The path to the source file.
>     docstring: The dedented module docstring, stripped of surrounding whitespace, or
>         None when the module has none.
>     members: The classes and functions defined at module level, in source order.
