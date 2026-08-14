from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_HEADINGS = (
    "Metadata",
    "Approval and Safety Boundaries",
    "Current Objective",
    "Verified State",
    "Git and Worktrees",
    "Completed Work",
    "Active Local and Remote Work",
    "Evidence and Results",
    "Decisions and Invariants",
    "Hypotheses and Evidence Gaps",
    "Risks and Stop Criteria",
    "Pending Work",
    "Recommended Next Step",
    "Import Verification",
)
DEFAULT_MAX_BYTES = 30_000
TIMESTAMP_RE = re.compile(
    r"\b20\d{2}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})\b"
)
PLACEHOLDER_RE = re.compile(
    r"\b(?:TBD|TODO|FIXME)\b|\{\{[^}]+\}\}|<[^>]+>", re.IGNORECASE
)
VOLATILE_RE = re.compile(
    r"\b(?:remote|server|host|pid|gpu|cuda|running|training|job)\b", re.IGNORECASE
)
CREDENTIAL_RE = re.compile(
    r"(?:api[_-]?key|access[_-]?token|secret|password)\s*[:=]\s*[^\s`]+|sk-[A-Za-z0-9_-]{20,}",
    re.IGNORECASE,
)
INHERITED_AUTH_RE = re.compile(
    r"(?:all|any)\s+(?:previous|prior|old)\s+authori[sz]ation\s+(?:automatically\s+)?transfers?",
    re.IGNORECASE,
)


def section_text(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def recommended_item_count(section: str) -> int:
    numbered = re.findall(r"^\s*\d+[.)]\s+\S", section, re.MULTILINE)
    bullets = re.findall(r"^\s*[-*]\s+\S", section, re.MULTILINE)
    if numbered or bullets:
        return len(numbered) + len(bullets)
    paragraphs = [
        paragraph.strip()
        for paragraph in re.split(r"\n\s*\n", section)
        if paragraph.strip()
    ]
    return len(paragraphs)


def validate_text(text: str, max_bytes: int = DEFAULT_MAX_BYTES) -> list[str]:
    errors: list[str] = []
    if len(text.encode("utf-8")) > max_bytes:
        errors.append(f"document exceeds size limit of {max_bytes} bytes")

    if not re.search(r"^# Project Handoff\s*$", text, re.MULTILINE):
        errors.append("missing title: Project Handoff")

    for heading in REQUIRED_HEADINGS:
        count = len(
            re.findall(rf"^## {re.escape(heading)}\s*$", text, re.MULTILINE)
        )
        if count == 0:
            errors.append(f"missing heading: {heading}")
        elif count > 1:
            errors.append(f"duplicate heading: {heading}")
        elif not section_text(text, heading):
            errors.append(f"empty section: {heading}")

    metadata = section_text(text, "Metadata")
    if "Project root:" not in metadata:
        errors.append("Metadata must include Project root")
    if not TIMESTAMP_RE.search(metadata):
        errors.append("Metadata must include an ISO-8601 timestamp with timezone")

    for heading in ("Verified State", "Active Local and Remote Work"):
        section = section_text(text, heading)
        if VOLATILE_RE.search(section) and not TIMESTAMP_RE.search(section):
            if "No active local or remote work" not in section:
                errors.append(f"volatile state in {heading} requires a timestamp")

    recommendation = section_text(text, "Recommended Next Step")
    if recommendation and recommended_item_count(recommendation) != 1:
        errors.append("Recommended Next Step must contain exactly one item")

    if PLACEHOLDER_RE.search(text):
        errors.append("document contains an unresolved placeholder")
    if INHERITED_AUTH_RE.search(text):
        errors.append("document claims previous authorization automatically transfers")
    if CREDENTIAL_RE.search(text):
        errors.append("document contains a possible credential")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a project handoff document.")
    parser.add_argument("path", type=Path)
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES)
    args = parser.parse_args(argv)

    try:
        text = args.path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: cannot read {args.path}: {exc}", file=sys.stderr)
        return 2

    errors = validate_text(text, max_bytes=args.max_bytes)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"PASS: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
