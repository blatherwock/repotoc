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

```python
class MinimaxPlayer:
```

### __init__

```python
    def __init__(self, side: str, depth: int=_MAX_DEPTH) -> None:
```

### choose

> Return the move with the best minimax score, None if stuck.

```python
    def choose(self, board: Board) -> 'Move | None':
```

### _search

> Score a position recursively; higher is better for our side.

```python
    def _search(self, board: Board, ply: int) -> int:
```

## _played

> Return a copy of the board with the move applied.

```python
def _played(board: Board, move: 'Move') -> Board:
```

## _opponent

> Return the other side's name.

```python
def _opponent(side: str) -> str:
```
