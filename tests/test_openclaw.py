"""Tests for openclaw.OpenClaw (top-level façade)."""

import pytest

from openclaw import Network, OpenClaw


class TestNetworkManagement:
    def test_create_network(self):
        oc = OpenClaw()
        net = oc.create_network("hub")
        assert isinstance(net, Network)
        assert "hub" in oc.networks

    def test_create_network_idempotent(self):
        oc = OpenClaw()
        n1 = oc.create_network("hub")
        n2 = oc.create_network("hub")
        assert n1 is n2

    def test_get_network_existing(self):
        oc = OpenClaw()
        oc.create_network("hub")
        assert oc.get_network("hub") is not None

    def test_get_network_missing(self):
        oc = OpenClaw()
        assert oc.get_network("ghost") is None

    def test_remove_network(self):
        oc = OpenClaw()
        oc.create_network("hub")
        oc.remove_network("hub")
        assert "hub" not in oc.networks

    def test_remove_network_missing_raises(self):
        oc = OpenClaw()
        with pytest.raises(KeyError):
            oc.remove_network("ghost")


class TestCreationMachineIntegration:
    def test_register_and_create(self):
        oc = OpenClaw()

        @oc.creation_machine.register("business")
        def make_business(name: str):
            return {"name": name}

        result = oc.creation_machine.create("business", name="Acme")
        assert result["name"] == "Acme"


class TestConnectNodes:
    def test_connect_nodes_creates_network(self):
        oc = OpenClaw()
        conn = oc.connect_nodes("hub", "a", "b", weight=3)
        assert conn.source == "a"
        assert conn.target == "b"
        assert conn.metadata["weight"] == 3
        net = oc.get_network("hub")
        assert net is not None
        assert "a" in net.nodes

    def test_connect_nodes_reuses_network(self):
        oc = OpenClaw()
        oc.connect_nodes("hub", "a", "b")
        oc.connect_nodes("hub", "b", "c")
        net = oc.get_network("hub")
        assert len(net.connections) == 2


class TestRepr:
    def test_repr(self):
        oc = OpenClaw()
        oc.create_network("n1")
        assert "n1" in repr(oc)
