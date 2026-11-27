# M2: Distributed Coordination & Consistency

> **Bedrock:** Mixu, Tanenbaum & van Steen 4e, MIT 6.824 (Raft), Kleppmann

What every concept in this module must emphasize (DEEP_DIVE reads this):

- **Mechanics:** State machines, quorums, logical clocks, leases
- **Failure modes:** Network partitions, GC pauses breaking leases, stale leaders, clock skew
- **Tradeoffs:** Consistency vs. availability vs. latency
- **AI-era bridge:** Concurrent multi-agent state mutations, conflicting tool calls, shared memory races

| Id | Concept | Roadmap week |
|---|---|---|
| c05 | Physical vs. Logical & Vector Clocks | 18 |
| c06 | CAP, PACELC & Linearizability vs. Eventual Consistency | 19 |
| c07 | Consensus (Raft / Paxos) & Leader Election | 20 |
| c08 | Distributed Locks, Leases & Fencing Tokens | 22 |
