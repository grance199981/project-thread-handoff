# Project Thread Handoff GitHub Publication Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the validated local Skill into a documented, tested public repository and push `main` to `grance199981/project-thread-handoff`.

**Architecture:** Keep publication files at the repository root and the installable Skill in a nested `project-thread-handoff/` directory. Copy the five validated installed files byte-for-byte, add public documentation, MIT licensing and cross-platform CI, then verify content and push a dedicated Git history.

**Tech Stack:** Markdown, YAML, Python 3 standard library, `unittest`, Git, GitHub Actions, GitHub CLI.

---

### Task 1: Create the publication-facing repository files

**Files:**
- Create: `README.md`
- Create: `LICENSE`
- Create: `.gitignore`

- [ ] **Step 1: Create README.md**

Write a concise README containing: purpose, export/import model, feature list, repository layout, installation commands for PowerShell and Bash, export/import prompts, validation commands, safety boundaries, development commands, and MIT license notice.

The README must use `project-thread-handoff/` as the directory users copy into their Codex skills root and must not claim guaranteed memory release, scientific correctness, approval validity, or remote liveness.

- [ ] **Step 2: Create the MIT license**

Use the standard MIT license text with:

```text
Copyright (c) 2026 grance199981
```

- [ ] **Step 3: Create .gitignore**

Use:

```gitignore
__pycache__/
*.py[cod]
.pytest_cache/
.coverage
htmlcov/
.DS_Store
Thumbs.db
.idea/
.vscode/
```

- [ ] **Step 4: Commit publication documentation**

Run:

```powershell
git add README.md LICENSE .gitignore
git commit -m "docs: add public repository documentation"
```

Expected: one commit containing only the three root publication files.

### Task 2: Add the installable Skill package

**Files:**
- Create: `project-thread-handoff/SKILL.md`
- Create: `project-thread-handoff/agents/openai.yaml`
- Create: `project-thread-handoff/assets/HANDOFF.template.md`
- Create: `project-thread-handoff/scripts/validate_handoff.py`
- Create: `project-thread-handoff/scripts/test_validate_handoff.py`

- [ ] **Step 1: Copy the five validated source files**

Copy each file byte-for-byte from:

```text
C:\Users\zijia\.codex\skills\project-thread-handoff
```

into the nested package. Do not copy caches, test fixtures, design documents, or machine-specific metadata.

- [ ] **Step 2: Verify exact source parity**

Run PowerShell SHA-256 comparisons for all five files. Expected: every installed/published pair has the same hash.

- [ ] **Step 3: Run the package unit tests**

Run:

```powershell
python -m unittest -v test_validate_handoff.py
```

from `project-thread-handoff/scripts`.

Expected: 10 tests pass.

- [ ] **Step 4: Run standard Skill validation**

Run:

```powershell
python C:\Users\zijia\.codex\skills\.system\skill-creator\scripts\quick_validate.py `
  D:\Doctor\杂七杂八\project-thread-handoff\project-thread-handoff
```

Expected: `Skill is valid!`

- [ ] **Step 5: Commit the package**

Run:

```powershell
git add project-thread-handoff
git commit -m "feat: publish project thread handoff skill"
```

Expected: only the five package files are committed.

### Task 3: Add cross-platform continuous integration

**Files:**
- Create: `.github/workflows/test.yml`

- [ ] **Step 1: Create the workflow**

Use this workflow:

```yaml
name: test

on:
  push:
  pull_request:

permissions:
  contents: read

jobs:
  validate:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Run validator tests
        working-directory: project-thread-handoff/scripts
        run: python -m unittest -v test_validate_handoff.py
      - name: Check package structure
        shell: python
        run: |
          from pathlib import Path
          root = Path("project-thread-handoff")
          expected = {
              Path("SKILL.md"),
              Path("agents/openai.yaml"),
              Path("assets/HANDOFF.template.md"),
              Path("scripts/validate_handoff.py"),
              Path("scripts/test_validate_handoff.py"),
          }
          actual = {path.relative_to(root) for path in root.rglob("*") if path.is_file()}
          if actual != expected:
              raise SystemExit(f"unexpected package files: {sorted(actual ^ expected)}")
          text = (root / "SKILL.md").read_text(encoding="utf-8")
          if not text.startswith("---\nname: project-thread-handoff\n"):
              raise SystemExit("invalid SKILL.md frontmatter")
```

- [ ] **Step 2: Run the workflow's structure check locally**

Execute the same Python structure check from the repository root. Expected: exit code 0.

- [ ] **Step 3: Check the YAML for obvious syntax and secret issues**

Inspect the complete workflow and search the repository for API keys, tokens, passwords, private paths, caches and logs. Expected: no sensitive values or unwanted files.

- [ ] **Step 4: Commit CI**

Run:

```powershell
git add .github/workflows/test.yml
git commit -m "ci: test skill on Windows and Ubuntu"
```

### Task 4: Perform final local release verification

**Files:**
- Verify all tracked files

- [ ] **Step 1: Run tests and Skill validation again**

Expected: 10 unit tests pass and standard Skill validation succeeds.

- [ ] **Step 2: Verify repository scope**

Run:

```powershell
git status --short
git ls-files
git log --oneline --decorate -5
```

Expected: clean working tree; only approved repository files are tracked; intentional commit history is present.

- [ ] **Step 3: Add and verify the remote**

Run:

```powershell
git remote add origin https://github.com/grance199981/project-thread-handoff.git
git remote -v
```

If `origin` already exists, verify it exactly matches the approved repository before changing anything.

### Task 5: Install GitHub CLI and publish main

**Files:**
- No repository file changes expected

- [ ] **Step 1: Install GitHub CLI with user approval**

Because `gh` is missing, request approval and run:

```powershell
winget install --id GitHub.cli --exact --source winget
```

Expected: GitHub CLI installs successfully. If unavailable, stop and ask the user to install it; do not use browser file-by-file upload.

- [ ] **Step 2: Verify authentication**

Run:

```powershell
gh auth status
```

If not authenticated, start `gh auth login` and let the user complete any browser/device authorization. Re-run `gh auth status` before pushing.

- [ ] **Step 3: Verify the remote repository**

Run:

```powershell
gh repo view grance199981/project-thread-handoff `
  --json nameWithOwner,url,visibility,defaultBranchRef,isEmpty
```

Expected: the repository is public, belongs to `grance199981`, and is empty or has no conflicting commit history.

- [ ] **Step 4: Push main**

Run:

```powershell
git push -u origin main
```

Expected: `main` is pushed and tracks `origin/main`.

- [ ] **Step 5: Verify the published repository**

Run:

```powershell
gh repo view grance199981/project-thread-handoff --web
git status -sb
```

Also verify through the GitHub API/CLI that the default branch is `main` and the latest remote commit equals local HEAD. Report the repository URL, HEAD commit, validation results, and any CI status that is already available.

## Self-Review

- Spec coverage: repository structure, README, MIT license, nested Skill purity, CI, source parity, local validation, dedicated Git history, remote verification and push are covered.
- Scope: this plan publishes one already-implemented Skill and does not change its semantics.
- Safety: only the dedicated repository is staged; remote identity is verified before push; browser file upload is excluded.
- Placeholders: no implementation placeholders remain.
