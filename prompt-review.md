Goal:
Review the current bundle-planning implementation inside the Code Writer flow and determine why it is producing semantically weak or incorrect inter-bundle dependencies, then recommend the minimum deterministic correction.

Context:

- The Code Writer direction was updated toward bundle-based generation
- Bundle planning is now being generated inside the codegen stage
- The current implementation is producing bundle dependencies that do not make architectural sense
- We do NOT want a broad redesign of the whole codegen stage
- We want a focused review of the current bundle-planning logic and a minimal correction strategy

Important constraints:

- Do NOT implement code
- Do NOT modify files
- Do NOT redesign the whole pipeline
- Do NOT propose semantic embeddings or broad AI planning
- Focus only on the correctness of the current bundle dependency planning

1. Review targets

Review internally:

- the current bundle-planning implementation in the codegen stage
- the produced in-memory / persisted bundle structures if available
- the current pre-codegen decision table
- package inference entries as needed
- the relevant codegen contract docs only as needed

2. Core question

Why is the current implementation producing inter-bundle dependencies that do not make architectural sense, and what is the smallest safe deterministic correction?

3. Review criteria

Evaluate specifically:

A. Current dependency heuristic

- What rule is currently causing meaningless dependencies?
- Is it based too heavily on:
  - target order
  - block order
  - artifact type
  - boundedContext coincidence
  - naming similarity
    without real dependency evidence?

B. Architectural validity

- Which current bundle dependencies are structurally weak or unjustified?
- Are bundles depending on one another without a clear reason grounded in:
  - known design intent
  - explicit reuse/generation relationship
  - repository/service/model layering rules

C. Minimum safe dependency rule

- What should be the minimum deterministic rule for bundle dependencies in the demo?
- Should dependency creation be restricted to a smaller set of allowed patterns?

D. Safe MVP simplification

- Would it be safer for the demo to reduce bundle dependencies to:
  - layer ordering only
  - explicit known generated dependency edges only
  - or no dependency unless explicitly justified?

E. Correction scope

- What is the smallest correction that avoids nonsense dependencies without destabilizing the rest of the writer?

4. Required response format

Return exactly this structure:

Bundle Planning Dependency Review

1. Overall conclusion

State one of:

- CURRENT BUNDLE DEPENDENCY LOGIC IS ACCEPTABLE
- CURRENT BUNDLE DEPENDENCY LOGIC IS TOO WEAK AND NEEDS CORRECTION

2. Why the current dependencies do not make sense

3. What heuristic is currently wrong

4. Minimum safe dependency rule for the demo

5. What bundle dependencies should be forbidden

6. Minimal correction recommended

7. Risks if left unchanged

8. Final recommendation

5. Final discipline

- Be pragmatic
- Be conservative
- Prefer the smallest correction over redesign
- Focus on stopping semantically invalid bundle dependencies