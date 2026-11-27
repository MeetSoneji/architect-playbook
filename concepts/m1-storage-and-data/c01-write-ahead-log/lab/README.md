# c01 lab · Write-Ahead Logs (WAL) & Crash Recovery

> Built ahead of the c01 DEEP_DIVE as the reference example of the lab contract. DEEP_DIVE c01 should
> align its §7 lab spec with this lab, or extend it.

## Invariant
Every write acknowledged to the client is readable after a power loss at **any** byte offset, and no
torn or corrupted record is ever applied.

## Failure injected
`FakeDisk(crash_after=N)` persists bytes in order and loses power after byte `N`. The tests sweep `N` over
every offset of the whole workload (7 writes), so every possible torn write is tried. One extra test flips a
byte inside a fully written record to model silent corruption.

## How to run
```bash
python3 -m unittest -v                  # from this folder; stdlib only
python3 tools/playbook.py labs c01      # from the repo root
```

## What you should observe
```
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
- Break it on purpose: in `WalStore._recover`, delete the `zlib.crc32(body) != crc` check and the
  corruption test fails: recovery trusts the bytes and dies decoding them (`UnicodeDecodeError`). With a
  luckier flip it would silently apply a wrong value instead, which is worse.
- Notice the naive numbers: 634 of 664 crash points lose acknowledged data, because almost every byte of a
  rewrite sits inside the "old state gone, new state incomplete" window.

## Extensions to try
1. Model the page cache: writes go to a volatile buffer and only `fsync()` makes them durable. Acknowledge
   before fsync and watch the recovery test fail (this is the classic "fsync lies" bug class).
2. Add a checkpoint (snapshot + truncate log) and crash in the middle of the checkpoint.
3. AI bridge: make each record an agent step result (`step_id`, tool output). Resume an agent after a crash
   without re-calling the LLM for completed steps.
