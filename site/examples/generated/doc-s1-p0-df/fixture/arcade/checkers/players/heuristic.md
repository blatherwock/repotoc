# fixture/arcade/checkers/players/heuristic.py

> Board scoring for evaluating checkers positions.

## material

> Score a board by piece counts from one side's view.

```python
def material(board: 'Board', side: str) -> int:
```

## positional

```python
def positional(board: 'Board', side: str) -> int:
```
