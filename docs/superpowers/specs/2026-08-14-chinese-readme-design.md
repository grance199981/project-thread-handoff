# Chinese README Design

**Date:** 2026-08-14  
**Status:** Approved

## Goal

Add a complete Simplified Chinese mirror of the public English README without changing Skill behavior, installation layout, tests, or CI semantics.

## Files

- Add root `README_zh.md` as the complete Chinese mirror.
- Add a language switch at the top of `README.md` linking to `README_zh.md`.
- Add a language switch at the top of `README_zh.md` linking to `README.md`.

## Translation Rules

- Preserve the English README section order and technical meaning.
- Keep command blocks, file paths, filenames, Skill name, prompts, and code identifiers unchanged unless explanatory prose requires Chinese punctuation.
- Translate safety boundaries precisely; do not weaken approval, remote-read-only, authorization, Git, or worktree constraints.
- Preserve disclaimers about memory release, scientific correctness, approval validity, and remote-job liveness.
- Use natural technical Chinese rather than literal machine translation.

## Verification

- Both language links resolve to tracked files.
- Heading structures remain aligned.
- Installation and validation commands remain executable equivalents.
- Existing 10 validator tests and Skill validation continue to pass.
- Commit and push only the two README changes.
