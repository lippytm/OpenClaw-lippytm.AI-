# OpenClaw ↔ MyClaw Integration

This document defines how `OpenClaw-lippytm.AI-` should integrate with `MyClaw.lippytm.AI-`.

The goal is to preserve a clean separation between the assistant experience and the swarm execution fabric.

---

## Integration Goal

Allow OpenClaw to act as a user-facing assistant surface while MyClaw handles:

- routing
n- agent coordination
- escalation
- task distribution
- structured handoffs

---

## Separation of Responsibility

### OpenClaw owns
- conversation surface
- user session flow
- intake and guidance experience
- assistant interaction design

### MyClaw owns
- task routing
- swarm communication
- supervisor escalation
- execution handoff
- dead-letter and recovery paths

---

## Suggested Interaction Pattern

1. user interacts with OpenClaw
2. OpenClaw gathers intent and context
3. OpenClaw packages structured task request
4. MyClaw routes task to appropriate agent or supervisor path
5. results or updates return to OpenClaw for user presentation

---

## Best Practices

- keep conversational complexity separate from routing complexity
- send structured task envelopes into MyClaw rather than raw chat whenever possible
- preserve user-friendly explanations when escalations happen
- do not expose internal swarm complexity directly unless needed for operators

---

## Rule of thumb

OpenClaw should feel simple on the surface while MyClaw handles the specialist coordination behind the scenes.
