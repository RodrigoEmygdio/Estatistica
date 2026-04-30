Goal:
Fix the pre-codegen repository materialization logic so logical repository/data-access targets are expanded into the concrete architecture required by the target codebase.

Context:

- The architecture requires two concrete artifact types for repository access:
  1. JpaRepository interface
  2. RepositoryService class
- However, design.md should not be required to list both concrete artifacts
- The design stage should identify logical repository/data-access needs and query responsibilities
- The pre-codegen stage must materialize the concrete architecture deterministically
- The codegen stage must receive separated bundles with explicit artifact categories

Problem:
Currently, repository-related artifacts may be classified or bundled incorrectly.
Sometimes repository-service and jpa-repository responsibilities are mixed.
Sometimes the LLM receives only repository-service artifacts and therefore does not generate the corresponding JpaRepository interfaces.

This should not be solved by forcing design.md to list both artifacts.
It must be solved in pre-codegen orchestration.

1. Scope

Implement only the pre-codegen repository materialization fix.

Do NOT:

- force design.md to explicitly list both RepositoryService and JpaRepository artifacts
- redesign the design stage
- redesign diagnosis or traceability
- introduce semantic retrieval
- rely on LLM inference for artifact category decisions
- broaden into unrelated codegen changes

2. Architectural rule

For every logical repository/data-access target, pre-codegen must materialize:

1. a "jpa-repository" artifact
2. a "repository-service" artifact

The "repository-service" must depend on the corresponding "jpa-repository".

The "jpa-repository" owns query method declarations.

The "repository-service" delegates to the "jpa-repository" and maps persistence results into domain/model/projection objects.

3. Source of logical repository targets

Logical repository/data-access targets may be derived from:

- design.md repository/data-access sections
- Required New Artifacts if present
- traceability blocks with "data_access"
- codebase-verification-report.json targets
- query-inventory/queryMethods when available
- pre-codegen-decision-table existing entries

Do not require design.md to explicitly include both concrete artifacts.

4. Materialization rule

For each logical repository target:

Create or confirm a JpaRepository artifact:

- artifactCategory: "jpa-repository"
- artifact role: Spring Data repository interface
- expected shape: interface extending JpaRepository or CrudRepository
- owns queryMethods

Create or confirm a RepositoryService artifact:

- artifactCategory: "repository-service"
- artifact role: service wrapper around repository access
- expected shape: class annotated with @Service
- injects the corresponding JpaRepository
- delegates query calls
- maps results to domain/model/projection

5. Naming rules

Use existing project naming conventions.

Examples:

- logical EventRepository -> IEventRepository + EventRepositoryService
- logical BranchRepository -> IBranchRepository + BranchRepositoryService
- logical InstructionRepository -> IInstructionRepository + InstructionRepositoryService

If the current project convention uses different prefixes or suffixes, preserve the existing convention already used by package inference.

6. Package inference rules

Use package inference to assign concrete locations:

jpa-repository

Should go to the infrastructure JPA repository package, for example:

- infrastructure/db/jpa/repositories/<bounded-context>

repository-service

Should go to the bounded-context repository service package, for example:

- isi_services/<bounded-context>/repository

Do not send both categories to the same package unless the existing project convention explicitly requires it.

7. Query method propagation

For each logical repository target:

- attach queryMethods to the "jpa-repository"
- attach delegatedQueryMethods to the "repository-service"
- the query definition belongs to "jpa-repository"
- the service method delegates to the repository method

If query methods are not known:

- still materialize the pair
- emit a warning that queryMethods are missing or unresolved
- do not silently omit the JpaRepository

8. Output artifact updates

Update "package-inference.json" and/or "pre-codegen-decision-table.json" so that each materialized artifact includes:

- artifactCategory
- designArtifactName
- derivedPackage
- derivedFqn
- targetPath
- sourceRule
- boundedContext
- relatedJpaRepositoryName for repository-service artifacts
- relatedRepositoryServiceName for jpa-repository artifacts
- queryMethods or delegatedQueryMethods when available
- warnings when query methods cannot be resolved

9. Codegen bundle rules

The codegen input must be separated by artifactCategory.

jpa-repository bundle

Contains only "jpa-repository" artifacts.

LLM instruction:

- generate interface
- extend JpaRepository or CrudRepository
- declare query methods
- use @Query only if query text is available and reliable
- otherwise generate derived method signatures or TODO comments with traceability

repository-service bundle

Contains only "repository-service" artifacts.

LLM instruction:

- generate @Service class
- inject corresponding JpaRepository
- expose domain-facing methods
- delegate to JpaRepository
- map persistence results to domain/model/projection objects

10. Validation rules

Before invoking codegen, validate:

- every logical repository/data-access target produced both concrete artifacts
- every repository-service has relatedJpaRepositoryName
- every jpa-repository has relatedRepositoryServiceName
- no repository-service is sent in the jpa-repository bundle
- no jpa-repository is sent in the repository-service bundle
- missing queryMethods produce warnings, not silent omission

11. Acceptance criteria

This fix is complete only if:

- design.md is not required to list both RepositoryService and JpaRepository
- pre-codegen materializes both artifacts from logical repository/data-access targets
- JpaRepository and RepositoryService are separated before codegen
- RepositoryService artifacts reference the JpaRepository they depend on
- JpaRepository artifacts own query methods when available
- package-inference and/or pre-codegen-decision-table expose the relationship explicitly
- codegen bundles are category-separated
- no broad unrelated refactor is introduced

12. Final instruction

This is a deterministic pre-codegen orchestration fix.

Do not push architectural materialization responsibility into design.md.
Do not ask the LLM to infer repository architecture.
The orchestrator must materialize the concrete repository architecture before codegen.