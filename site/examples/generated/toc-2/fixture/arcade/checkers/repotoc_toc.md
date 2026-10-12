# fixture/arcade/checkers

> Checkers: an eight-by-eight board game with forced captures.

- [`board.py`](board.md) ([source](../../../../../fixture/arcade/checkers/board.py)): The checkers board: piece positions and the moves that change them.
- [`players/`](players/repotoc_toc.md) ([source](../../../../../fixture/arcade/checkers/players/__init__.py)): Players: move choosers that share one interface across games.
  - [`heuristic.py`](players/heuristic.md) ([source](../../../../../fixture/arcade/checkers/players/heuristic.py)): Board scoring for evaluating checkers positions.
  - [`minimax.py`](players/minimax.md) ([source](../../../../../fixture/arcade/checkers/players/minimax.py)): A minimax player that searches a few plies deep.
  - [`strategies/`](players/strategies/repotoc_toc.md) ([source](../../../../../fixture/arcade/checkers/players/strategies/__init__.py))
- [`rules.py`](rules.md) ([source](../../../../../fixture/arcade/checkers/rules.py)): Checkers move generation: forced captures and quiet moves.
