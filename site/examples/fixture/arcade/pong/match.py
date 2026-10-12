"""A pong match: serve, rally, and score until a side reaches eleven."""

from dataclasses import dataclass

from .ball import Ball
from .paddle import Paddle

_WINNING = 11


@dataclass
class Match:
    """The state of one rally: both paddles, the ball, and the score.

    Attributes:
        left: The left player's paddle.
        right: The right player's paddle.
        ball: The ball in flight.
        score: Points for the left and right sides.
    """

    left: Paddle
    right: Paddle
    ball: Ball
    score: tuple[int, int] = (0, 0)

    def rally(self, steps: int = 10) -> tuple[int, int]:
        """Advance the ball for a number of steps, scoring edges.

        Returns:
            The updated score, with a point added when the ball
            crosses a side's edge.
        """
        left, right = self.score
        for _ in range(steps):
            self.ball = self.ball.step()
            if self.ball.past_left():
                right += 1
                break
            if self.ball.past_right():
                left += 1
                break
        self.score = (left, right)
        return self.score

    def is_over(self) -> bool:
        """Return whether either side has reached the winning score."""
        return max(self.score) >= _WINNING


def serve(*, toward_right: bool = True) -> Ball:
    """Return a fresh ball leaving the server toward one side."""
    direction = 1.0 if toward_right else -1.0
    return Ball(5.0, 3.0, direction, 0.5)
