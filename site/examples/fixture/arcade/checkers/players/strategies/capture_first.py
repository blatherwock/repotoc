"""A greedy player that always plays the first available capture."""

from typing import TYPE_CHECKING

from ...board import Board
from ...rules import legal_moves

if TYPE_CHECKING:
    from ....game import Move


class CaptureFirstPlayer:
    def __init__(self, side: str) -> None:
        """Bind the player to one side."""
        self.side = side

    def choose(self, board: Board) -> "Move | None":
        """Return the first capture, else the first quiet move."""
        moves = legal_moves(board, self.side)
        captures = [move for move in moves if move.captures]
        if captures:
            return captures[0]
        return moves[0] if moves else None
