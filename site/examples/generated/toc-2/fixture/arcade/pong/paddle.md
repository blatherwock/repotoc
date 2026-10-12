# fixture/arcade/pong/paddle.py

> The paddles each side controls.

## Paddle

> One player's paddle: fixed x, free to move in y.
>
> Attributes:
>     x: The fixed horizontal position.
>     y: The vertical center of the paddle.
>     reach: Half the paddle's height, the strike zone around y.

```python
@dataclass(frozen=True)
class Paddle:
```

### moved

> Return the paddle shifted by dy, clamped to the track.

```python
    def moved(self, dy: float) -> 'Paddle':
```

### hits

> Return whether a ball at this height is in the strike zone.

```python
    def hits(self, ball_y: float) -> bool:
```
