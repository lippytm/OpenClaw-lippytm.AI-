"""OpenClaw Connection – links between nodes in an OpenClaw Network."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Connection:
    """Represents a directional connection between two network nodes.

    Attributes:
        source: Identifier of the originating node.
        target: Identifier of the destination node.
        metadata: Arbitrary key-value data attached to this connection.
        connection_id: Auto-generated unique identifier for this connection.
    """

    source: str
    target: str
    metadata: dict[str, Any] = field(default_factory=dict)
    connection_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------

    def is_connected_to(self, node_id: str) -> bool:
        """Return True if this connection involves *node_id* (source or target)."""
        return self.source == node_id or self.target == node_id

    def reverse(self) -> "Connection":
        """Return a new Connection with source and target swapped."""
        return Connection(
            source=self.target,
            target=self.source,
            metadata=dict(self.metadata),
        )

    def __repr__(self) -> str:
        return (
            f"Connection(id={self.connection_id!r}, "
            f"{self.source!r} -> {self.target!r})"
        )
