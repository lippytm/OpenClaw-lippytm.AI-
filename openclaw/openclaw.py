"""OpenClaw – top-level façade that wires together CreationMachines and Networks."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .connection import Connection
from .creation_machine import CreationMachine
from .network import Network


class OpenClaw:
    """The central hub of the OpenClaw platform.

    An :class:`OpenClaw` instance owns:

    * A :class:`~openclaw.creation_machine.CreationMachine` for unlimited
      entity creation.
    * A registry of named :class:`~openclaw.network.Network` objects.

    Usage::

        oc = OpenClaw()

        # Register a blueprint and create entities
        @oc.creation_machine.register("business")
        def make_business(name: str, industry: str = "general"):
            return {"name": name, "industry": industry}

        biz_a = oc.creation_machine.create("business", name="Acme")

        # Build a network of businesses
        hub = oc.create_network("BusinessHub")
        hub.add_node("Acme", industry="tech")
        hub.add_node("BetaCo", industry="finance")
        hub.connect("Acme", "BetaCo", partnership="strategic")
    """

    def __init__(self) -> None:
        self.creation_machine: CreationMachine = CreationMachine()
        self._networks: Dict[str, Network] = {}

    # ------------------------------------------------------------------
    # Network management
    # ------------------------------------------------------------------

    def create_network(self, name: str) -> Network:
        """Create (or retrieve) a :class:`Network` with the given *name*."""
        if name not in self._networks:
            self._networks[name] = Network(name)
        return self._networks[name]

    def get_network(self, name: str) -> Optional[Network]:
        """Return the network for *name*, or ``None`` if it doesn't exist."""
        return self._networks.get(name)

    def remove_network(self, name: str) -> None:
        """Remove a network by name.

        Raises:
            KeyError: If the network does not exist.
        """
        if name not in self._networks:
            raise KeyError(f"Network {name!r} not found")
        del self._networks[name]

    @property
    def networks(self) -> List[str]:
        """Return the names of all registered networks."""
        return list(self._networks)

    # ------------------------------------------------------------------
    # Cross-network convenience
    # ------------------------------------------------------------------

    def connect_nodes(
        self,
        network_name: str,
        source: str,
        target: str,
        **metadata: Any,
    ) -> Connection:
        """Connect *source* to *target* in a network (creates network if needed).

        Returns the resulting :class:`~openclaw.connection.Connection`.
        """
        net = self.create_network(network_name)
        return net.connect(source, target, **metadata)

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"OpenClaw(networks={self.networks}, "
            f"kinds={self.creation_machine.kinds})"
        )
