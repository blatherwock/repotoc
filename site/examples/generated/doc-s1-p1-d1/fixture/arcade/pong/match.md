# fixture/arcade/pong/match.py

> A pong match: serve, rally, and score until a side reaches eleven.

## Match

> The state of one rally: both paddles, the ball, and the score.
>
> Attributes:
>     left: The left player's paddle.
>     right: The right player's paddle.
>     ball: The ball in flight.
>     score: Points for the left and right sides.

```python
@dataclass
class Match:
```

## serve

> Return a fresh ball leaving the server toward one side.

```python
def serve(*, toward_right: bool=True) -> Ball:
```
