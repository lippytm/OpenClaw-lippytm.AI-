"""OpenClaw Network – manages a collection of nodes and their connections."""

from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional

from .connection import Connection


class Network:
    """A named network that holds nodes and the connections between them.

    A *node* is any hashable identifier (typically a string).  Nodes do not
    need to be registered explicitly – they are inferred from connections or
    can be added via :meth:`add_node`.

    Usage::

        net = Network("BusinessHub")
        net.add_node("company-a", data={"industry": "tech"})
        net.add_node("company-b", data={"industry": "finance"})
        conn = net.connect("company-a", "company-b", partnership="strategic")
        print(net)
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self._nodes: Dict[str, Dict[str, Any]] = {}
        self._connections: List[Connection] = []

    # ------------------------------------------------------------------
    # Node management
    # ------------------------------------------------------------------

    def add_node(self, node_id: str, **data: Any) -> None:
        """Add a node to the network (idempotent – updates data if exists)."""
        self._nodes.setdefault(node_id, {}).update(data)

    def remove_node(self, node_id: str) -> None:
        """Remove a node and all its connections from the network.

        Raises:
            KeyError: If *node_id* is not in the network.
        """
        if node_id not in self._nodes:
            raise KeyError(f"Node {node_id!r} not found in network {self.name!r}")
        del self._nodes[node_id]
        self._connections = [
            c for c in self._connections if not c.is_connected_to(node_id)
        ]

    def node_data(self, node_id: str) -> Dict[str, Any]:
        """Return the metadata dict for a node."""
        return dict(self._nodes[node_id])

    @property
    def nodes(self) -> List[str]:
        """Return all node identifiers."""
        return list(self._nodes)

    # ------------------------------------------------------------------
    # Connection management
    # ------------------------------------------------------------------

    def connect(
        self, source: str, target: str, **metadata: Any
    ) -> Connection:
        """Create a connection from *source* to *target* and add both as nodes.

        Returns the new :class:`~openclaw.connection.Connection`.
        """
        self.add_node(source)
        self.add_node(target)
        conn = Connection(source=source, target=target, metadata=metadata)
        self._connections.append(conn)
        return conn

    def disconnect(self, connection_id: str) -> None:
        """Remove the connection with the given *connection_id*.

        Raises:
            KeyError: If no matching connection is found.
        """
        for i, c in enumerate(self._connections):
            if c.connection_id == connection_id:
                del self._connections[i]
                return
        raise KeyError(f"Connection {connection_id!r} not found")

    def connections_for(self, node_id: str) -> List[Connection]:
        """Return all connections that involve *node_id*."""
        return [c for c in self._connections if c.is_connected_to(node_id)]

    @property
    def connections(self) -> List[Connection]:
        """Return all connections in the network."""
        return list(self._connections)

    # ------------------------------------------------------------------
    # Iteration
    # ------------------------------------------------------------------

    def __iter__(self) -> Iterator[str]:
        return iter(self._nodes)

    def __len__(self) -> int:
        return len(self._nodes)

    def __repr__(self) -> str:
        return (
            f"Network(name={self.name!r}, nodes={len(self._nodes)}, "
            f"connections={len(self._connections)})"
        )
