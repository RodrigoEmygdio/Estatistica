Goal:
Review the current "docs/architecture/code-gen/minimal-codegen-contract.md" against a proposed refinement and determine whether the document is now missing or underspecifying the rules required for a demo-safe Codegen MVP.

Context:

- The current codegen implementation has exposed architectural ambiguity around:
  - execution unit vs scheduling unit
  - phase-based generation
  - bundle planning rules
  - inter-bundle dependency rules
  - writer authority boundary
  - prompt constitution rules
- A proposed refinement has been prepared to make the contract more normative for the demo MVP
- We do NOT want to redesign the whole system
- We want to validate whether the current documentation is incomplete or underspecified relative to the actual needs of the Codegen MVP

Important constraints:

- Do NOT implement code
- Do NOT modify files
- Do NOT rewrite the whole document from scratch
- Focus only on whether the current contract is sufficiently normative and what sections/rules must be added or sharpened

1. Review target

Review:

- "docs/architecture/code-gen/minimal-codegen-contract.md"

Evaluate it against the following proposed refinements:

Proposed additions / sharpened rules

1. Explicit distinction between:
   
   - decision unit
   - execution unit
   - scheduling unit

2. Normative generation phases:
   
   - model-dto-phase
   - repository-phase
   - domain-service-phase
   - application-service-phase

3. Bundle planning rules:
   
   - bundle contains only "generate_new"
   - bundle not formed from bounded context alone
   - bundle not formed from naming similarity alone
   - bundle must remain small and functionally coherent

4. Inter-bundle dependency rules:
   
   - no dependency edge from bundle order / block order / same bounded context / broad phase expansion
   - exact required generated-artifact mapping
   - explicit no-dependency signal:
     "NO GENERATED DEPENDENCIES - DO NOT IMPORT ANY GENERATED TYPES"

5. Writer authority boundary:
   
   - writer materializes only already-approved targets
   - writer must not invent dependencies, packages, actions, or extra files

6. Writer prompt rules:
   
   - concise authoritative contract only
   - exact dependency context only
   - no full raw design/SP text as primary prompt body

7. Demo MVP simplifications and forbidden noisy heuristics

8. Execution sequence updated to reflect:
   
   - pre-codegen
   - phase plan
   - bundle plan
   - exact dependency propagation
   - generated signatures as downstream contract propagation only

2. Core question

Is the current "minimal-codegen-contract.md" sufficiently normative for the current demo MVP, or does it need targeted documentation refinement in the areas listed above?

3. Required response format

Return exactly this structure:

Minimal Codegen Contract Review

1. Overall conclusion

State one of:

- CURRENT DOCUMENT IS SUFFICIENT
- CURRENT DOCUMENT NEEDS TARGETED REFINEMENT

2. What is already well specified

3. What is underspecified or missing

4. Which proposed refinements are truly necessary now

5. Which proposed refinements can wait until after the demo

6. Smallest documentation update that would materially improve implementation discipline

7. Final recommendation

4. Final discipline

- Be pragmatic
- Be conservative
- Do not redesign the whole document
- Focus on the smallest documentation changes that reduce implementation drift this week