# fixture/arcade

> A tiny arcade of classic games built on one shared move interface.

- [`checkers/`](checkers/repotoc_toc.md) ([source](../../../../fixture/arcade/checkers/__init__.py)): Checkers: an eight-by-eight board game with forced captures.
  - [`board.py`](checkers/board.md) ([source](../../../../fixture/arcade/checkers/board.py)): The checkers board: piece positions and the moves that change them.
  - [`players/`](checkers/players/repotoc_toc.md) ([source](../../../../fixture/arcade/checkers/players/__init__.py)): Players: move choosers that share one interface across games.
  - [`rules.py`](checkers/rules.md) ([source](../../../../fixture/arcade/checkers/rules.py)): Checkers move generation: forced captures and quiet moves.
- [`game.py`](game.md) ([source](../../../../fixture/arcade/game.py)): The shared move and game types every arcade game builds on.
- [`pong/`](pong/repotoc_toc.md) ([source](../../../../fixture/arcade/pong/__init__.py)): Pong: two paddles, one ball, first to eleven points wins.
  - [`ball.py`](pong/ball.md) ([source](../../../../fixture/arcade/pong/ball.py)): The pong ball and the bounce rules it obeys.
  - [`match.py`](pong/match.md) ([source](../../../../fixture/arcade/pong/match.py)): A pong match: serve, rally, and score until a side reaches eleven.
  - [`paddle.py`](pong/paddle.md) ([source](../../../../fixture/arcade/pong/paddle.py)): The paddles each side controls.
- [`registry.py`](registry.md) ([source](../../../../fixture/arcade/registry.py)): Game registry: names mapped to factory functions.
