"""Error types raised by the collection layer."""


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
