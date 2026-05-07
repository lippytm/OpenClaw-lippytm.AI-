"""Tests for openclaw.Network."""

import pytest

from openclaw import Network


class TestNodes:
    def test_add_node(self):
        net = Network("test")
        net.add_node("node-1", color="red")
        assert "node-1" in net.nodes

    def test_add_node_idempotent(self):
        net = Network("test")
        net.add_node("node-1", x=1)
        net.add_node("node-1", y=2)
        data = net.node_data("node-1")
        assert data["x"] == 1
        assert data["y"] == 2

    def test_remove_node(self):
        net = Network("test")
        net.add_node("n1")
        net.remove_node("n1")
        assert "n1" not in net.nodes

    def test_remove_node_also_removes_connections(self):
        net = Network("test")
        net.connect("a", "b")
        net.connect("b", "c")
        net.remove_node("b")
        assert len(net.connections) == 0

    def test_remove_nonexistent_node_raises(self):
        net = Network("test")
        with pytest.raises(KeyError):
            net.remove_node("ghost")

    def test_len(self):
        net = Network("test")
        net.add_node("a")
        net.add_node("b")
        assert len(net) == 2

    def test_iter(self):
        net = Network("test")
        net.add_node("x")
        net.add_node("y")
        assert set(net) == {"x", "y"}


class TestConnections:
    def test_connect_creates_nodes(self):
        net = Network("test")
        net.connect("src", "tgt")
        assert "src" in net.nodes
        assert "tgt" in net.nodes

    def test_connect_returns_connection(self):
        from openclaw import Connection

        net = Network("test")
        conn = net.connect("a", "b")
        assert isinstance(conn, Connection)
        assert conn.source == "a"
        assert conn.target == "b"

    def test_connect_with_metadata(self):
        net = Network("test")
        conn = net.connect("a", "b", weight=5)
        assert conn.metadata["weight"] == 5

    def test_connections_for(self):
        net = Network("test")
        net.connect("a", "b")
        net.connect("c", "a")
        net.connect("b", "c")
        conns = net.connections_for("a")
        assert len(conns) == 2

    def test_disconnect(self):
        net = Network("test")
        conn = net.connect("a", "b")
        net.disconnect(conn.connection_id)
        assert len(net.connections) == 0

    def test_disconnect_nonexistent_raises(self):
        net = Network("test")
        with pytest.raises(KeyError):
            net.disconnect("no-such-id")

    def test_repr(self):
        net = Network("MyNet")
        assert "MyNet" in repr(net)
