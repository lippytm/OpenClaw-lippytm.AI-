"""Tests for openclaw.CreationMachine."""

import pytest

from openclaw import CreationMachine


def _make_cm_with_business():
    cm = CreationMachine()

    @cm.register("business")
    def make_business(name: str, industry: str = "general"):
        return {"type": "business", "name": name, "industry": industry}

    return cm


class TestRegistration:
    def test_register_decorator(self):
        cm = CreationMachine()

        @cm.register("widget")
        def make_widget(color: str = "red"):
            return {"color": color}

        assert "widget" in cm.kinds

    def test_register_function(self):
        cm = CreationMachine()
        cm.register_function("thing", lambda name: {"name": name})
        assert "thing" in cm.kinds

    def test_register_class(self):
        class Dog:
            def __init__(self, name: str):
                self.name = name

        cm = CreationMachine()
        cm.register_class("dog", Dog)
        assert "dog" in cm.kinds


class TestCreate:
    def test_create_basic(self):
        cm = _make_cm_with_business()
        biz = cm.create("business", name="Acme", industry="tech")
        assert biz == {"type": "business", "name": "Acme", "industry": "tech"}

    def test_create_defaults(self):
        cm = _make_cm_with_business()
        biz = cm.create("business", name="Beta")
        assert biz["industry"] == "general"

    def test_create_unknown_kind_raises(self):
        cm = CreationMachine()
        with pytest.raises(KeyError, match="unknown"):
            cm.create("unknown")

    def test_create_many(self):
        cm = CreationMachine()
        cm.register_function("token", lambda: object())
        tokens = cm.create_many("token", 5)
        assert len(tokens) == 5

    def test_create_many_zero(self):
        cm = CreationMachine()
        cm.register_function("item", lambda: {})
        assert cm.create_many("item", 0) == []

    def test_create_many_negative_raises(self):
        cm = CreationMachine()
        cm.register_function("item", lambda: {})
        with pytest.raises(ValueError):
            cm.create_many("item", -1)


class TestKinds:
    def test_kinds_empty(self):
        cm = CreationMachine()
        assert cm.kinds == []

    def test_kinds_multiple(self):
        cm = CreationMachine()
        cm.register_function("a", lambda: None)
        cm.register_function("b", lambda: None)
        assert set(cm.kinds) == {"a", "b"}

    def test_repr(self):
        cm = CreationMachine()
        cm.register_function("x", lambda: None)
        assert "x" in repr(cm)
