# `fixture/arcade/checkers/players/strategies/random_move.py`

## `class RandomMovePlayer:`

> A player that picks uniformly among the legal moves.

### `def __init__(self, side: str) -> None:`

> Bind the player to one side.

### `def choose(self, board: Board) -> 'Move | None':`

> Return a uniformly random legal move, None if stuck.
