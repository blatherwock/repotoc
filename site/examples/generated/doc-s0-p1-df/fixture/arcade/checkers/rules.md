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

## is_capture

> Return whether a move removes any pieces.

## describe

> Render a move as notation, like `c3xd4` for captures.
>
> Args:
>     move: The move to render.
>     verbose: When set, also name every captured square.

## _captures

> Return the single-jump captures available to the side.

## _quiet_moves

> Return the diagonal steps to empty neighboring squares.

## _shift

> Move a square name by offsets, or None if off the board.
