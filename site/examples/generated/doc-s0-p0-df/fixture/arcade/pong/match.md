# `fixture/arcade/pong/match.py`

> A pong match: serve, rally, and score until a side reaches eleven.

## `class Match:`

> The state of one rally: both paddles, the ball, and the score.
>
> Attributes:
>     left: The left player's paddle.
>     right: The right player's paddle.
>     ball: The ball in flight.
>     score: Points for the left and right sides.

### `def rally(...):`

> Advance the ball for a number of steps, scoring edges.
>
> Returns:
>     The updated score, with a point added when the ball
>     crosses a side's edge.

### `def is_over(...):`

> Return whether either side has reached the winning score.

---

## `def serve(...):`

> Return a fresh ball leaving the server toward one side.
