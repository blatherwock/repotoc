import random
from typing import TYPE_CHECKING

from ...board import Board
from ...rules import legal_moves

if TYPE_CHECKING:
    from ....game import Move


class RandomMovePlayer:
    """A player that picks uniformly among the legal moves."""

    def __init__(self, side: str) -> None:
        """Bind the player to one side."""
        self.side = side

    def choose(self, board: Board) -> "Move | None":
        """Return a uniformly random legal move, None if stuck."""
        moves = legal_moves(board, self.side)
        return random.choice(moves) if moves else None
