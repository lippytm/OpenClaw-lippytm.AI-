from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List
from datetime import datetime, timezone


@dataclass
class SessionAwareness:
    session_id: str
    lane: str = 'product'
    state: str = 'idle'
    confidence: float = 0.75
    current_goal: str = ''
    memory_summary: str = ''
    recent_events: List[str] = field(default_factory=list)
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


def build_session_snapshot(session_id: str, current_goal: str = '', memory_summary: str = '') -> Dict[str, object]:
    awareness = SessionAwareness(
        session_id=session_id,
        state='planning' if current_goal else 'idle',
        current_goal=current_goal,
        memory_summary=memory_summary,
    )
    return awareness.__dict__
