Use a combination, with this priority order:

1. Primary driver: deterministic orchestration rules
   
   - target type / layer rules
   - pre-codegen authorized targets
   - package-inference resolved targets
   - explicit planned relationships when present

2. Secondary validator/enricher: design + traceability
   
   - use these to validate intended functional relationships
   - do not let them invent dependencies by themselves

3. Tertiary runtime enrichment only: generated signatures
   
   - use generated-signatures.json only after a bundle is generated
   - use it to provide downstream prompt context for later bundles
   - do NOT use it as the primary source to build the dependency graph for the demo MVP

For the demo, we want a deterministic and conservative bundle graph, not a self-evolving architecture derived from generated code.

Additional answers:

- Existing tooling: only use an existing parser/import extractor if it is already present, simple, and reliable. Do not make the MVP depend on building or introducing new parsing infrastructure for cross-bundle dependency inference.
- Cycle policy: do not abort the entire codegen stage by default. If a cycle is detected, mark the affected bundle(s) as "manual_review_required", emit a warning/report entry, and continue with the remaining safe bundles when possible.

The MVP rule should be:

- no dependency edge unless explicitly justified by deterministic orchestration logic
- no dependency edge based only on bundle order, bounded-context coincidence, block order, or naming similarity
- generated signatures are for contract propagation, not for inventing the graph