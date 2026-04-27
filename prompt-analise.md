Goal:
Review the current Code Writer direction and determine whether it should be refactored so that:

- bundle generation is planned explicitly before writing,
- inter-bundle dependencies are provided explicitly,
- newly generated artifacts expose normalized signatures for downstream bundles,
- and the writer returns to using the existing canonical prompt as its fixed base.

Context:

- The current writer direction is evolving toward bundle-based generation
- This is the right direction for the demo, but there is a risk of turning the writer into an ad hoc stateful system
- We want a controlled solution:
  - explicit bundle planning
  - explicit dependency context
  - incremental generated-signature capture
  - canonical-prompt-based writer composition
- The coding model created its own custom prompt instead of using the canonical prompt base
- We want to validate whether this should be corrected now

Important constraints:

- Do NOT implement code
- Do NOT modify files
- Do NOT redesign the whole pipeline
- Do NOT propose broad runtime statefulness
- Focus only on this writer-model refinement

1. Core question

Should the Code Writer architecture for the demo be refined so that:

1. bundle generation is first planned explicitly in a "codegen-bundle-plan.json"
2. each bundle includes:
   - targets to generate
   - reused dependency context
   - generated dependency context from earlier bundles
3. newly generated artifacts produce normalized signatures persisted in a "generated-signatures.json"
4. the actual writer prompt uses the existing canonical prompt as a fixed base instead of an ad hoc prompt invented by the coding model

2. Questions to decide

A. Bundle planning

Is an explicit "codegen-bundle-plan.json" the right minimum mechanism for the demo?

B. Inter-bundle dependency handling

Should dependencies on already-existing artifacts and newly-generated artifacts be represented explicitly and separately?

C. Generated signature propagation

Is a "generated-signatures.json" artifact the safest MVP way to pass newly created contracts to later bundles?

D. Canonical prompt discipline

Should the writer be forced back to:

- canonical fixed prompt base
  plus
- orchestrator-assembled bundle payload

instead of a custom free-form prompt created by the coding model?

E. Demo viability

Does this refinement keep the happy path realistic for this week, or does it risk overcomplicating the demo?

3. Required response format

Return exactly this structure:

Code Writer Bundle-Planning Review

1. Overall conclusion

State one of:

- KEEP CURRENT WRITER MODEL
- REFINE WRITER WITH BUNDLE PLAN AND GENERATED SIGNATURES
- CURRENT WRITER NEEDS A DIFFERENT ADJUSTMENT

2. Why the current direction is or is not sufficient

3. Whether explicit bundle planning is required

4. Whether generated-signatures.json is the right MVP artifact

5. Whether the writer must return to canonical prompt usage

6. Risks of doing this now

7. Risks of not doing this now

8. Final recommendation

4. Final discipline

- Be pragmatic
- Be conservative
- Optimize for a demo-safe happy path
- Do not redesign the whole product
- Focus on the smallest structural refinement that prevents writer chaos