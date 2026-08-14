# Project Thread Handoff GitHub Publication Design

**Date:** 2026-08-14  
**Status:** Approved design; publication implementation not started

## Goal

Prepare and publish `project-thread-handoff` as a public, reusable GitHub repository while preserving the installed Codex Skill as a minimal, self-contained package.

## Repository Structure

```text
project-thread-handoff/
├── README.md
├── LICENSE
├── .gitignore
├── .github/
│   └── workflows/
│       └── test.yml
├── docs/
│   └── superpowers/
│       └── specs/
│           └── 2026-08-14-github-publication-design.md
└── project-thread-handoff/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    ├── assets/
    │   └── HANDOFF.template.md
    └── scripts/
        ├── validate_handoff.py
        └── test_validate_handoff.py
```

The repository root is publication-facing. The nested `project-thread-handoff/` directory is the installable Skill package and must contain no README, changelog, installation guide, or unrelated artifacts.

## README Scope

The root README will explain:

- the problem the Skill solves;
- its export/import handoff model;
- installation by copying or cloning the nested package into the Codex skills directory;
- concise export and import usage examples;
- `.codex/HANDOFF.md` structure and 30 KB size boundary;
- approval, Git, worktree, remote-read-only, and authorization non-transfer rules;
- local validation and testing commands;
- repository layout and contribution expectations.

The README must not claim that the Skill can guarantee application memory release, scientific correctness, approval validity, or remote-job liveness.

## License

Use the MIT License. Copyright holder: `grance199981`. Year: 2026.

## Continuous Integration

Add a GitHub Actions workflow that:

- runs on pushes and pull requests;
- tests on current Ubuntu and Windows runners;
- uses a supported Python 3 version;
- runs `unittest` for the validator suite;
- runs a lightweight package structure and YAML/frontmatter validation without requiring private local Codex paths.

The workflow must not download models, datasets, or invoke remote systems.

## Source of Truth and Copy Policy

The currently installed package at `C:\Users\zijia\.codex\skills\project-thread-handoff` is the source for the initial publication snapshot. Copy only the five validated package files into the nested repository package. Exclude caches, temporary fixtures, design scratch files, and machine-specific paths.

After publication, the GitHub repository becomes the development source of truth. Future changes should be developed and tested in the repository, then copied or installed into the local Codex skills directory.

## Git and Publication Strategy

- Initialize a dedicated Git repository at `D:\Doctor\杂七杂八\project-thread-handoff`.
- Use `main` as the branch.
- Add remote `https://github.com/grance199981/project-thread-handoff.git`.
- Stage only files in this dedicated repository.
- Run all tests before committing.
- Create an intentional initial publication commit.
- Push `main` to the already-created empty GitHub repository.

The current machine does not have GitHub CLI installed. Before publication, install and authenticate `gh`, or stop and request user action if installation/authentication cannot be completed safely. Do not fall back to uploading files one by one through the browser.

## Verification

Publication is complete only when:

1. the nested Skill contains exactly the five required files;
2. all validator unit tests pass locally;
3. the installed Skill and published package files match byte-for-byte at publication time;
4. repository metadata and remote URL are correct;
5. the initial commit is pushed to `main`;
6. GitHub shows the README, MIT license, and workflow;
7. no secrets, caches, personal logs, remote credentials, or research-project files are present.

## Non-Goals

- Publishing the design and implementation-plan workspace outside this repository.
- Packaging as a Python module or publishing to PyPI.
- Creating a GitHub Release in the initial publication.
- Adding telemetry, network access, or automatic remote-job control.
- Changing the already validated export/import semantics.
