# OpenClaw-lippytm.AI-

My personal AI Assistant Creation Networking Platform — unlimited creation machines, networked business entities, and the connections that enable everything.

---

## Overview

OpenClaw is a Python platform built around three core primitives:

| Class | Purpose |
|---|---|
| `CreationMachine` | Unlimited factory — register blueprints and create any number of entities |
| `Network` | Named graph of nodes (businesses, services, agents …) and the connections between them |
| `Connection` | A directed link between two nodes, with optional metadata |
| `OpenClaw` | Top-level façade that owns a `CreationMachine` and a registry of `Network` objects |

---

## Quick Start

```python
from openclaw import OpenClaw

oc = OpenClaw()

# ── 1. Register blueprints with the Creation Machine ──────────────────
@oc.creation_machine.register("business")
def make_business(name: str, industry: str = "general"):
    return {"name": name, "industry": industry}

# Create unlimited instances
acme   = oc.creation_machine.create("business", name="Acme Corp", industry="tech")
beta   = oc.creation_machine.create("business", name="Beta Inc",  industry="finance")
# … or many at once
startups = oc.creation_machine.create_many("business", count=10, name="Startup", industry="SaaS")

# ── 2. Build networks of businesses ───────────────────────────────────
hub = oc.create_network("BusinessHub")
hub.add_node("Acme Corp",  industry="tech")
hub.add_node("Beta Inc",   industry="finance")

# ── 3. Connect nodes (enable everything) ──────────────────────────────
conn = hub.connect("Acme Corp", "Beta Inc", partnership="strategic")
print(conn)
# Connection(id='...', 'Acme Corp' -> 'Beta Inc')

# Shorthand — creates the network automatically if it doesn't exist
oc.connect_nodes("BusinessHub", "Acme Corp", "Gamma Ltd", role="supplier")

print(oc)
# OpenClaw(networks=['BusinessHub'], kinds=['business'])
```

---

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

---

## Project Structure

```
openclaw/
├── __init__.py          # Public API
├── connection.py        # Connection dataclass
├── creation_machine.py  # CreationMachine factory
├── network.py           # Network graph
└── openclaw.py          # OpenClaw façade
tests/
├── test_connection.py
├── test_creation_machine.py
├── test_network.py
└── test_openclaw.py
```

