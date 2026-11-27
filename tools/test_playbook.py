"""Self-tests for the scheduler and gates, so automation logic can't silently regress."""
import copy
import datetime as dt
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import playbook  # noqa: E402


def reg_with(**stages):
    reg = copy.deepcopy(playbook.load())
    for cid, st in stages.items():
        reg["by_id"][cid]["stage"] = st
    return reg


def flows(items):
    return [(i["workflow"], i["concept"]) for i in items if i["workflow"] != "INGEST"]


class TestNext(unittest.TestCase):
    def setUp(self):
        self.wk1 = playbook.load()["schedule"]["start"]

    def test_nothing_before_week_one(self):
        self.assertEqual(flows(playbook.next_items(reg_with(), self.wk1 - dt.timedelta(days=1))), [])

    def test_week_one_starts_first_concept(self):
        self.assertEqual(flows(playbook.next_items(reg_with(), self.wk1)), [("DEEP_DIVE", "c01")])

    def test_finishes_before_starting(self):
        items = flows(playbook.next_items(reg_with(c01="drafted"), self.wk1 + dt.timedelta(weeks=1)))
        self.assertEqual(items[0], ("BUILD_LAB", "c01"))
        self.assertIn(("DEEP_DIVE", "c09"), items)

    def test_wip_limit_is_backpressure(self):
        items = flows(playbook.next_items(reg_with(c01="proven", c09="proven"), self.wk1 + dt.timedelta(weeks=3)))
        self.assertNotIn("DEEP_DIVE", [w for w, _ in items])
        self.assertIn(("BLOCKED_BY_WIP", "c10"), items)

    def test_mastered_gets_published_never_challenged_by_automation(self):
        items = flows(playbook.next_items(reg_with(c01="mastered"), self.wk1))
        self.assertIn(("PUBLISH", "c01"), items)
        self.assertNotIn("CHALLENGE", [w for w, _ in items])


class TestGates(unittest.TestCase):
    def test_current_repo_is_valid(self):
        errs, _ = playbook.validate(playbook.load())
        self.assertEqual(errs, [])

    def test_drafted_without_notes_is_rejected(self):
        errs, _ = playbook.validate(reg_with(c02="drafted"))
        self.assertTrue(any("c02" in e and "notes.md" in e for e in errs))

    def test_c01_lab_satisfies_lab_contract(self):
        reg = playbook.load()
        self.assertEqual(playbook.check_lab(reg["by_id"]["c01"]), [])


if __name__ == "__main__":
    unittest.main()
