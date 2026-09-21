"""Install the self-evolution harness without overwriting existing files."""

from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class InstallResult:
    created: tuple[Path, ...]
    skipped: tuple[Path, ...]


def _copy_missing(source: Path, destination: Path, created: list[Path], skipped: list[Path]) -> None:
    if destination.exists():
        skipped.append(destination)
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    created.append(destination)


def bootstrap(project: Path, skills_dir: Path | None = None) -> InstallResult:
    root = Path(__file__).resolve().parents[1]
    template_root = root / "templates"
    project = project.resolve()
    project.mkdir(parents=True, exist_ok=True)

    created: list[Path] = []
    skipped: list[Path] = []
    project_files = {
        template_root / "AGENTS.project.md": project / "AGENTS.md",
        template_root / "memory" / "progress.md": project / "memory" / "progress.md",
        template_root / "memory" / "corrections.md": project / "memory" / "corrections.md",
        template_root / "memory" / "learned_rules.md": project / "memory" / "learned_rules.md",
        template_root / "memory" / "wiki" / "index.md": project / "memory" / "wiki" / "index.md",
        template_root / "memory" / "wiki" / "skill_impact.md": project / "memory" / "wiki" / "skill_impact.md",
    }
    for source, destination in project_files.items():
        _copy_missing(source, destination, created, skipped)

    if skills_dir is not None:
        skills_dir = skills_dir.resolve()
        for source in sorted((root / "skills").iterdir()):
            destination = skills_dir / source.name
            if destination.exists():
                skipped.append(destination)
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source, destination)
            created.append(destination)

    return InstallResult(tuple(created), tuple(skipped))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path, help="project directory to initialize")
    parser.add_argument("--skills-dir", type=Path, help="optional Codex-compatible Skill directory")
    args = parser.parse_args()

    result = bootstrap(args.project, args.skills_dir)
    for path in result.created:
        print(f"created: {path}")
    for path in result.skipped:
        print(f"skipped: {path}")
    print(f"Bootstrap complete: {len(result.created)} created, {len(result.skipped)} skipped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
