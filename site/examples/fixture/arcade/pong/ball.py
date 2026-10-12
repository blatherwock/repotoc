"""The pong ball and the bounce rules it obeys."""

from dataclasses import dataclass

_TABLE_H = 6
_LEFT_EDGE = 0.0
_RIGHT_EDGE = 10.0


@dataclass(frozen=True)
class Ball:
    """The ball's position and travel vector.

    The table runs from x `0` to `10` and y `0` to `6`. The ball moves
    by its velocity each step and bounces off the top and bottom.

    Attributes:
        x: The horizontal position.
        y: The vertical position.
        vx: The horizontal travel per step.
        vy: The vertical travel per step.
    """

    x: float
    y: float
    vx: float
    vy: float

    def step(self) -> "Ball":
        """Return the ball after one step, bounced off the long walls."""
        y = self.y + self.vy
        vy = self.vy
        if y <= 0 or y >= _TABLE_H:
            vy = -self.vy
        return Ball(self.x + self.vx, y, self.vx, vy)

    def past_left(self) -> bool:
        """Return whether the ball crossed the left edge."""
        return self.x <= _LEFT_EDGE

    def past_right(self) -> bool:
        """Return whether the ball crossed the right edge."""
        return self.x >= _RIGHT_EDGE
