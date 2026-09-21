# Contributing

Keep changes small, evidence-backed, and portable.

1. Add or update a fixed case for behavior changes.
2. Run `python -m unittest discover -s tests -v`.
3. Run `python tools/check_rule_health.py`.
4. Confirm that no personal paths, credentials, account identifiers, or local
   runtime artifacts were added.

Do not add a global rule from a single anecdote. Prefer a project-local note or
proposal until the behavior repeats or a fixed evaluation supports promotion.
