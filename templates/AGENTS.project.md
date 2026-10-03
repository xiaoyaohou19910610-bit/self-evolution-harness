# AGENTS.md

## Project Sources

- Read `memory/progress.md` before resuming unfinished work.
- Record verified corrections in `memory/corrections.md`.
- Keep candidate lessons separate from active project rules.

## Long-Running Work

- For resumable or batch tasks, assign stable `run_id`, `item_id`, and
  `stage_id` values; persist a checkpoint after each completed stage. Resume
  only from read-back-verified checkpoints, preserve interrupted attempts, and
  report incomplete items as incomplete.
- Before dropping a recurring review or agent step, compare complete and reduced
  workflows on a fixed representative sample with the same acceptance criteria.
  Record quality, failures, observed token usage when available, and elapsed
  time; published savings are not local results.

## Completion

- Run checks proportional to the change.
- Report verified, partially verified, and unverified results distinctly.
- Remove temporary files created only for the current investigation.
