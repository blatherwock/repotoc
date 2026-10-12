"""The checkers board: piece positions and the moves that change them."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..game import Move

_FILES = "abcdefgh"
_RANKS = "12345678"


def playable_squares() -> list[str]:
    """Return every square a piece can stand on, in reading order.

    Only the dark squares are playable in checkers: those where the
    file and rank counters have opposite parity.
    """
    return [
        f"{file}{rank}"
        for rank in _RANKS
        for file in _FILES
        if (ord(file) - ord("a") + int(rank)) % 2 == 1
    ]


class Board:
    """Piece positions for one game of checkers.

    Squares are named like `c3`, file letter then rank number. The
    `pieces` mapping holds one entry per occupied square.

    Attributes:
        pieces: The occupied squares mapped to their owning side.
    """

    def __init__(self, pieces: dict[str, str]) -> None:
        """Set the piece positions for both sides."""
        self.pieces = pieces

    @classmethod
    def opening(cls) -> "Board":
        """Build the standard opening position: dark low, light high."""
        dark_rows = {"1", "2", "3"}
        light_rows = {"6", "7", "8"}
        pieces = {}
        for square in playable_squares():
            if square[1] in dark_rows:
                pieces[square] = "dark"
            elif square[1] in light_rows:
                pieces[square] = "light"
        return cls(pieces)

    def piece_at(self, square: str) -> str | None:
        return self.pieces.get(square)

    def apply(self, move: "Move") -> None:
        """Update the board for one played move.

        The moving piece lands on the target square and every
        captured square is emptied.
        """
        piece = self.pieces.pop(move.origin)
        for square in move.captures:
            self.pieces.pop(square, None)
        self.pieces[move.target] = piece

    def count(self, side: str) -> int:
        """Count the pieces the given side still has on the board."""
        return sum(1 for piece in self.pieces.values() if piece == side)
