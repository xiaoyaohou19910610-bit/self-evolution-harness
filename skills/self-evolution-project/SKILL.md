---
name: self-evolution-project
description: Use for persistent coding-agent projects that need file-first continuity, durable project memory, or reviewed rule promotion. Do not use for self-contained questions or ordinary one-off edits.
---

# Self-Evolution Project

Keep long-running work recoverable from project files and improve future
behavior from verified evidence without forcing every task into a fixed process.

## Scope

- Use when project state must survive separate tasks, repeated mistakes need a
  durable record, or a reviewable handoff is required.
- Do not use for a self-contained explanation, a one-off low-risk edit, or an
  ordinary task whose relevant context is already available.

## Start Or Resume

Read the smallest relevant set first:

1. `AGENTS.md` for active project rules.
2. `memory/progress.md` for objective, current state, and next action.
3. Relevant entries in `memory/corrections.md`, `memory/learned_rules.md`, or
   `memory/wiki/` only when the current task needs them.

If the structure is missing, initialize it from this repository:

```powershell
python tools/bootstrap.py --project C:\path\to\project
```

The bootstrap is idempotent and must not overwrite existing project files.

## Work Loop

1. Establish the current objective and acceptance criteria from project files.
2. Separate verified facts, user decisions, agent suggestions, and unknowns.
3. Implement the smallest complete change and verify observable behavior.
4. Update `memory/progress.md` when unfinished state must survive the task.
5. Record a verified correction when the lesson may matter again.

Do not treat generated files, successful writes, or a plan as delivery when a
runtime or user-visible check is available.

## Evolution Boundary

Keep three layers distinct:

- evidence: corrections, failures, evaluations, and command receipts;
- explanation: durable patterns and rejected lessons under `memory/wiki/`;
- active behavior: compact rules in `AGENTS.md` or a Skill.

A single observation can become a local correction, but it must not become a
shared active rule without review and a regression case. Retire rules that are
noisy, obsolete, or contradicted by stronger evidence.

## Handoff

Transfer the objective, current state, decisions, evidence, blockers, hazards,
owner, and next safe action. Avoid copying the whole conversation. Mark work
complete only after the requested output and its acceptance check are observed.

## Verification

For changes to this harness, run:

```powershell
python -m unittest discover -s tests -v
python tools/check_rule_health.py
```

Keep human approval for publishing, sending, spending money, account or
permission changes, and irreversible cleanup.
