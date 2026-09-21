"""Static health checks for global, project, and Skill instruction files."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    message: str


def _resolve(raw: str, base: Path) -> Path:
    expanded = os.path.expandvars(raw.replace("${USERPROFILE}", os.environ.get("USERPROFILE", "")))
    path = Path(expanded)
    return path if path.is_absolute() else base / path


def _read(path: Path, findings: list[Finding]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        findings.append(Finding("missing-file", str(path), str(exc)))
        return ""


def _frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line[:1].isspace():
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"\'')
    return result


def _bullets(text: str) -> set[str]:
    values = set()
    for line in text.splitlines():
        match = re.match(r"^\s*[-*]\s+(.+?)\s*$", line)
        if match:
            value = re.sub(r"\s+", " ", match.group(1)).strip().casefold()
            if len(value) >= 40:
                values.add(value)
    return values


def check_manifest(manifest_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        manifest: dict[str, Any] = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [Finding("invalid-manifest", str(manifest_path), str(exc))]

    base = manifest_path.parent
    global_path = _resolve(manifest["global_agents"], base)
    project_paths = [_resolve(item, base) for item in manifest.get("project_agents", [])]
    document_paths = [global_path, *project_paths]
    documents = {path: _read(path, findings) for path in document_paths}

    global_text = documents.get(global_path, "")
    for marker in manifest.get("specialized_global_markers", []):
        if marker.casefold() in global_text.casefold():
            findings.append(
                Finding("specialized-global-rule", str(global_path), f"specialized marker found: {marker}")
            )

    skill_names: set[str] = set()
    skill_paths: list[Path] = []
    for entry in manifest.get("skills", []):
        expected_name = entry["name"]
        path = _resolve(entry["path"], base)
        skill_names.add(expected_name)
        skill_paths.append(path)
        text = _read(path, findings)
        if not text:
            continue
        if not entry.get("validate_metadata", True):
            continue
        metadata = _frontmatter(text)
        if metadata.get("name") != expected_name:
            findings.append(
                Finding("skill-name-mismatch", str(path), f"expected {expected_name!r}, got {metadata.get('name')!r}")
            )
        description = metadata.get("description", "")
        if len(description) < 50 or "use" not in description.casefold():
            findings.append(Finding("vague-description", str(path), "description lacks a concrete positive trigger"))
        if "do not use" not in description.casefold():
            findings.append(Finding("missing-description-boundary", str(path), "description lacks a negative boundary"))
        if entry.get("require_scope"):
            scope_match = re.search(r"^## Scope\s*$([\s\S]*?)(?=^## |\Z)", text, re.MULTILINE)
            scope = scope_match.group(1) if scope_match else ""
            if not scope_match or "use when" not in scope.casefold():
                findings.append(Finding("missing-positive-scope", str(path), "Scope must contain 'Use when'"))
            if "do not use" not in scope.casefold():
                findings.append(Finding("missing-negative-scope", str(path), "Scope must contain 'Do not use'"))

    all_texts = dict(documents)
    validated_skill_paths = {
        _resolve(entry["path"], base)
        for entry in manifest.get("skills", [])
        if entry.get("validate_metadata", True)
    }
    for path in skill_paths:
        if path not in validated_skill_paths:
            continue
        if path not in all_texts:
            all_texts[path] = _read(path, findings)
    owners: dict[str, list[str]] = defaultdict(list)
    for path, text in all_texts.items():
        for bullet in _bullets(text):
            owners[bullet].append(str(path))
    for bullet, paths in owners.items():
        if len(paths) > 1:
            findings.append(
                Finding("duplicate-rule", " | ".join(paths), f"duplicated bullet: {bullet[:120]}")
            )

    cases_path = _resolve(manifest["routing_cases"], base)
    try:
        cases = json.loads(cases_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        findings.append(Finding("invalid-routing-cases", str(cases_path), str(exc)))
        return findings

    seen_ids: set[str] = set()
    for index, case in enumerate(cases):
        case_path = f"{cases_path}#{index}"
        case_id = case.get("id")
        if not case_id or case_id in seen_ids:
            findings.append(Finding("duplicate-case-id", case_path, f"invalid or duplicate id: {case_id!r}"))
        seen_ids.add(case_id)
        expected = set(case.get("expected_skills", []))
        excluded = set(case.get("must_not_load", []))
        overlap = expected & excluded
        unknown = (expected | excluded) - skill_names
        if overlap:
            findings.append(Finding("contradictory-case", case_path, f"skills both expected and excluded: {sorted(overlap)}"))
        if unknown:
            findings.append(Finding("unknown-skill", case_path, f"unregistered skills: {sorted(unknown)}"))
        if not str(case.get("request", "")).strip():
            findings.append(Finding("empty-request", case_path, "routing case request is empty"))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path("rule_health_manifest.json"))
    parser.add_argument("--json", action="store_true", help="emit machine-readable findings")
    args = parser.parse_args()
    findings = check_manifest(args.manifest.resolve())
    if args.json:
        print(json.dumps([asdict(item) for item in findings], ensure_ascii=False, indent=2))
    elif findings:
        for item in findings:
            print(f"{item.code}: {item.path}: {item.message}")
    else:
        print("Rule health check passed.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
