"""Board scoring for evaluating checkers positions."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..board import Board

_KING_BONUS = 2
_BACK_ROW_BONUS = 1


def material(board: "Board", side: str) -> int:
    """Score a board by piece counts from one side's view."""
    other = "light" if side == "dark" else "dark"
    return board.count(side) - board.count(other)


def positional(board: "Board", side: str) -> int:
    total = material(board, side)
    for square, piece in board.pieces.items():
        if piece == side and square[1] in ("1", "8"):
            total += _BACK_ROW_BONUS
    return total
