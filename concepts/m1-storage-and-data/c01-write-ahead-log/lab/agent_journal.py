"""The AI bridge: an agent that journals its steps like a database journals its writes.

A four-step "refund agent" calls an LLM, charges a payment API, sends an email, and calls the LLM again.
The process can die right after any side effect, before the agent has recorded it (the worst moment).

NaiveAgent restarts from step 1.  JournaledAgent writes an intent record before each step and a result
record after it, using the WalStore from wal.py, and resumes from its journal.
"""
from __future__ import annotations

import json

from wal import Crash, FakeDisk, WalStore

STEPS = [("plan", "llm"), ("refund", "payment"), ("notify", "email"), ("summarize", "llm")]


class World:
    """Everything outside the agent: paid LLM calls and side-effecting tools. Survives agent crashes."""

    def __init__(self, crash_after_ops: int | None = None):
        self.llm_calls = 0
        self.refunds: list[str] = []          # what the customer's bank actually sees
        self.emails: list[str] = []
        self.seen_keys: dict[str, str] = {}   # payment API idempotency keys (see c10)
        self.ops, self.crash_after = 0, crash_after_ops

    def _tick(self):
        self.ops += 1
        if self.crash_after is not None and self.ops == self.crash_after:
            raise Crash()                     # the side effect happened; the agent never heard back

    def call(self, step: str, kind: str, key: str | None) -> str:
        if kind == "llm":
            self.llm_calls += 1
            out = f"llm-output-for-{step}"
        elif kind == "payment":
            if key and key in self.seen_keys:  # retry with the same key: same answer, no new charge
                return self.seen_keys[key]
            self.refunds.append("refund $40")
            out = "refund-id-881"
            if key:
                self.seen_keys[key] = out
        else:
            self.emails.append("your refund is on its way")
            out = "email-sent"
        self._tick()
        return out


class NaiveAgent:
    def __init__(self, disk: FakeDisk, world: World, run_id: str):
        self.world = world

    def run(self) -> None:
        for step, kind in STEPS:
            self.world.call(step, kind, key=None)


class JournaledAgent:
    """Write-ahead rule for agents: record what you are about to do, do it, record what happened."""

    def __init__(self, disk: FakeDisk, world: World, run_id: str):
        self.journal, self.world, self.run_id = WalStore(disk), world, run_id

    def run(self) -> None:
        for i, (step, kind) in enumerate(STEPS):
            done = self.journal.data.get(f"done:{i}")
            if done is not None:
                continue                                    # replay: reuse the recorded result, no call
            key = f"{self.run_id}:{i}"                      # same key on every attempt of this step
            self.journal.set(f"intent:{i}", json.dumps({"step": step, "key": key}))
            result = self.world.call(step, kind, key=key)
            self.journal.set(f"done:{i}", json.dumps({"result": result}))


def crash_and_resume(agent_cls, crash_after_ops: int) -> World:
    """Run once with a crash after the Nth side effect, then restart the agent and let it finish."""
    disk, world = FakeDisk(), World(crash_after_ops)
    try:
        agent_cls(disk, world, "run-42").run()
    except Crash:
        pass
    world.crash_after = None
    agent_cls(disk.reboot(), world, "run-42").run()
    return world
