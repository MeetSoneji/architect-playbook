# M5: Network, Caching & Edge

> **Bedrock:** AOSA (nginx), System Design Primer, ByteByteGo System Design 101

What every concept in this module must emphasize (DEEP_DIVE reads this):

- **Mechanics:** epoll/kqueue event loops, connection pooling, eviction policies
- **Failure modes:** Thundering herd, cache stampede, stale reads, head-of-line blocking
- **Tradeoffs:** Memory cost vs. hit rate; TTL freshness vs. origin load
- **AI-era bridge:** Semantic caching, prompt-prefix caching, SSE/WebSocket token streaming gateways

| Id | Concept | Roadmap week |
|---|---|---|
| c17 | Event Loops, Reverse Proxies & L4/L7 Load Balancing | 11 |
| c18 | Cache Patterns, Invalidation & Thundering Herd | 12 |
| c19 | Semantic Caching, Prompt-Prefix Caching & SSE Streaming | 26 |
