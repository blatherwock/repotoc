"""The paddles each side controls."""

from dataclasses import dataclass

_TRACK_TOP = 0.5
_TRACK_BOTTOM = 5.5


@dataclass(frozen=True)
class Paddle:
    """One player's paddle: fixed x, free to move in y.

    Attributes:
        x: The fixed horizontal position.
        y: The vertical center of the paddle.
        reach: Half the paddle's height, the strike zone around y.
    """

    x: float
    y: float
    reach: float = 1.0

    def moved(self, dy: float) -> "Paddle":
        """Return the paddle shifted by dy, clamped to the track."""
        y = min(max(self.y + dy, _TRACK_TOP), _TRACK_BOTTOM)
        return Paddle(self.x, y, self.reach)

    def hits(self, ball_y: float) -> bool:
        """Return whether a ball at this height is in the strike zone."""
        return abs(self.y - ball_y) <= self.reach
