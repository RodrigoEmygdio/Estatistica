Goal:
Generate a minimal correction prompt for Qwen that replaces the current flawed bundle-planning basis with a simpler, demo-safe phase-based bundle planning model.

Context:

- The current "codegen-bundle-plan.json" is not reliable enough
- Bundles are still being grouped in a way that produces artificial or inflated "dependsOnBundles"
- Application-service bundles are ending up with large meaningless dependency lists
- The current problem is no longer just prompt noise; the bundle-plan itself is weak
- For the demo MVP, we need a smaller and more deterministic execution model
- We do NOT want a full redesign of the writer or pipeline
- We want the smallest structural correction that makes the bundle plan usable

Important constraints:

- Do NOT implement code
- Do NOT redesign the whole pipeline
- Do NOT broaden into advanced dependency graph inference
- Generate only a correction prompt for Qwen

1. Required correction target

Generate a correction prompt for Qwen that does the following:

A. Replace the current dependency-heavy bundle plan basis

Do not treat the current broad "dependsOnBundles" generation as the foundation to preserve.

B. Introduce a phase-based execution plan for the demo MVP

Build bundle planning primarily from deterministic artifact phases/layers:

1. "model-dto-phase"
   
   - DomainModel
   - DTO
   - ValueObject
   - Projection / supporting model artifacts

2. "repository-phase"
   
   - Repository
   - Query-support
   - Adapter / data-access artifacts

3. "domain-service-phase"
   
   - DomainService

4. "application-service-phase"
   
   - ApplicationService

C. Build bundles within each phase conservatively

- only include "generate_new" targets
- group small related targets within the same phase
- do not rely on boundedContext alone
- do not mix unrelated layers in the same bundle

D. Restrict dependencies by phase

For the demo MVP:

- model/dto phase -> no higher-layer dependencies
- repository phase -> may depend only on model/dto/query-support artifacts
- domain-service phase -> may depend only on repository phase and model phase
- application-service phase -> may depend only on domain-service phase, repository phase, and model phase

E. No artificial dependency edges

Do NOT create dependency edges based only on:

- same bounded context
- bundle order
- block order
- naming similarity
- “all possible layer-to-layer edges”

F. Minimal "dependsOnBundles"

A bundle should depend only on bundles from earlier phases that are actually required by the phase rules and explicit target relationships.
If there is no clear dependency, leave "dependsOnBundles" empty.

G. Keep prompt/context logic secondary

The goal of this correction is first to produce a sane "codegen-bundle-plan.json".
Prompt simplification can remain secondary and must consume the corrected plan.

2. Required response format

Return exactly this structure:

Qwen Phase-Based Bundle Plan Correction Prompt

<full correction prompt text only>3. Final discipline

- Keep the correction minimal
- Replace the flawed bundle-plan basis, not the whole writer
- Prefer deterministic phase-based planning over noisy dependency graphs
- Optimize for a demo-safe happy path