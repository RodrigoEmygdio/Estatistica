Goal:
Assess whether the current existing codebase inventory artifacts are strong enough to safely support a minimal downstream code generation stage without causing incorrect reuse decisions.

Context:

- The migration pipeline already reaches:
  - diagnosis
  - traceability
  - design
  - design-validator
  - codebase-verification
- The "codebase-verification-report.json" quality has improved
- Current residual risk appears to originate partly from the evidence quality of the inventory artifacts
- We do NOT want a general review of the whole pipeline now
- We want a focused assessment of whether the inventory layer itself is strong enough for minimal downstream codegen use

Important constraints:

- Do NOT implement code
- Do NOT modify files
- Do NOT redesign the architecture
- Do NOT expose internal source code
- Focus only on the quality, completeness, and downstream safety of the current inventory artifacts

1. Review targets

Review internally:

- repository-inventory.json
- service-inventory.json
- entity-inventory.json
- adapter-inventory.json
- query-inventory.json
- search-fallback.json if present

Also review only as needed:

- the current "codebase-verification-report.json"
- the inventory schema contracts
- the current extraction/output structure of Step 1A

2. Core question

Are the current inventory artifacts strong enough to support a minimal codegen stage that needs to decide whether to:

- reuse existing artifacts
- extend existing artifacts
- or create new artifacts

without being misled by weak or incomplete evidence?

3. Evaluation criteria

Evaluate specifically:

A. Inventory completeness

- Do the inventories cover the minimum required evidence for repositories, services, entities, adapters, and queries?
- Are there major blind spots that would cause downstream false negatives or false positives?

B. Identity strength

- Are inventory items identifiable enough through fields like:
  - name
  - fullyQualifiedName
  - filePath
  - packageName
  - sourceKind
- Is there enough structural identity to support reuse decisions safely?

C. Dependency and query usefulness

- Is query-inventory strong enough to help distinguish true repository/query reuse from superficial name similarity?
- Are extracted method signatures or query-bearing methods reliable enough for a conservative demo?

D. Adapter/service/repository separation

- Are adapters, services, and repositories distinguished clearly enough?
- Could the current inventories cause codegen to reuse the wrong artifact category?

E. False-positive reuse risk

- Where could the current inventory make the matcher/report overestimate reuse?
- Which missing fields or weak extraction areas are most dangerous?

F. False-negative / over-conservative risk

- Where is the inventory too weak, causing viable reuse/extension opportunities to be missed?
- Are these acceptable for a minimal demo?

G. Minimal codegen readiness

- If a minimal codegen stage consumed the current inventory indirectly through the verification report, what inventory weaknesses would still be true blockers?
- Which weaknesses can be tolerated if codegen uses guarded/manual rules?

4. Required response format

Return exactly this structure:

Inventory Readiness for Minimal Codegen

1. Overall status

State one of:

- READY FOR MINIMAL CODEGEN
- READY FOR MINIMAL CODEGEN WITH GUARDED USE
- NOT READY FOR CODEGEN

2. What is already strong in the inventory layer

3. Current weak points in the inventory layer

4. False-positive reuse risk areas caused by inventory weakness

5. False-negative / over-conservative areas caused by inventory weakness

6. Real blockers before codegen

7. What can be safely deferred until after 07/05

8. Final recommendation

5. Final discipline

- Focus on the inventory layer as evidence source
- Be conservative
- Do not redesign the pipeline
- Do not provide patch code
- Review only