"""Error types raised by the config, collection, and generation layers."""


class ConfigError(Exception):
    """Raised when the config is invalid.

    Attributes:
        key: The offending config key, or the path of the offending file.
        message: The problem with the key's value.
    """

    def __init__(self, key: str, message: str) -> None:
        """Initialize the error with the offending key and message."""
        text = f"{key}: {message}"
        super().__init__(text)
        self.key = key
        self.message = message


class CollectionError(Exception):
    """Base error for collection failures."""


class ParseError(CollectionError):
    """Raised when a source file cannot be parsed.

    Attributes:
        path: The path to the unparseable source file.
        message: The parser message.
    """

    def __init__(self, path: str, message: str) -> None:
        """Initialize the error with the offending path and parser message."""
        text = f"{path}: {message}"
        super().__init__(text)
        self.path = path
        self.message = message


class MissingRootError(CollectionError):
    """Raised when a collection root does not exist.

    Attributes:
        root: The missing root path.
    """

    def __init__(self, root: str) -> None:
        """Initialize the error with the missing root."""
        text = f"collection root does not exist: {root}"
        super().__init__(text)
        self.root = root


class GenerationError(Exception):
    """Raised when the output directory cannot be created, written, or pruned.

    Attributes:
        path: The path of the offending file or directory.
        message: The filesystem's message.
    """

    def __init__(self, path: str, message: str) -> None:
        """Initialize the error with the offending path and message."""
        text = f"{path}: {message}"
        super().__init__(text)
        self.path = path
        self.message = message
