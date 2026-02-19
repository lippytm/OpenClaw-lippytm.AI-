"""Tests for openclaw.Connection."""

from openclaw import Connection


class TestConnection:
    def test_creation(self):
        conn = Connection(source="a", target="b")
        assert conn.source == "a"
        assert conn.target == "b"
        assert conn.connection_id  # auto-generated UUID

    def test_metadata(self):
        conn = Connection(source="a", target="b", metadata={"weight": 10})
        assert conn.metadata["weight"] == 10

    def test_is_connected_to_source(self):
        conn = Connection(source="a", target="b")
        assert conn.is_connected_to("a")

    def test_is_connected_to_target(self):
        conn = Connection(source="a", target="b")
        assert conn.is_connected_to("b")

    def test_is_connected_to_unrelated(self):
        conn = Connection(source="a", target="b")
        assert not conn.is_connected_to("c")

    def test_reverse(self):
        conn = Connection(source="x", target="y", metadata={"k": "v"})
        rev = conn.reverse()
        assert rev.source == "y"
        assert rev.target == "x"
        assert rev.metadata == {"k": "v"}
        # reversed connection should be a new object
        assert rev is not conn

    def test_unique_ids(self):
        c1 = Connection(source="a", target="b")
        c2 = Connection(source="a", target="b")
        assert c1.connection_id != c2.connection_id

    def test_repr(self):
        conn = Connection(source="a", target="b")
        assert "a" in repr(conn)
        assert "b" in repr(conn)
