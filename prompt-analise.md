Goal:
Perform a strict diagnostic review of the current Code Writer implementation and its generated writer prompt composition, and determine why the latest implementation is still not producing a good demo-safe writer model.

Context:

- The Code Writer has already gone through multiple iterations
- Qwen has implemented changes, but the result is still not satisfactory
- Current symptoms include:
  - weak or artificial bundle dependencies
  - prompt composition that is still too noisy or not semantically well-structured
  - the writer still not behaving like a clean controlled code-generation stage
- We do NOT want a redesign of the entire pipeline
- We want a precise diagnosis of what is still wrong now

Important constraints:

- Do NOT implement code
- Do NOT modify files
- Do NOT redesign the whole architecture
- Focus only on diagnosing the current Code Writer implementation and prompt-builder direction

1. Review targets

Review internally:

- current codegen/code writer implementation
- current bundle planning logic
- current prompt builder logic
- current writer output contract
- current use of:
  - pre-codegen-decision-table.json
  - package-inference.json
  - codegen-bundle-plan.json
  - design.md
  - sp-numbered.sql
- any generated prompt sample / debug prompt output available

2. Core question

Why is the current Code Writer direction still not good enough, even after the recent refactors?

3. Review criteria

Evaluate specifically:

A. Bundle planning quality

- Are bundle dependencies still artificial, inflated, or semantically invalid?
- Are bundles themselves too small, too large, or poorly grouped?

B. Prompt constitution quality

- Is the prompt still overloaded?
- Are authoritative decisions mixed with too much weak context?
- Is the prompt structure helping the model, or overburdening it?

C. Responsibility separation

- Is the writer still being asked to solve decisions that should already be settled before prompt construction?
- Is the orchestrator doing enough work, or is too much still delegated to the LLM?

D. Output contract realism

- Is the output contract appropriate for the current prompt?
- Is the stage asking for too much structure and too much implementation at once?

E. Smallest next correction

- What is the smallest correction that would most improve the current writer stage?

4. Required response format

Return exactly this structure:

Current Code Writer Diagnostic Review

1. Overall conclusion

State one of:

- CURRENT WRITER IS CLOSE AND NEEDS SMALL FIXES
- CURRENT WRITER HAS A STRUCTURAL PROBLEM AND NEEDS A TARGETED REWORK

2. What is already correct

3. What is still wrong

4. What is causing the writer to remain weak

5. What must stop being delegated to Qwen/LLM

6. Smallest high-value correction now

7. What can wait until after the demo

8. Final recommendation

5. Final discipline

- Be precise
- Be conservative
- Prefer diagnosis over redesign
- Focus on actionable architectural correction