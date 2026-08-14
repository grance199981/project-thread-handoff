import unittest
from pathlib import Path

from validate_handoff import validate_text


REQUIRED = (
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


def valid_document() -> str:
    sections = {
        "Metadata": "- Project root: `D:\\\\Research\\\\Demo`\n- Generated: 2026-08-14T16:00:00-07:00\n- Source task: task-123\n- Mode: export\n- Skill version: 1.0.0",
        "Approval and Safety Boundaries": "- Approved for project-local writes.\n- GPU launches require fresh authorization.",
        "Current Objective": "Verify the existing experiment before continuing.",
        "Verified State": "- Git state verified from local repository at 2026-08-14T16:00:00-07:00.",
        "Git and Worktrees": "- Branch: `main`\n- HEAD: `0123456789abcdef`\n- Worktree: clean",
        "Completed Work": "- Baseline tests passed; evidence: `reports/baseline.txt`.",
        "Active Local and Remote Work": "- No active local or remote work.",
        "Evidence and Results": "- Preliminary accuracy is stored in `results/summary.json`.",
        "Decisions and Invariants": "- Keep the registered evaluation protocol unchanged.",
        "Hypotheses and Evidence Gaps": "- Hypothesis: the new gate improves robustness; not yet tested.",
        "Risks and Stop Criteria": "- Stop if validation accuracy regresses by more than 2 pp.",
        "Pending Work": "1. Verify the held-out evaluation configuration.",
        "Recommended Next Step": "Read-only verify `results/summary.json` against the registered protocol.",
        "Import Verification": "Status: awaiting takeover.",
    }
    body = ["# Project Handoff"]
    for heading in REQUIRED:
        body.extend((f"## {heading}", "", sections[heading], ""))
    return "\n".join(body)


class ValidateHandoffTests(unittest.TestCase):
    def test_valid_document_passes(self):
        self.assertEqual(validate_text(valid_document()), [])

    def test_missing_heading_fails(self):
        text = valid_document().replace("## Pending Work\n", "")
        self.assertTrue(any("missing heading: Pending Work" in x for x in validate_text(text)))

    def test_duplicate_heading_fails(self):
        text = valid_document() + "\n## Verified State\nDuplicate"
        self.assertTrue(any("duplicate heading: Verified State" in x for x in validate_text(text)))

    def test_unresolved_placeholder_fails(self):
        text = valid_document().replace("Verify the existing experiment", "TODO verify experiment")
        self.assertTrue(any("placeholder" in x for x in validate_text(text)))

    def test_oversized_document_fails(self):
        text = valid_document() + ("x" * 31_000)
        self.assertTrue(any("size limit" in x for x in validate_text(text)))

    def test_remote_claim_requires_timestamp(self):
        text = valid_document().replace("No active local or remote work.", "Remote PID 1234 is running on server2.")
        self.assertTrue(any("volatile state" in x for x in validate_text(text)))

    def test_multiple_recommended_steps_fail(self):
        text = valid_document().replace(
            "Read-only verify `results/summary.json` against the registered protocol.",
            "1. Verify the summary.\n2. Launch training.",
        )
        self.assertTrue(any("exactly one" in x for x in validate_text(text)))

    def test_inherited_authorization_language_fails(self):
        text = valid_document().replace(
            "GPU launches require fresh authorization.",
            "All previous authorization automatically transfers to the new task.",
        )
        self.assertTrue(any("authorization" in x for x in validate_text(text)))

    def test_credential_pattern_fails(self):
        text = valid_document().replace(
            "Status: awaiting takeover.",
            "Status: awaiting takeover.\napi_key=sk-abcdefghijklmnopqrstuvwxyz123456",
        )
        self.assertTrue(any("credential" in x for x in validate_text(text)))

    def test_rendered_template_shape_passes(self):
        template_path = Path(__file__).resolve().parents[1] / "assets" / "HANDOFF.template.md"
        text = template_path.read_text(encoding="utf-8")
        replacements = {
            "{{PROJECT_ROOT}}": "D:\\\\Research\\\\Demo",
            "{{GENERATED_AT_ISO8601}}": "2026-08-14T16:00:00-07:00",
            "{{SOURCE_TASK_ID}}": "task-456",
            "{{APPROVAL_AND_SAFETY}}": "- Project-local writes approved.\n- Remote writes require fresh authorization.",
            "{{CURRENT_OBJECTIVE}}": "Verify the registered baseline.",
            "{{VERIFIED_STATE_WITH_EVIDENCE}}": "- Local Git state verified at 2026-08-14T16:00:00-07:00.",
            "{{GIT_AND_WORKTREES}}": "- Branch: `main`\n- Worktree: clean",
            "{{COMPLETED_WORK}}": "- Baseline implementation committed as `0123456`.",
            "{{ACTIVE_WORK_WITH_TIMESTAMPS}}": "- No active local or remote work.",
            "{{EVIDENCE_AND_RESULTS}}": "- Results are recorded in `results.json`.",
            "{{DECISIONS_AND_INVARIANTS}}": "- Preserve the registered split.",
            "{{HYPOTHESES_AND_GAPS}}": "- Generalization remains unverified.",
            "{{RISKS_AND_STOP_CRITERIA}}": "- Stop on data leakage.",
            "{{PENDING_WORK}}": "1. Audit the evaluation manifest.",
            "{{ONE_RECOMMENDED_NEXT_STEP}}": "Read-only audit the evaluation manifest.",
        }
        for marker, value in replacements.items():
            text = text.replace(marker, value)
        self.assertEqual(validate_text(text), [])


if __name__ == "__main__":
    unittest.main()
