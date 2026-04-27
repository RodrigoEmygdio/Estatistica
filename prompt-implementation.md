Goal:
Generate a minimal correction prompt for Qwen based on the approved diagnostic review of the current Code Writer, with one important refinement: the new per-bundle required-artifact mapping must be driven primarily by deterministic orchestration inputs and explicit dependency hints, not by generated-code/stub analysis as the main architectural source.

Context:

- The current Code Writer has already been diagnosed
- The approved diagnosis concluded that the writer still suffers mainly from:
  - artificial bundle dependencies
  - prompt overload
  - mixing weak context with authoritative contract
  - lack of explicit “no generated dependency” signaling
- The approved smallest high-value correction is:
  - introduce precise per-bundle required-artifact mapping
  - replace generic generated dependency lists with the exact required list
  - explicitly say when there are no generated dependencies
- We want Qwen to apply only this narrow correction
- We do NOT want Qwen to redesign the writer, bundling strategy, or pipeline

Important refinement:

- The exact required-artifact mapping must be derived primarily from:
  - deterministic orchestration rules
  - pre-codegen authorized targets
  - package inference
  - explicit dependency hints already available in structured artifacts and/or curated design dependency hints
- It must NOT rely primarily on parsing generated code stubs to invent the dependency graph
- Generated signatures may remain secondary support for downstream prompt context, but not the primary dependency source

Important constraints:

- Do NOT implement code
- Do NOT redesign the writer
- Do NOT redesign the bundle plan
- Do NOT broaden scope into full bundling overhaul
- Generate only a correction prompt for Qwen

1. Required correction target

Generate a Qwen correction prompt that fixes only the highest-value current problem:

- remove artificial generic generated dependency propagation
- introduce an exact per-bundle required generated-artifact list
- reduce writer prompt noise
- add an explicit “no generated dependencies” signal when applicable

2. Required intent of the correction

The correction prompt for Qwen must enforce that:

A. Exact required-artifact mapping

After bundle planning is built, compute a second mapping for each bundle containing only the generated artifacts that are actually required by that bundle.

B. Primary source of truth

This mapping must be driven primarily by:

- deterministic orchestration rules
- structured upstream artifacts
- explicit dependency hints already available
- curated design dependency hints only where needed

C. Secondary-only support

Generated signatures may still be used only as secondary contract propagation support, not as the primary architectural source for deciding dependency edges.

D. Prompt simplification

The writer prompt must stop listing noisy generic generated dependencies and instead list only:

- the exact required generated artifacts
  or
- an explicit “none” statement

E. Explicit no-dependency signal

If a bundle requires no generated artifacts, the prompt must explicitly say:

- "NO GENERATED DEPENDENCIES - DO NOT IMPORT ANY GENERATED TYPES"

3. Required response format

Return exactly this structure:

Qwen Minimal Correction Prompt

<full correction prompt text only>4. Final discipline

- Keep the correction narrow
- Preserve the rest of the current writer direction
- Fix only the highest-value current problem
- Do not redesign the stage
- Do not make generated-code parsing the primary dependency source