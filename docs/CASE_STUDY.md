# Bootstrap Case Study

This case verifies the two bootstrap paths that matter most: adopting the
harness in an existing project and starting from an empty directory.

## Existing Project

The fixture begins with a custom `AGENTS.md` and no harness memory files.

```powershell
python tools/bootstrap.py --project .case-study/existing
python tools/bootstrap.py --project .case-study/existing
```

Observed behavior:

- first run: five missing memory files are created and the existing
  `AGENTS.md` is skipped;
- second run: zero files are created and all six project files are skipped;
- the SHA-256 hash of the custom `AGENTS.md` is unchanged across both runs.

This is the migration contract: adoption fills missing structure without
replacing project-specific instructions.

## Empty Project

The fixture begins as an empty directory.

```powershell
python tools/bootstrap.py --project .case-study/empty
python tools/bootstrap.py --project .case-study/empty
```

Observed behavior:

- first run: all six project files are created;
- second run: zero files are created and all six files are skipped;
- the resulting project contains `AGENTS.md`, progress, corrections, learned
  rules, and both Wiki entry files.

## Skill Installation

Running with `--skills-dir` creates both included Skill directories on the
first run and skips them on the second run. The unit test
`tests/test_bootstrap.py` enforces this behavior in CI.

## Verification

The case was executed on Windows with Python 3.11. GitHub Actions independently
repeats unit tests, rule-health checks, and a clean bootstrap smoke test on
Python 3.11 and Python 3.14.
