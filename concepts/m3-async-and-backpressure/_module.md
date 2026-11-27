# M3: Async Messaging & Backpressure

> **Bedrock:** Burns (Designing Distributed Systems), Amazon Builders' Library, Kreps (The Log)

What every concept in this module must emphasize (DEEP_DIVE reads this):

- **Mechanics:** Broker vs. log offsets, consumer groups, bounded buffers, acks
- **Failure modes:** Poison pills, consumer lag, duplicate deliveries, queue explosion
- **Tradeoffs:** Throughput vs. ordering vs. tail latency
- **AI-era bridge:** Slow, rate-limited LLM calls need durable async queues and idempotent tool execution

| Id | Concept | Roadmap week |
|---|---|---|
| c09 | Message Queues vs. Event Logs | 2 |
| c10 | Delivery Guarantees & Idempotency Keys | 3 |
| c11 | Backpressure, Bounded Queues & Dead Letter Queues | 6 |
| c12 | Durable Execution for Long-Running AI Agents | 24 |
