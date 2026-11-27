"""Proof by failure for the AI bridge: crash a refund agent after each side effect, then resume it.

Invariant: the customer is refunded exactly once, and completed LLM calls are never paid for twice
(at most the one in-flight step is retried).
"""
import unittest

from agent_journal import STEPS, JournaledAgent, NaiveAgent, crash_and_resume

LLM_STEPS = sum(kind == "llm" for _, kind in STEPS)


class TestAgentJournal(unittest.TestCase):
    def test_simulate_failure_naive_agent_double_refunds_after_crash(self):
        """Negative control: restart-from-scratch repeats every side effect before the crash."""
        world = crash_and_resume(NaiveAgent, crash_after_ops=2)   # dies right after the refund
        self.assertEqual(len(world.refunds), 2)
        self.assertEqual(world.llm_calls, LLM_STEPS + 1)
        print(f"\n  naive agent, crash after refund:     refunds={len(world.refunds)}  llm_calls={world.llm_calls}")

    def test_recovery_journaled_agent_refunds_once_at_every_crash_point(self):
        for n in range(1, len(STEPS) + 1):
            with self.subTest(crash_after_ops=n):
                world = crash_and_resume(JournaledAgent, n)
                self.assertEqual(len(world.refunds), 1)
                self.assertLessEqual(world.llm_calls, LLM_STEPS + 1)   # only the in-flight step repeats
                self.assertEqual(len(world.emails), 1 if STEPS[n - 1][1] != "email" else 2)
        world = crash_and_resume(JournaledAgent, 2)
        print(f"\n  journaled agent, crash after refund: refunds={len(world.refunds)}  llm_calls={world.llm_calls}")

    def test_recovery_needs_both_journal_and_idempotency_key(self):
        """The journal alone is not enough: the refund ran, but its 'done' record never made it to disk."""
        from agent_journal import World
        from wal import FakeDisk

        disk, world = FakeDisk(), World(crash_after_ops=2)
        agent = JournaledAgent(disk, world, "run-42")
        try:
            agent.run()
        except Exception:
            pass
        world.crash_after = None
        world.seen_keys.clear()                  # pretend the payment API ignores idempotency keys
        JournaledAgent(disk.reboot(), world, "run-42").run()
        self.assertEqual(len(world.refunds), 2)  # the intent record says "maybe", and maybe means retry


if __name__ == "__main__":
    unittest.main()
