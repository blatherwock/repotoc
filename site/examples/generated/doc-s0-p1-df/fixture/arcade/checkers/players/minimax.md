# fixture/arcade/checkers/players/minimax.py

> A minimax player that searches a few plies deep.
>
> The search alternates sides ply by ply and scores leaves with the
> positional heuristic. Nothing is pruned; checkers trees stay small
> enough for a demo.

## MinimaxPlayer

> A player choosing moves by minimax over a board heuristic.
>
> Attributes:
>     side: The side this player moves for.
>     depth: The search depth in plies.

### __init__

### choose

> Return the move with the best minimax score, None if stuck.

### _search

> Score a position recursively; higher is better for our side.

## _played

> Return a copy of the board with the move applied.

## _opponent

> Return the other side's name.
