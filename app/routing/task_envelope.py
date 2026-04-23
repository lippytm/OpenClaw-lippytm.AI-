from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List
from uuid import uuid4


@dataclass
class TaskEnvelope:
    task_id: str
    objective: str
    required_capability: str
    source: str = "openclaw"
    priority: str = "normal"
    constraints: Dict[str, Any] = field(default_factory=dict)
    memory_summary: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    success_criteria: List[str] = field(default_factory=list)


def build_task_envelope(
    objective: str,
    required_capability: str,
    context: Dict[str, Any] | None = None,
    memory_summary: str = "",
    priority: str = "normal",
) -> TaskEnvelope:
    return TaskEnvelope(
        task_id=f"task_{uuid4().hex}",
        objective=objective,
        required_capability=required_capability,
        priority=priority,
        constraints={
            "write_allowed": False,
            "review_required": False,
            "protected_paths": [],
        },
        memory_summary=memory_summary,
        context=context or {},
        success_criteria=["task routed", "next step returned to assistant surface"],
    )
