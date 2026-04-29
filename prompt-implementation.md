Goal:
Fix the pre-codegen artifact classification so JPA repositories and repository services are separated deterministically before codegen.

Context:

- The current codegen bundles artifacts by artifactCategory
- RepositoryService artifacts and JpaRepository artifacts are currently being mixed or misclassified
- As a result, the LLM generates repository service classes but does not generate the corresponding Spring Data JPA repository interfaces
- This is not primarily a codegen prompt problem
- This is a pre-codegen classification and query-mapping problem

Problem:
Repository-layer artifacts from design.md may include both:

1. JPA Repository interfaces:
   
   - Spring Data interfaces
   - extend JpaRepository or CrudRepository
   - contain query methods such as @Query or derived finder methods

2. Repository Service classes:
   
   - @Service classes
   - inject the corresponding JPA repository
   - map persistence/query results to domain/model classes

These two artifact types must not be bundled together under the same artifactCategory.

Scope

Implement only the deterministic pre-codegen classification fix.

Do NOT:

- redesign the whole pipeline
- modify diagnosis
- modify traceability
- modify design generation
- implement broad codegen redesign
- introduce semantic retrieval
- rely on LLM inference for this classification

Required behavior

Before codegen bundles are created, every repository-layer artifact must be classified as one of:

- jpa-repository
- repository-service

Classification rules

jpa-repository

Classify as "jpa-repository" when the artifact represents a Spring Data repository interface.

Signals:

- name ends with "Repository" but not "RepositoryService"
- artifact is described as interface
- design or package inference indicates Spring Data / JPA repository
- target package matches infrastructure db jpa repositories
- should extend JpaRepository or CrudRepository

repository-service

Classify as "repository-service" when the artifact represents a service wrapper around persistence access.

Signals:

- name ends with "RepositoryService"
- artifact is described as service or implementation
- target package matches bounded-context repository/service package
- should inject a corresponding JPA repository
- should map query results to domain/model classes

Pairing rule

For every "repository-service", infer or attach the corresponding "jpa-repository".

Example:

- BranchRepositoryService -> BranchRepository
- IEventRepositoryService -> IEventRepository
- InstructionRepositoryService -> InstructionRepository

If the corresponding JPA repository is missing from the pre-codegen decision table, create a derived "jpa-repository" artifact entry unless a conflicting artifact already exists.

The derived entry must include:

- artifactCategory: "jpa-repository"
- designArtifactName
- derivedPackage
- targetPath
- queryMethods if available
- relation to the repository-service

Query method propagation

If query methods are known from:

- codebase-verification-report.json
- design.md Required New Artifacts
- pre-codegen-decision-table.json
- query-inventory.json

then attach them to the "jpa-repository" artifact.

The "repository-service" must reference the same query methods as delegated methods, but the actual query definition belongs to the "jpa-repository".

Codegen bundle rules

The codegen bundle must separate:

Bundle: jpa-repository

Must include only artifacts classified as "jpa-repository".

Instruction for LLM:

- generate interface
- annotate with @Repository if project convention requires it
- extend JpaRepository or CrudRepository
- declare query methods
- include @Query only when query text is available and reliable
- otherwise generate derived method signatures or TODO comments with traceability

Bundle: repository-service

Must include only artifacts classified as "repository-service".

Instruction for LLM:

- generate @Service class
- inject corresponding JPA repository
- expose domain-facing methods
- delegate persistence calls to JPA repository
- map persistence results to domain/model/projection objects

Required output updates

Update the relevant artifact decision structures so they explicitly contain:

- artifactCategory
- relatedJpaRepositoryName, when artifactCategory is repository-service
- relatedRepositoryServiceName, when artifactCategory is jpa-repository
- queryMethods, when known
- sourceRule explaining whether classification came from suffix, package, design, or derived pairing

Validation

Add or update validation so that:

- no "repository-service" artifact is sent in the "jpa-repository" bundle
- no "jpa-repository" artifact is sent in the "repository-service" bundle
- every "repository-service" has a corresponding "jpa-repository", unless explicitly marked as unresolved
- if unresolved, emit a warning before codegen

Acceptance criteria

This fix is complete only if:

- JPA repositories and repository services are separated before codegen
- repository-service artifacts no longer suppress generation of JPA repository interfaces
- generated codegen bundles contain the correct artifact categories
- repository services receive the name of the JPA repository they must inject
- JPA repositories receive the query methods they must declare when available
- no broad unrelated refactor is introduced

Final instruction:
This is a deterministic pre-codegen classification fix.
Do not rely on the LLM to guess artifact category.
The LLM must receive already-separated bundles with explicit instructions.