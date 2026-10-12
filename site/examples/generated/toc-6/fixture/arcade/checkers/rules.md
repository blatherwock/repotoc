# `fixture/arcade/checkers/rules.py`

> Checkers move generation: forced captures and quiet moves.
>
> The rules are pure functions: they read a board and produce moves, and
> never mutate the positions they are given.

## `def legal_moves(board: Board, side: str) -> list[Move]:`

> Return every move the rules allow the side to play.
>
> When any capture exists the rules force it: quiet moves are
> dropped from the result.

---

## `def is_capture(move: Move) -> bool:`

> Return whether a move removes any pieces.

---

## `def describe(move: Move, *, verbose: bool=False) -> str:`

> Render a move as notation, like `c3xd4` for captures.
>
> Args:
>     move: The move to render.
>     verbose: When set, also name every captured square.
