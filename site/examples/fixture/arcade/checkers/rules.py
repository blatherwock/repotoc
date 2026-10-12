"""Checkers move generation: forced captures and quiet moves.

The rules are pure functions: they read a board and produce moves, and
never mutate the positions they are given.
"""

from ..game import Move
from .board import Board

_FILES = "abcdefgh"
_RANKS = "12345678"
_DIAGONALS = ((1, 1), (1, -1), (-1, 1), (-1, -1))


def legal_moves(board: Board, side: str) -> list[Move]:
    """Return every move the rules allow the side to play.

    When any capture exists the rules force it: quiet moves are
    dropped from the result.
    """
    captures = _captures(board, side)
    if captures:
        return captures
    return _quiet_moves(board, side)


def is_capture(move: Move) -> bool:
    """Return whether a move removes any pieces."""
    return bool(move.captures)


def describe(move: Move, *, verbose: bool = False) -> str:
    """Render a move as notation, like `c3xd4` for captures.

    Args:
        move: The move to render.
        verbose: When set, also name every captured square.
    """
    if move.captures:
        text = f"{move.origin}x{move.target}"
    else:
        text = f"{move.origin}-{move.target}"
    if verbose and move.captures:
        text = f"{text} ({', '.join(move.captures)})"
    return text


def _captures(board: Board, side: str) -> list[Move]:
    """Return the single-jump captures available to the side."""
    moves = []
    for origin, piece in board.pieces.items():
        if piece != side:
            continue
        for file_step, rank_step in _DIAGONALS:
            over = _shift(origin, file_step, rank_step)
            landing = _shift(origin, 2 * file_step, 2 * rank_step)
            if over is None or landing is None:
                continue
            enemy = board.piece_at(over)
            if enemy and enemy != side and board.piece_at(landing) is None:
                moves.append(Move(origin, landing, (over,)))
    return moves


def _quiet_moves(board: Board, side: str) -> list[Move]:
    """Return the diagonal steps to empty neighboring squares."""
    moves = []
    for origin, piece in board.pieces.items():
        if piece != side:
            continue
        for file_step, rank_step in _DIAGONALS:
            target = _shift(origin, file_step, rank_step)
            if target is not None and board.piece_at(target) is None:
                moves.append(Move(origin, target))
    return moves


def _shift(square: str, file_step: int, rank_step: int) -> str | None:
    """Move a square name by offsets, or None if off the board."""
    file = ord(square[0]) - ord("a") + file_step
    rank = int(square[1]) + rank_step
    if 0 <= file < len(_FILES) and 1 <= rank <= len(_RANKS):
        return f"{chr(file + ord('a'))}{rank}"
    return None
