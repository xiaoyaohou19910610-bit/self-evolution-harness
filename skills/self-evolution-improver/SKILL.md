---
name: self-evolution-improver
description: Turn verified corrections, repeated mistakes, retrospectives, or explicit requests to improve future agent behavior into reviewable proposals and regression checks. Do not use for an isolated fix with no reusable learning request.
---

# Self-Evolution Improver

Use this skill as the outer loop around a project-specific agent, workflow, or
Skill. It analyzes evidence and prepares a candidate change; it does not edit
active rules or Skills by itself. When the user explicitly asks to remember,
absorb, or settle a lesson, it may write non-active project-local notes or
proposal records, but those notes do not change agent behavior until promoted
through the normal approval path.

## Scope

- Use when evidence should change future behavior: a repeated failure, user
  correction, retrospective, rule cleanup, or explicit request to remember,
  absorb, settle, promote, apply, roll back, or retire a lesson.
- Do not use for a single implementation bug, factual correction, or local
  documentation edit unless the user also wants a durable behavior change.

## Inputs

Read the project files first, especially `AGENTS.md`, `memory/progress.md`,
`memory/corrections.md`, `memory/learned_rules.md`, `memory/wiki/`, and
`memory/evolution/feedback.jsonl` when present. Treat user feedback, test
failures, review comments, and runtime observations as evidence with different
confidence levels.

## Procedure

1. Separate the expected behavior, observed behavior, cause, and evidence.
2. Check whether the signal is local, repeated, or supported across projects.
3. Identify the narrowest target: task guidance, project memory, a Skill,
   template, or global guidance.
   If the failure is in review, approval, handoff, or maintenance rather than
   implementation, consider an artifact-chain change such as intent/spec/plan or
   review evidence before adding more execution rules.
4. Propose the smallest change that explains the reason and does not duplicate
   an existing rule.
5. Keep raw evidence, Wiki patterns, and active Skill/rule text separate. Long
   WHY, root-cause history, and rejected-candidate lessons belong in Wiki files,
   not inside `SKILL.md`.
6. Read `memory/wiki/index.md` and `memory/wiki/skill_impact.md` before
   proposing a Skill/rule change, then inspect only relevant pattern pages and
   the minimum raw evidence needed.
7. Attach fixed regression cases, a verification plan, and explicit risks.
8. Record the proposal under `memory/evolution/proposals/`, including its
   evidence, scope, regression case, verification plan, and retirement
   condition. If the user asked only to remember a lesson, write a non-active
   local correction and mark any behavior change as `candidate` or `proposed`.
9. Stop at `proposed` before applying any active Skill, template, or rule
   change until a human reviews and approves it. Codex may then apply the patch,
   run the regression cases, and record `applied` only with evidence.

## Invariants

- Never convert one unverified opinion into a global rule.
- Never let a feedback record or proposal execute commands, publish, send
  messages, change permissions, or handle credentials. Writing an explicitly
  requested non-active project note is allowed; changing active instructions is
  not.
- Keep Memory as what happened and Skills/rules as how to behave next time.
- Preserve useful lessons from rejected or rolled-back candidates in the Wiki
  layer, even when the active Skill/rule change is removed.
- Keep active Skills compact and traceable to the Wiki pattern or impact entry
  that motivated the change.
- Do not treat full-Wiki access during normal task execution as validation of a
  Skill; it can mask whether the compact Skill actually works.
- Reject a candidate when it regresses a previously passing fixed case or lacks
  coverage for the affected behavior.
- Retire noisy, obsolete, or contradicted feedback instead of accumulating it.

## Output

Return a concise review packet containing: source feedback, diagnosis, target,
minimal change, why it generalizes, regression cases, verification result,
risks, and the proposed state. The final decision belongs to the human owner.
