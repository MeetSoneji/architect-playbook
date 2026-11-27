# BUILD_LAB <id>

Goal: a lab where you **watch the failure happen**, then watch the mechanism prevent it.
Stage: `drafted → proven`. Input: `notes.md` §7 (lab spec).

## The lab contract (enforced by `playbook.py validate`)

```
concepts/<module>/<id>-<slug>/lab/
  README.md          # Invariant · Failure injected · How to run · What you should observe
  <name>.py          # the mechanism, minimal, readable, stdlib only
  test_<name>.py     # unittest, stdlib only, deterministic (seeded randomness, no sleeps > 1 s)
```

`test_<name>.py` must contain both:
- `test_simulate_failure_*` — the **negative control**. The naive version (no WAL, no idempotency key,
  no jitter…) is run under the fault and the test asserts that the invariant **is violated**.
  If this test cannot fail the naive version, the lab proves nothing.
- `test_recovery_*` — the same fault, the real mechanism, and the test asserts the invariant **holds**.

## Steps

1. Read `notes.md` §1, §2, §7. Pick the smallest model that shows the mechanism honestly. Simulate
   the fault in-process (fake disk with a crash-at-byte hook, a fake network that drops/duplicates/reorders,
   a fake clock) so tests are deterministic and run in CI in seconds.
2. Write the naive implementation and the real one side by side so the diff *is* the lesson.
3. Write the tests. Run `python3 tools/playbook.py labs <id>` until green.
4. Prove the negative control works: temporarily break the mechanism and confirm `test_recovery_*` fails.
   Note in the README which line you broke.
5. README "What you should observe": include actual output from a run.
6. If building the lab revealed something the notes got wrong, fix `notes.md` in the same PR and say so.
7. Set `stage = "proven"`, `validate`, `status`, open PR `build-lab/<id>-<slug>`.
