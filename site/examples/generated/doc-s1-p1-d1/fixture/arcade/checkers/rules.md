# fixture/arcade/checkers/rules.py

> Checkers move generation: forced captures and quiet moves.
>
> The rules are pure functions: they read a board and produce moves, and
> never mutate the positions they are given.

## legal_moves

> Return every move the rules allow the side to play.
>
> When any capture exists the rules force it: quiet moves are
> dropped from the result.

```python
def legal_moves(board: Board, side: str) -> list[Move]:
```

## is_capture

> Return whether a move removes any pieces.

```python
def is_capture(move: Move) -> bool:
```

## describe

> Render a move as notation, like `c3xd4` for captures.
>
> Args:
>     move: The move to render.
>     verbose: When set, also name every captured square.

```python
def describe(move: Move, *, verbose: bool=False) -> str:
```

## _captures

> Return the single-jump captures available to the side.

```python
def _captures(board: Board, side: str) -> list[Move]:
```

## _quiet_moves

> Return the diagonal steps to empty neighboring squares.

```python
def _quiet_moves(board: Board, side: str) -> list[Move]:
```

## _shift

> Move a square name by offsets, or None if off the board.

```python
def _shift(square: str, file_step: int, rank_step: int) -> str | None:
```
