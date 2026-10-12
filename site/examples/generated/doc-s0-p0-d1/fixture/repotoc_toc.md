# fixture

- [`arcade/`](arcade/repotoc_toc.md) ([source](../../../fixture/arcade/__init__.py)): A tiny arcade of classic games built on one shared move interface.
  - [`checkers/`](arcade/checkers/repotoc_toc.md) ([source](../../../fixture/arcade/checkers/__init__.py)): Checkers: an eight-by-eight board game with forced captures.
    - [`board.py`](arcade/checkers/board.md) ([source](../../../fixture/arcade/checkers/board.py)): The checkers board: piece positions and the moves that change them.
    - [`players/`](arcade/checkers/players/repotoc_toc.md) ([source](../../../fixture/arcade/checkers/players/__init__.py)): Players: move choosers that share one interface across games.
      - [`heuristic.py`](arcade/checkers/players/heuristic.md) ([source](../../../fixture/arcade/checkers/players/heuristic.py)): Board scoring for evaluating checkers positions.
      - [`minimax.py`](arcade/checkers/players/minimax.md) ([source](../../../fixture/arcade/checkers/players/minimax.py)): A minimax player that searches a few plies deep.
      - [`strategies/`](arcade/checkers/players/strategies/repotoc_toc.md) ([source](../../../fixture/arcade/checkers/players/strategies/__init__.py))
        - [`capture_first.py`](arcade/checkers/players/strategies/capture_first.md) ([source](../../../fixture/arcade/checkers/players/strategies/capture_first.py)): A greedy player that always plays the first available capture.
        - [`random_move.py`](arcade/checkers/players/strategies/random_move.md) ([source](../../../fixture/arcade/checkers/players/strategies/random_move.py))
    - [`rules.py`](arcade/checkers/rules.md) ([source](../../../fixture/arcade/checkers/rules.py)): Checkers move generation: forced captures and quiet moves.
  - [`game.py`](arcade/game.md) ([source](../../../fixture/arcade/game.py)): The shared move and game types every arcade game builds on.
  - [`pong/`](arcade/pong/repotoc_toc.md) ([source](../../../fixture/arcade/pong/__init__.py)): Pong: two paddles, one ball, first to eleven points wins.
    - [`ball.py`](arcade/pong/ball.md) ([source](../../../fixture/arcade/pong/ball.py)): The pong ball and the bounce rules it obeys.
    - [`match.py`](arcade/pong/match.md) ([source](../../../fixture/arcade/pong/match.py)): A pong match: serve, rally, and score until a side reaches eleven.
    - [`paddle.py`](arcade/pong/paddle.md) ([source](../../../fixture/arcade/pong/paddle.py)): The paddles each side controls.
  - [`registry.py`](arcade/registry.md) ([source](../../../fixture/arcade/registry.py)): Game registry: names mapped to factory functions.
