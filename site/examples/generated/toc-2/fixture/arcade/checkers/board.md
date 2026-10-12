# `fixture/arcade/checkers/board.py`

> The checkers board: piece positions and the moves that change them.

## `def playable_squares() -> list[str]:`

> Return every square a piece can stand on, in reading order.
>
> Only the dark squares are playable in checkers: those where the
> file and rank counters have opposite parity.

---

## `class Board:`

> Piece positions for one game of checkers.
>
> Squares are named like `c3`, file letter then rank number. The
> `pieces` mapping holds one entry per occupied square.
>
> Attributes:
>     pieces: The occupied squares mapped to their owning side.

### `def __init__(self, pieces: dict[str, str]) -> None:`

> Set the piece positions for both sides.

### `def opening(cls) -> 'Board':`

> Build the standard opening position: dark low, light high.

### `def piece_at(self, square: str) -> str | None:`

### `def apply(self, move: 'Move') -> None:`

> Update the board for one played move.
>
> The moving piece lands on the target square and every
> captured square is emptied.

### `def count(self, side: str) -> int:`

> Count the pieces the given side still has on the board.
