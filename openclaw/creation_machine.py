"""OpenClaw CreationMachine – unlimited factory for creating network entities."""

from __future__ import annotations

from typing import Any, Callable, Dict, Type


class CreationMachine:
    """A factory that registers blueprints and produces unlimited instances.

    Usage::

        cm = CreationMachine()

        @cm.register("business")
        def make_business(name: str, **kw):
            return {"type": "business", "name": name, **kw}

        biz = cm.create("business", name="Acme Corp")
    """

    def __init__(self) -> None:
        self._blueprints: Dict[str, Callable[..., Any]] = {}

    # ------------------------------------------------------------------
    # Blueprint registration
    # ------------------------------------------------------------------

    def register(self, kind: str) -> Callable:
        """Decorator that registers a factory function under *kind*."""

        def decorator(fn: Callable) -> Callable:
            self._blueprints[kind] = fn
            return fn

        return decorator

    def register_class(self, kind: str, cls: Type) -> None:
        """Register a class constructor directly."""
        self._blueprints[kind] = cls

    def register_function(self, kind: str, fn: Callable) -> None:
        """Register a plain callable as the factory for *kind*."""
        self._blueprints[kind] = fn

    # ------------------------------------------------------------------
    # Creation
    # ------------------------------------------------------------------

    def create(self, kind: str, *args: Any, **kwargs: Any) -> Any:
        """Instantiate an entity of *kind* using the registered blueprint.

        Raises:
            KeyError: If no blueprint is registered for *kind*.
        """
        if kind not in self._blueprints:
            raise KeyError(
                f"No blueprint registered for kind {kind!r}. "
                f"Available kinds: {list(self._blueprints)}"
            )
        return self._blueprints[kind](*args, **kwargs)

    def create_many(self, kind: str, count: int, *args: Any, **kwargs: Any) -> list:
        """Create *count* instances of *kind* in one call."""
        if count < 0:
            raise ValueError("count must be >= 0")
        return [self.create(kind, *args, **kwargs) for _ in range(count)]

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    @property
    def kinds(self) -> list[str]:
        """Return all registered kind names."""
        return list(self._blueprints)

    def __repr__(self) -> str:
        return f"CreationMachine(kinds={self.kinds})"
