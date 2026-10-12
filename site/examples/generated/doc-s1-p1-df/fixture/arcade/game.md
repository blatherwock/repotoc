# fixture/arcade/game.py

> The shared move and game types every arcade game builds on.
>
> Each game describes its own rules and reports legal moves as `Move`
> records, so player code can be written once and shared across games.

## Move

> One legal move in a game.
>
> Attributes:
>     origin: The position the acting piece starts on.
>     target: The position the acting piece lands on.
>     captures: The positions of any pieces the move removes.

```python
@dataclass(frozen=True)
class Move:
```

## Game

> A turn-based game that can report and apply its own moves.
>
> Games are passive: they hold rules and state only. Choosing which
> move to play belongs to the players, not to the game.

```python
class Game:
```

### legal_moves

> Return every move the rules allow for the side to act.

```python
    def legal_moves(self) -> list[Move]:
```

### apply

> Update the game state to reflect a played move.

```python
    def apply(self, move: Move) -> None:
```
