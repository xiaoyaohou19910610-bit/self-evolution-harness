# Self-Evolution Harness

A small, auditable harness for agents that need durable project context and a
controlled way to learn from verified mistakes.

It provides:

- file-first project continuity;
- two reusable Codex Skills;
- project memory templates;
- a rule-health checker with fixed routing cases;
- an idempotent bootstrap command;
- project guidance for stable IDs, resumable checkpoints, and evidence-based
  workflow changes;
- tests and CI with no runtime dependencies.

The harness does not let feedback rewrite active instructions automatically.
Lessons remain proposals until a human reviews and promotes them.

## Quick Start

Requires Python 3.11 or newer.

```powershell
git clone https://github.com/xiaoyaohou19910610-bit/self-evolution-harness.git
cd self-evolution-harness
python tools/bootstrap.py --project C:\path\to\your-project
python tools/check_rule_health.py
python -m unittest discover -s tests -v
```

Run the bootstrap command again at any time. Existing project files are never
overwritten.

## What Gets Installed

The project bootstrap adds missing files only:

```text
AGENTS.md
memory/
  corrections.md
  learned_rules.md
  progress.md
  wiki/
    index.md
    skill_impact.md
```

Use `--skills-dir` to install the included Skills into a separate Skill root:

```powershell
python tools/bootstrap.py \
  --project C:\path\to\your-project \
  --skills-dir C:\Users\you\.codex\skills
```

## Design Boundary

The inner loop completes normal project work. The outer loop captures a
correction, identifies the narrowest reusable lesson, adds a regression case,
and prepares a proposal. A human decides whether that proposal becomes an
active project rule, Skill change, or shared template.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the verification contract and
[SECURITY.md](SECURITY.md) for the trust boundary. A reproducible old-project
and empty-project walkthrough is available in
[docs/CASE_STUDY.md](docs/CASE_STUDY.md).

Project ownership and decision boundaries are documented in
[MAINTAINERS.md](MAINTAINERS.md) and [GOVERNANCE.md](GOVERNANCE.md).

## 中文说明

这是一个可审查的 Agent 自我进化脚手架。它把项目状态、纠错记录、规则提案和
回归检查放进项目文件，但不会让反馈自动修改生效中的规则。初始化脚本可重复运行，
默认只补齐缺失文件，不覆盖项目现有内容。

## License

MIT
