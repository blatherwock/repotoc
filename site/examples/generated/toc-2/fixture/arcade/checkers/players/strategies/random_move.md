# fixture/arcade/checkers/players/strategies/random_move.py

## RandomMovePlayer

> A player that picks uniformly among the legal moves.

```python
class RandomMovePlayer:
```

### __init__

> Bind the player to one side.

```python
    def __init__(self, side: str) -> None:
```

### choose

> Return a uniformly random legal move, None if stuck.

```python
    def choose(self, board: Board) -> 'Move | None':
```
