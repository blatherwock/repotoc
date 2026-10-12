# fixture/arcade

> A tiny arcade of classic games built on one shared move interface.

- dir: [`checkers/`](checkers/repotoc_toc.md) ([source](../../../../fixture/arcade/checkers/__init__.py)): Checkers: an eight-by-eight board game with forced captures.
  - file: [`board.py`](checkers/board.md) ([source](../../../../fixture/arcade/checkers/board.py)): The checkers board: piece positions and the moves that change them.
  - dir: [`players/`](checkers/players/repotoc_toc.md) ([source](../../../../fixture/arcade/checkers/players/__init__.py)): Players: move choosers that share one interface across games.
    - file: [`heuristic.py`](checkers/players/heuristic.md) ([source](../../../../fixture/arcade/checkers/players/heuristic.py)): Board scoring for evaluating checkers positions.
    - file: [`minimax.py`](checkers/players/minimax.md) ([source](../../../../fixture/arcade/checkers/players/minimax.py)): A minimax player that searches a few plies deep.
    - dir: [`strategies/`](checkers/players/strategies/repotoc_toc.md) ([source](../../../../fixture/arcade/checkers/players/strategies/__init__.py))
      - file: [`capture_first.py`](checkers/players/strategies/capture_first.md) ([source](../../../../fixture/arcade/checkers/players/strategies/capture_first.py)): A greedy player that always plays the first available capture.
      - file: [`random_move.py`](checkers/players/strategies/random_move.md) ([source](../../../../fixture/arcade/checkers/players/strategies/random_move.py))
  - file: [`rules.py`](checkers/rules.md) ([source](../../../../fixture/arcade/checkers/rules.py)): Checkers move generation: forced captures and quiet moves.
- file: [`game.py`](game.md) ([source](../../../../fixture/arcade/game.py)): The shared move and game types every arcade game builds on.
- dir: [`pong/`](pong/repotoc_toc.md) ([source](../../../../fixture/arcade/pong/__init__.py)): Pong: two paddles, one ball, first to eleven points wins.
  - file: [`ball.py`](pong/ball.md) ([source](../../../../fixture/arcade/pong/ball.py)): The pong ball and the bounce rules it obeys.
  - file: [`match.py`](pong/match.md) ([source](../../../../fixture/arcade/pong/match.py)): A pong match: serve, rally, and score until a side reaches eleven.
  - file: [`paddle.py`](pong/paddle.md) ([source](../../../../fixture/arcade/pong/paddle.py)): The paddles each side controls.
- file: [`registry.py`](registry.md) ([source](../../../../fixture/arcade/registry.py)): Game registry: names mapped to factory functions.
