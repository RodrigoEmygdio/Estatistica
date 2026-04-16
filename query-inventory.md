Goal:
Refine the existing query-inventory implementation and define the minimum safe hardening required so it becomes useful enough for the golden-path demo.

Context:

- The migration pipeline already has working stages up to "codebase-verification"
- The current weakest evidence area is "query-inventory.json"
- Current observed problems:
  - it does not capture methods reliably enough
  - it misses relevant repositories/services that contain HQL/JPQL
  - it is too weak to support conservative reuse decisions for data-access artifacts
- We do NOT want a redesign of the whole inventory layer
- We do NOT want a full-blown query analysis engine
- We want the minimum safe improvement needed for the demo golden path

Important constraints:

- Do NOT implement code
- Do NOT modify files
- Do NOT redesign the pipeline
- Do NOT propose semantic embeddings or complex retrieval
- Focus only on refining the current query-inventory extraction strategy

1. Review targets

Review internally:

- the existing Step 1A query-inventory extraction logic
- the current "query-inventory.json"
- the relevant inventory contracts/docs
- the current verification/codebase report only as needed to understand downstream impact

2. Objective

Determine the smallest set of practical improvements that would make "query-inventory.json" materially more useful for a conservative golden-path demo.

3. Questions to answer

Evaluate and decide:

A. Method extraction

What minimum method-level metadata must be captured so query-bearing artifacts become useful for downstream reuse verification?

B. Query source detection

Which query-bearing sources must be recognized for the demo MVP?
Evaluate at least:

- "@Query"
- "EntityManager"
- "JdbcTemplate"
- "NamedParameterJdbcTemplate"
- inline HQL/JPQL strings in repositories/services/adapters

C. HQL/JPQL coverage

What minimum static detection of HQL/JPQL is sufficient for the demo?
Do not aim for completeness. Aim for useful minimum coverage.

D. Output usefulness

What fields are strictly necessary in "query-inventory.json" so later matching can distinguish:

- real query reuse candidates
- plain method names
- infrastructure wrappers
- weak/noisy hits

E. Non-goals

What should explicitly be left for after the demo?

4. Required response format

Return exactly this structure:

Query Inventory Hardening Plan

1. Overall conclusion

State one of:

- MINIMAL HARDENING IS ENOUGH
- HARDENING IS NEEDED BUT MUST STAY VERY NARROW
- CURRENT APPROACH IS TOO WEAK FOR DEMO

2. Current critical weaknesses

3. Minimum improvements required now

4. Query sources that must be detected for the demo

5. Minimum fields that query-inventory must expose

6. What can be safely deferred until after 07/05

7. Safe implementation guidance for Qwen

8. Final recommendation

5. Final discipline

- Be pragmatic
- Be conservative
- Focus on the golden path
- Do not redesign the extractor family
- Prefer small high-value improvements