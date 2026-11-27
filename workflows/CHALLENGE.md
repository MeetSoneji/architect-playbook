# CHALLENGE <id | design>

**Interactive only. Never scheduled.** This is the step where understanding is tested, so the
person being challenged is Meet, not the notes.

Claude acts as a Staff/Principal engineer running a design review. Tone: direct, specific, fair.

## Steps

1. **Teach-back first.** Ask Meet to explain the concept (or describe their design) in their own words,
   without looking at `notes.md`. Record it verbatim in `review.md` → *Teach-back*.
2. **Attack.** Ask 6–10 questions, one at a time, escalating. Always cover the ones that apply:
   - Tail latency: what happens at p99 / p99.9, and under 10x load?
   - Partial failure: crash between step N and N+1? Who notices, and how?
   - Split-brain / stale leaders / clock skew.
   - Idempotency: what if this runs twice? What if the ack is lost?
   - Retry storms and amplification across layers.
   - Backpressure: where does the queue live when the consumer is slow?
   - LLM-specific: cost and loop bounds, non-deterministic retries, tool side effects, context limits.
   - "Which real incident in part 5 would your design have prevented, and which would still hit you?"
   Judge each answer: *holds*, *partial*, or *breaks*, with one sentence why.
3. **Gaps.** List what was missing and the follow-up for each (fix notes, extend lab, INGEST question).
4. **Verdict.** `pass` when no answer *breaks* and the teach-back covers mechanics, a failure mode, and
   a tradeoff. Otherwise `revise`, and run CHALLENGE again later.
5. Write `review.md` from `templates/review.md`. Only if Meet agrees with a `pass`, set
   `stage = "mastered"`. Run `validate`, `status`, and open PR `challenge/<id>-<slug>`.

## Free-form design review

`/challenge` with a design instead of an id runs steps 2–3 against that design and writes the result to
`inbox/reports/design-review-YYYY-MM-DD-<topic>.md`. No stage changes.
