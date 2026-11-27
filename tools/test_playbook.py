"""Self-tests for the scheduler and gates, so automation logic can't silently regress."""
import copy
import datetime as dt
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import playbook  # noqa: E402


def reg_with(**stages):
    """A registry with every concept queued except the given ones, so tests don't depend on real progress."""
    reg = copy.deepcopy(playbook.load())
    for c in reg["concepts"]:
        c["stage"] = "queued"
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
        self.assertEqual(flows(playbook.next_items(reg_with(), self.wk1)), [("DEEP_DIVE", "c23")])

    def test_finishes_before_starting(self):
        items = flows(playbook.next_items(reg_with(c23="drafted"), self.wk1))
        self.assertEqual(items[0], ("BUILD_LAB", "c23"))
        self.assertIn(("DEEP_DIVE", "c25"), items)

    def test_wip_limit_is_backpressure(self):
        items = flows(playbook.next_items(reg_with(c23="proven", c25="proven"), self.wk1 + dt.timedelta(weeks=1)))
        self.assertNotIn("DEEP_DIVE", [w for w, _ in items])
        self.assertIn(("BLOCKED_BY_WIP", "c24"), items)

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
