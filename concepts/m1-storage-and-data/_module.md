# M1: Storage, Data & State

> **Bedrock:** OSTEP (Persistence), AOSA (SQLite, HDFS), MIT 6.824 (GFS, Bigtable, Dynamo), Chip Huyen (AI Engineering)

What every concept in this module must emphasize (DEEP_DIVE reads this):

- **Mechanics:** How it works on disk, in memory, over the network
- **Failure modes:** Crash mid-write, torn pages, split-brain replicas, compaction stalls, hot keys
- **Tradeoffs:** Read vs. write vs. space amplification; durability vs. latency (fsync)
- **AI-era bridge:** Vector indexes, RAG freshness, agent long-term memory, checkpointing agent state

| Id | Concept | Roadmap week |
|---|---|---|
| c01 | Write-Ahead Logs (WAL) & Crash Recovery | 6 |
| c02 | B-Trees vs. LSM-Trees (Read/Write/Space Amplification) | 13 |
| c03 | Partitioning, Sharding & Consistent Hashing | 14 |
| c04 | Vector Indexes (HNSW/IVF) & Hybrid Agent Memory | 29 |
