# fixture/arcade/checkers/players/strategies/capture_first.py

> A greedy player that always plays the first available capture.

## CaptureFirstPlayer

```python
class CaptureFirstPlayer:
```

### __init__

> Bind the player to one side.

```python
    def __init__(self, side: str) -> None:
```

### choose

> Return the first capture, else the first quiet move.

```python
    def choose(self, board: Board) -> 'Move | None':
```
