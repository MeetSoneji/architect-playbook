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
        self.reg = playbook.load()
        self.day1 = self.reg["schedule"]["start"]
        self.first = min(self.reg["concepts"], key=lambda c: c["seq"])["id"]

    def test_nothing_before_first_release(self):
        self.assertEqual(flows(playbook.next_items(reg_with(), self.day1 - dt.timedelta(days=1))), [("NOT_YET", self.first)])

    def test_first_release_starts_seq_1(self):
        self.assertEqual(flows(playbook.next_items(reg_with(), self.day1)), [("CONCEPT", self.first)])

    def test_two_releases_a_week_on_schedule_days(self):
        dates = playbook.release_dates(self.reg)
        order = sorted(self.reg["concepts"], key=lambda c: c["seq"])
        days = {playbook.DAY_NAMES[dates[c["id"]].weekday()] for c in order}
        self.assertEqual(days, set(self.reg["schedule"]["days"]))
        self.assertEqual((dates[order[2]["id"]] - dates[order[0]["id"]]).days, 7)

    def test_serial_skips_in_flight_branch(self):
        order = sorted(self.reg["concepts"], key=lambda c: c["seq"])
        later = self.day1 + dt.timedelta(days=30)
        items = flows(playbook.next_items(reg_with(), later, in_flight={order[0]["id"]}))
        self.assertEqual(items, [("CONCEPT", order[1]["id"])])

    def test_finishes_drafted_before_starting_new(self):
        self.assertEqual(flows(playbook.next_items(reg_with(c02="drafted"), self.day1)), [("PUBLISH", "c02")])

    def test_backpressure_when_meet_has_not_merged(self):
        items = playbook.next_items(reg_with(), self.day1 + dt.timedelta(days=60), in_flight={"c23", "c25", "c24", "c26"})
        self.assertEqual([i["workflow"] for i in items if i["workflow"] != "INGEST"], ["WAITING_ON_MEET"])

    def test_published_is_never_redone(self):
        reg = reg_with(**{c["id"]: "published" for c in self.reg["concepts"]})
        self.assertEqual(flows(playbook.next_items(reg, self.day1 + dt.timedelta(days=999))), [])


class TestGates(unittest.TestCase):
    def test_current_repo_is_valid(self):
        errs, _ = playbook.validate(playbook.load())
        self.assertEqual(errs, [])

    def test_drafted_without_notes_is_rejected(self):
        errs, _ = playbook.validate(reg_with(c02="drafted"))
        self.assertTrue(any("c02" in e and "notes.md" in e for e in errs))

    def test_mastered_requires_review(self):
        reg = reg_with(c02="queued")
        reg["by_id"]["c02"]["mastered"] = True
        errs, _ = playbook.validate(reg)
        self.assertTrue(any("c02" in e and "review.md" in e for e in errs))

    def test_c01_optional_lab_satisfies_lab_contract(self):
        reg = playbook.load()
        self.assertEqual(playbook.check_lab(reg["by_id"]["c01"]), [])


if __name__ == "__main__":
    unittest.main()
