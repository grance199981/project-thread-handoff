# Chinese README Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a complete Simplified Chinese mirror of the public README and reciprocal language links.

**Architecture:** Keep English and Chinese documentation in separate root files with matching section order. Preserve all executable commands and safety semantics while translating explanatory prose naturally.

**Tech Stack:** Markdown, Python standard library for structural checks, Git, GitHub Actions.

---

### Task 1: Add reciprocal language navigation

**Files:**
- Modify: `README.md`
- Create: `README_zh.md`

- [ ] **Step 1: Add the English README language switch**

Immediately below the title, add:

```markdown
[English](README.md) | [简体中文](README_zh.md)
```

- [ ] **Step 2: Create the complete Chinese mirror**

Translate every English section in the same order. Preserve commands, paths, filenames, repository URL, Skill prompts, safety constraints, validation instructions, and MIT attribution.

- [ ] **Step 3: Add the Chinese README language switch**

Immediately below the Chinese title, add the same language links.

### Task 2: Verify documentation parity and existing behavior

**Files:**
- Verify: `README.md`
- Verify: `README_zh.md`
- Test: `project-thread-handoff/scripts/test_validate_handoff.py`

- [ ] **Step 1: Verify heading parity**

Use a Python script to compare the ordered count of level-two headings. Expected: both files have the same number and corresponding topic order.

- [ ] **Step 2: Verify reciprocal links and commands**

Check both language links resolve to tracked files. Confirm both READMEs contain the clone URL, export/import examples, unit-test command, validator command, and safety disclaimer.

- [ ] **Step 3: Run existing tests and Skill validation**

Run 10 unit tests and `quick_validate.py`. Expected: all pass.

- [ ] **Step 4: Commit the README changes**

Run:

```powershell
git add README.md README_zh.md
git commit -m "docs: add Simplified Chinese README"
```

### Task 3: Push and verify publication

**Files:**
- No additional file changes expected

- [ ] **Step 1: Push main**

Push the committed `main` branch to `origin` using the previously authenticated GitHub account.

- [ ] **Step 2: Verify remote HEAD and CI**

Confirm local and remote HEAD match, then wait for Windows and Ubuntu CI to pass.

- [ ] **Step 3: Verify GitHub rendering**

Confirm `README_zh.md` is visible on GitHub and the English README language link targets it.

## Self-Review

- The plan changes documentation only.
- Both languages preserve commands and safety semantics.
- Existing tests, Skill validation and CI remain required.
- No placeholders or unrelated changes are included.
