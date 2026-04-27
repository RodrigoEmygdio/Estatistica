Refine the current bundle-planning logic inside the Code Writer Stage so that inter-bundle dependencies become deterministic, conservative, and semantically valid for the demo MVP.

Context:

- The current bundle-based writer direction is correct
- However, the current dependency logic between bundles is too weak and is producing semantically invalid or artificial dependencies
- We want the smallest safe correction
- We do NOT want a broad redesign of the codegen stage
- We do NOT want a self-evolving dependency graph inferred primarily from generated code
- We want a deterministic MVP bundle graph driven mainly by orchestration rules

Goal:
Correct the bundle dependency logic so that:

- bundle dependencies are created only when justified by deterministic orchestration rules
- design/traceability may validate or enrich relationships, but not invent them alone
- generated signatures are used only for downstream contract propagation after generation, not as the primary source of graph construction

1. Scope of this correction

Implement only:

- correction of inter-bundle dependency planning
- explicit conservative dependency rules
- safer cycle handling
- alignment of generated-signatures usage with the new role

Do NOT implement:

- broad redesign of the writer
- full dependency graph inference from generated code
- new semantic retrieval
- new parser infrastructure unless already present and trivial
- redesign of pre-codegen

2. Required dependency-source priority

Use this priority order for bundle dependency planning:

Primary source

Deterministic orchestration rules:

- target type / layer rules
- pre-codegen authorized targets
- package-inference resolved targets
- explicit planned relationships when present

Secondary source

Design + traceability:

- may validate intended functional relationships
- may enrich known relationships
- must NOT invent dependency edges by themselves

Tertiary source

Generated signatures:

- may be used only after a bundle is generated
- may provide public contract context for later bundle prompts
- must NOT be the primary source of bundle graph creation for the demo

3. Forbidden dependency heuristics

Do NOT create bundle dependencies based only on:

- bundle order
- block order
- bounded-context coincidence
- naming similarity
- “previous bundle” fallback
- loose artifact-type guess without explicit deterministic rule

4. Minimum safe bundle dependency rule

A bundle may depend on another bundle only if at least one of these is true:

A. Deterministic layer/type rule

The current bundle contains target types that are explicitly allowed to depend on target types from the other bundle according to MVP orchestration rules.

For the demo MVP, use a conservative layering model such as:

- application-service may depend on:
  - domain-service
  - repository
  - model / dto / value object
- domain-service may depend on:
  - repository
  - model / value object
- repository / adapter may depend on:
  - model / query-support artifacts
- model / dto / value object should not depend on higher layers

Keep this strict and minimal.

B. Explicit planned relationship

There is an explicit planned relationship already available in orchestrator artifacts and it can be mapped deterministically to another generated target/bundle.

C. Generated-contract propagation for later prompts

After an earlier bundle is generated, its signatures may be propagated as prompt context to a later bundle that is already known to depend on it by rules A or B.
This propagation must not itself create a new dependency edge.

5. Bundle planning artifact behavior

Refine "codegen-bundle-plan.json" so that for each bundle:

- "dependsOnBundles" contains only justified edges
- "generatedDependencies" contains only artifacts that are truly needed from already-generated bundles
- "reusedDependencies" remains unchanged for existing-codebase reuse context

Do not inflate dependency lists.

6. Generated-signatures role correction

If "generated-signatures.json" already exists or is being produced:

- keep it
- but use it only to pass normalized public contracts to later bundles
- do not use it to invent bundle dependencies from simple FQN/string matching alone

7. Cycle policy

If bundle dependency planning detects a cycle:

- do NOT abort the entire stage by default
- mark the affected bundle(s) as guarded / "manual_review_required"
- emit a warning/report entry
- continue with remaining safe bundles when possible

Do not silently ignore cycles.

8. Determinism requirements

Maintain determinism in:

- bundle ordering
- dependency ordering
- generatedDependencies ordering
- JSON field names
- pretty-printing
- cycle reporting

Stable ordering is mandatory.

9. Acceptance criteria

This correction is complete only if:

- semantically weak artificial dependencies are no longer created
- dependency edges come only from justified deterministic rules
- generated-signatures are no longer misused as the primary graph source
- cycle handling is conservative and explicit
- no broad redesign is introduced
- the bundle-based writer remains demo-viable

10. Required output after changes

After applying the correction, return a concise summary with exactly these sections:

Bundle Dependency Logic Corrected

Files updated

Dependency rules implemented

Forbidden heuristics removed

Generated-signature role corrected

Cycle handling implemented

What was intentionally left unchanged

11. Final instruction

Make the smallest safe correction that turns the current bundle dependency planning into a deterministic, conservative, demo-safe MVP model.

Do not redesign the whole writer.
Do not depend primarily on generated-code scanning.
Do not create artificial dependency edges.