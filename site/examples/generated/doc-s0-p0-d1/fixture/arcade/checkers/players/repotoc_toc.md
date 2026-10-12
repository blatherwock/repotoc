# fixture/arcade/checkers/players

> Players: move choosers that share one interface across games.

- file: [`heuristic.py`](heuristic.md) ([source](../../../../../../fixture/arcade/checkers/players/heuristic.py)): Board scoring for evaluating checkers positions.
- file: [`minimax.py`](minimax.md) ([source](../../../../../../fixture/arcade/checkers/players/minimax.py)): A minimax player that searches a few plies deep.
- dir: [`strategies/`](strategies/repotoc_toc.md) ([source](../../../../../../fixture/arcade/checkers/players/strategies/__init__.py))
  - file: [`capture_first.py`](strategies/capture_first.md) ([source](../../../../../../fixture/arcade/checkers/players/strategies/capture_first.py)): A greedy player that always plays the first available capture.
  - file: [`random_move.py`](strategies/random_move.md) ([source](../../../../../../fixture/arcade/checkers/players/strategies/random_move.py))
