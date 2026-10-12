# `fixture/arcade/pong/ball.py`

> The pong ball and the bounce rules it obeys.

## `class Ball:`

> The ball's position and travel vector.
>
> The table runs from x `0` to `10` and y `0` to `6`. The ball moves
> by its velocity each step and bounces off the top and bottom.
>
> Attributes:
>     x: The horizontal position.
>     y: The vertical position.
>     vx: The horizontal travel per step.
>     vy: The vertical travel per step.

### `def step(self) -> 'Ball':`

> Return the ball after one step, bounced off the long walls.

### `def past_left(self) -> bool:`

> Return whether the ball crossed the left edge.

### `def past_right(self) -> bool:`

> Return whether the ball crossed the right edge.
