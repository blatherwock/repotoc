"""A minimax player that searches a few plies deep.

The search alternates sides ply by ply and scores leaves with the
positional heuristic. Nothing is pruned; checkers trees stay small
enough for a demo.
"""

from typing import TYPE_CHECKING

from ..board import Board
from ..rules import legal_moves
from .heuristic import material, positional

if TYPE_CHECKING:
    from ...game import Move

_MAX_DEPTH = 4


class MinimaxPlayer:
    """A player choosing moves by minimax over a board heuristic.

    Attributes:
        side: The side this player moves for.
        depth: The search depth in plies.
    """

    def __init__(self, side: str, depth: int = _MAX_DEPTH) -> None:
        self.side = side
        self.depth = depth

    def choose(self, board: Board) -> "Move | None":
        """Return the move with the best minimax score, None if stuck."""
        best = None
        best_score = -999
        for move in legal_moves(board, self.side):
            score = self._search(_played(board, move), 1)
            if score > best_score:
                best_score = score
                best = move
        return best

    def _search(self, board: Board, ply: int) -> int:
        """Score a position recursively; higher is better for our side."""
        if ply >= self.depth:
            return positional(board, self.side)
        side = self.side if ply % 2 == 0 else _opponent(self.side)
        scores = [
            self._search(_played(board, move), ply + 1)
            for move in legal_moves(board, side)
        ]
        if not scores:
            return material(board, self.side)
        if ply % 2 == 0:
            return max(scores)
        return min(scores)


def _played(board: Board, move: "Move") -> Board:
    """Return a copy of the board with the move applied."""
    worked = Board(dict(board.pieces))
    worked.apply(move)
    return worked


def _opponent(side: str) -> str:
    """Return the other side's name."""
    return "light" if side == "dark" else "dark"
