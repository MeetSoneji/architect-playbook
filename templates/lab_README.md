# {{id}} lab · {{title}}

## Invariant
<!-- FILL: One sentence, testable. e.g. "Every write acknowledged to the client survives a crash at any byte offset." -->

## Failure injected
<!-- FILL: The exact fault and where it is injected: kill mid-write at byte N, drop every 3rd packet,
     deliver each message twice, upstream returns 429 for 5 s. -->

## How to run
```bash
python3 -m unittest -v          # from this folder; stdlib only
python3 tools/playbook.py labs {{id}}   # from the repo root
```

## What you should observe
<!-- FILL: What the negative-control test (test_simulate_failure_*) shows breaking, what the
     recovery test (test_recovery_*) shows holding, and which lines of code make the difference. -->
