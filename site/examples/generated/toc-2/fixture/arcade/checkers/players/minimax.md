# `fixture/arcade/checkers/players/minimax.py`

> A minimax player that searches a few plies deep.
>
> The search alternates sides ply by ply and scores leaves with the
> positional heuristic. Nothing is pruned; checkers trees stay small
> enough for a demo.

## `class MinimaxPlayer:`

> A player choosing moves by minimax over a board heuristic.
>
> Attributes:
>     side: The side this player moves for.
>     depth: The search depth in plies.

### `def __init__(self, side: str, depth: int=_MAX_DEPTH) -> None:`

### `def choose(self, board: Board) -> 'Move | None':`

> Return the move with the best minimax score, None if stuck.
