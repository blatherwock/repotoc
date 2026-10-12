# fixture/arcade/pong/ball.py

> The pong ball and the bounce rules it obeys.

## Ball

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

### step

> Return the ball after one step, bounced off the long walls.

### past_left

> Return whether the ball crossed the left edge.

### past_right

> Return whether the ball crossed the right edge.
