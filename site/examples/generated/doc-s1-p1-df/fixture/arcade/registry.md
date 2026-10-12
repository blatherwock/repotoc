# fixture/arcade/registry.py

> Game registry: names mapped to factory functions.
>
> Registering a game makes it available to callers that only know its
> name, without importing every game module up front.

## register

> Add a game factory under a name, replacing any earlier one.

```python
def register(name: str, factory: 'Callable[[], Game]') -> None:
```

## create

> Build a fresh instance of the named game.
>
> Raises:
>     KeyError: No game was registered under the name.

```python
def create(name: str) -> 'Game':
```

## known_games

```python
def known_games() -> list[str]:
```
