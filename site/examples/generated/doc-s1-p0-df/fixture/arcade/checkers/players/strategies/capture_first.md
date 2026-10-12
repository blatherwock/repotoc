# `fixture/arcade/checkers/players/strategies/capture_first.py`

> A greedy player that always plays the first available capture.

## `class CaptureFirstPlayer:`

### `def __init__(self, side: str) -> None:`

> Bind the player to one side.

### `def choose(self, board: Board) -> 'Move | None':`

> Return the first capture, else the first quiet move.
