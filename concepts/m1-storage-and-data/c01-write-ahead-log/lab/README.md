# c01 lab · Write-Ahead Logs (WAL) & Crash Recovery

Two experiments. `wal.py` is the classic one: a key-value store on a disk that loses power. `agent_journal.py`
is the AI bridge: a refund agent that crashes mid-run and has to resume without refunding twice.

## Invariant
- **Store:** every write acknowledged to the client is readable after a power loss at **any** byte offset, and
  no torn or corrupted record is ever applied.
- **Agent:** after a crash at any step and a restart, the customer is refunded exactly once and no completed
  LLM call is paid for again.

## Failure injected
`FakeDisk(crash_after=N)` persists bytes in order and loses power after byte `N`. The tests sweep `N` over
every offset of the whole workload (7 writes), so every possible torn write is tried. One extra test flips a
byte inside a fully written record to model silent corruption.

`World(crash_after_ops=N)` kills the agent right after its Nth side effect (LLM call, refund, email) and
**before** it can record the result, which is the worst possible moment. The tests try every N.

## How to run
```bash
python3 -m unittest -v                  # from this folder; stdlib only
python3 tools/playbook.py labs c01      # from the repo root
```

## What you should observe
```
test_simulate_failure_naive_agent_double_refunds_after_crash ...
  naive agent, crash after refund:     refunds=2  llm_calls=3
ok
test_recovery_journaled_agent_refunds_once_at_every_crash_point ...
  journaled agent, crash after refund: refunds=1  llm_calls=2
ok
test_recovery_needs_both_journal_and_idempotency_key ... ok
test_recovery_wal_checksum_stops_at_corrupted_record ... ok
test_recovery_wal_keeps_every_acknowledged_write_at_every_crash_point ...
  wal: 0 of 230 crash points lose acked data
ok
test_recovery_wal_truncates_torn_tail_and_keeps_writing ... ok
test_simulate_failure_naive_rewrite_loses_acknowledged_writes ...
  naive: 634 of 664 crash points lose acked data; worst: crash at byte 514 loses 6 of 6 acked keys
ok
```

- **The naive store** destroys the old state (`truncate`) before the new state exists (`append`). A crash in
  that window loses everything ever acknowledged, not just the last write.
- **The WAL store** never overwrites: it only appends `[length][crc32][payload]`. On reboot it replays records
  until the first short or checksum-failing one, then truncates that tail. The worst a crash can do is drop
  the one write that was never acknowledged.
- **The naive agent** restarts from step 1: it pays for the planning LLM call again and refunds the customer
  a second time.
- **The journaled agent** writes `intent:i` before each step and `done:i` after it. On restart, steps with a
  `done` record are skipped and their saved result is reused. A step with only an `intent` record *may* have
  run, so it is retried with the **same idempotency key**, and the payment API answers "already done".
- `test_recovery_needs_both_journal_and_idempotency_key` shows why the key matters: with the journal but
  without the key, the in-flight refund still happens twice. The journal tells you *what might have
  happened*; only the downstream system can tell you *what did*. That handoff is concept c10.
- The email tool has no idempotency key, so a crash right after sending the email sends it twice. That is
  the honest limit: for a tool without a key, "at least once" is the best a journal can do.
- Break it on purpose: in `WalStore._recover`, delete the `zlib.crc32(body) != crc` check and the
  corruption test fails: recovery trusts the bytes and dies decoding them (`UnicodeDecodeError`). With a
  luckier flip it would silently apply a wrong value instead, which is worse.
- Notice the naive numbers: 634 of 664 crash points lose acknowledged data, because almost every byte of a
  rewrite sits inside the "old state gone, new state incomplete" window.

## Extensions to try
1. Model the page cache: writes go to a volatile buffer and only `fsync()` makes them durable. Acknowledge
   before fsync and watch the recovery test fail (this is the classic "fsync lies" bug class).
2. Add a checkpoint (snapshot + truncate log) and crash in the middle of the checkpoint.
3. Give the email tool an idempotency key and make the email assertion `== 1` at every crash point.
