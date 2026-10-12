"""Game registry: names mapped to factory functions.

Registering a game makes it available to callers that only know its
name, without importing every game module up front.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from .game import Game

_factories: "dict[str, Callable[[], Game]]" = {}


def register(name: str, factory: "Callable[[], Game]") -> None:
    """Add a game factory under a name, replacing any earlier one."""
    _factories[name] = factory


def create(name: str) -> "Game":
    """Build a fresh instance of the named game.

    Raises:
        KeyError: No game was registered under the name.
    """
    if name not in _factories:
        message = f"no game registered under {name!r}"
        raise KeyError(message)
    return _factories[name]()


def known_games() -> list[str]:
    return sorted(_factories)
