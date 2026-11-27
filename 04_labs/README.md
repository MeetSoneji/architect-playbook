# Hands-On Systems Labs

Every concept mastered in `02_living_kb/` should have a small, runnable prototype here proving how it works under the hood (and how it fails).

## Naming Convention
`<module_num>_<concept_slug>/` (e.g., `01_wal_crash_recovery/`, `03_idempotent_tool_queue/`, `04_circuit_breaker_llm/`)

Each lab directory should include:
- `README.md` — What invariant it proves, how to run it, and what failure mode it simulates.
- Clean, minimal runnable code (Python/Go/TypeScript).
- A test or simulation script demonstrating the failure & recovery.
