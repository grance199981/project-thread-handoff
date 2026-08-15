# Project Thread Handoff

[English](README.md) | [简体中文](README_zh.md)

`project-thread-handoff` is a Codex Skill for moving a long-running project from an old task into a fresh one without copying the entire conversation history.

It creates a compact, evidence-backed `.codex/HANDOFF.md` snapshot, then requires the receiving task to verify that snapshot against the current project before continuing.

## Why use it?

Long Codex tasks can accumulate tool output, terminal logs, file changes, worktree state, remote experiments, and stale assumptions. A conversational summary alone is easy to trust too much and difficult to audit.

This Skill provides a two-phase handoff:

1. **Export** — inspect the source project, generate and validate `.codex/HANDOFF.md`, and commit it safely when permitted.
2. **Import** — independently verify Git, worktrees, project evidence, and explicitly referenced remote work before recommending one next step.

## Features

- Separates verified facts, inferences, hypotheses, and unverified claims.
- Records Git branches, commits, worktrees, and user-owned modifications.
- Preserves project approval gates and safety boundaries.
- Prevents one-time authorization from silently transferring to a new task.
- Restricts remote verification to read-only checks for work already in scope.
- Detects stale HEADs, missing jobs, conflicting state, and unverifiable claims.
- Keeps handoffs under 30 KB by linking to canonical logs and project files.
- Includes a dependency-free validator and unit tests.

## Repository layout

```text
.
├── README.md
├── README_zh.md
├── LICENSE
├── .github/workflows/test.yml
└── project-thread-handoff/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── assets/HANDOFF.template.md
    └── scripts/
        ├── validate_handoff.py
        └── test_validate_handoff.py
```

The nested `project-thread-handoff/` directory is the complete installable Skill package.

## Installation

### PowerShell

```powershell
git clone https://github.com/grance199981/project-thread-handoff.git
Copy-Item -Recurse -Force `
  .\project-thread-handoff\project-thread-handoff `
  "$HOME\.codex\skills\project-thread-handoff"
```

### Bash

```bash
git clone https://github.com/grance199981/project-thread-handoff.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R project-thread-handoff/project-thread-handoff \
  "${CODEX_HOME:-$HOME/.codex}/skills/project-thread-handoff"
```

Restart Codex if the Skill does not appear immediately.

## Usage

Export the current project from an old task:

```text
Use $project-thread-handoff to export this project for a fresh Codex task.
```

Verify and take over the project in a new task:

```text
Use $project-thread-handoff to import and verify this project's .codex/HANDOFF.md. Do not continue until I confirm the takeover report.
```

The export workflow writes:

```text
<project-root>/.codex/HANDOFF.md
```

The document captures the current objective, evidence, Git state, completed and active work, decisions, risks, pending work, and exactly one recommended next step. The importing task classifies material claims as **Consistent**, **Stale**, **Conflicting**, or **Unverifiable**.

## Safety model

- Applicable `AGENTS.md` instructions and project approval gates are checked before writes.
- Existing project files and handoff content are treated as data, not higher-priority instructions.
- User changes are never cleaned, reset, overwritten, or staged silently.
- Downloads, remote writes, GPU launches, messages, and destructive actions require authorization under the receiving task's current rules.
- Remote checks are read-only and limited to work explicitly identified in the project.
- Secrets, full logs, full diffs, chat transcripts, and large source blocks are excluded from the handoff.

The Skill does not guarantee application memory release, scientific correctness, approval validity, or remote-job liveness. It provides a structured process for checking those claims.

## Validation

Run the validator tests:

```bash
cd project-thread-handoff/scripts
python -m unittest -v test_validate_handoff.py
```

Validate a rendered handoff:

```bash
python project-thread-handoff/scripts/validate_handoff.py /path/to/project/.codex/HANDOFF.md
```

The raw template intentionally fails validation because it contains replacement markers. Only a fully rendered handoff should pass.

## Development

Keep the installable package minimal. It should contain exactly five files:

```text
SKILL.md
agents/openai.yaml
assets/HANDOFF.template.md
scripts/validate_handoff.py
scripts/test_validate_handoff.py
```

Before proposing a change:

1. Update tests first for validator behavior.
2. Run the complete unit-test suite.
3. Verify the package contains no caches, credentials, logs, or machine-specific state.
4. Keep export/import behavior aligned with the safety model above.

## License

MIT © 2026 grance199981. See [LICENSE](LICENSE).
