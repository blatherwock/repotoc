# src/repotoc/errors.py

> Error types raised by the config, collection, and generation layers.

## ConfigError

> Raised when the config is invalid.
>
> Attributes:
>     key: The offending config key, or the path of the offending file.
>     message: The problem with the key's value.

```python
class ConfigError(Exception):
```

### __init__

> Initialize the error with the offending key and message.

```python
    def __init__(self, key: str, message: str) -> None:
```

## CollectionError

> Base error for collection failures.

```python
class CollectionError(Exception):
```

## ParseError

> Raised when a source file cannot be parsed.
>
> Attributes:
>     path: The path to the unparseable source file.
>     message: The parser message.

```python
class ParseError(CollectionError):
```

### __init__

> Initialize the error with the offending path and parser message.

```python
    def __init__(self, path: str, message: str) -> None:
```

## MissingRootError

> Raised when a collection root does not exist.
>
> Attributes:
>     root: The missing root path.

```python
class MissingRootError(CollectionError):
```

### __init__

> Initialize the error with the missing root.

```python
    def __init__(self, root: str) -> None:
```

## GenerationError

> Raised when the output directory cannot be created, written, or pruned.
>
> Attributes:
>     path: The path of the offending file or directory.
>     message: The filesystem's message.

```python
class GenerationError(Exception):
```

### __init__

> Initialize the error with the offending path and message.

```python
    def __init__(self, path: str, message: str) -> None:
```
