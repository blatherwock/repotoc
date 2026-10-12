# `fixture/arcade/checkers/board.py`

> The checkers board: piece positions and the moves that change them.

## `def playable_squares():`

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
