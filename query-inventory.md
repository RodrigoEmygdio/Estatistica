Apply a minimal hardening pass to the existing query-inventory extraction so it becomes materially more useful for the golden-path demo, without redesigning the inventory system.

Context:

- Step 1A already exists
- The current weakest area is "query-inventory.json"
- Current observed issues:
  - method extraction is weak
  - HQL/JPQL-bearing artifacts are being missed
  - downstream data-access reuse decisions are underpowered because query evidence is too thin
- We do NOT want a full query-analysis engine
- We want the smallest correct improvement for the demo path

Goal:
Improve the existing query-inventory extraction so it captures enough method/query evidence to support conservative downstream reuse verification for the demo golden path.

1. Scope of this correction

Implement only:

- stronger method extraction for query-bearing artifacts
- stronger detection of query-bearing sources
- minimum useful enrichment of "query-inventory.json"

Do NOT implement:

- full JPQL/HQL parser
- semantic search
- complex query normalization
- full call graph
- runtime reflection
- broad redesign of all inventory artifacts

2. Required query sources to detect

For the MVP, improve detection of these sources when statically obvious:

- "@Query"
- "EntityManager"
- "JdbcTemplate"
- "NamedParameterJdbcTemplate"
- inline HQL/JPQL string usage in repositories/services/adapters when clearly present

This is a detection improvement, not a full parser.

3. Method extraction improvement

The query inventory must capture real method-level evidence more reliably.

At minimum, for each query entry, try to expose:

- "ownerArtifactName"
- "ownerArtifactType"
- "ownerFullyQualifiedName"
- "methodName"
- "filePath"
- "queryKind"
- "sourceKind"

If safely available, also include:

- "hasQueryAnnotation"
- "usesEntityManager"
- "usesJdbcTemplate"
- "usesNamedParameterJdbcTemplate"
- "querySnippet" or "queryPreview" (short, bounded, optional)
- "parameterTypes" (optional, only if easily extractable)
- "returnType" (optional, only if easily extractable)

Do not overengineer optional fields.

4. HQL/JPQL detection rule

Add lightweight static detection for HQL/JPQL-like strings when they are clearly present in:

- repository classes
- service classes
- adapter classes involved in DB access

Conservative rule:

- only capture when there is an obvious query-bearing string near a recognized data-access mechanism
- do not guess from arbitrary strings

5. Noise control

Avoid polluting "query-inventory.json" with generic infrastructure noise.

Do NOT emit query entries for:

- unrelated helper methods
- plain constructors
- non-query utility methods
- framework boilerplate without clear query behavior

Prefer fewer useful entries over many weak entries.

6. Preservation rules

Do NOT break:

- deterministic ordering
- metadata wrapper shape ("generatedAt", "gitCommitSha", "items")
- current inventory generation for repositories/services/entities/adapters
- fallback behavior already implemented

Only strengthen query extraction.

7. Determinism requirements

Keep extraction deterministic:

- stable file traversal
- stable per-item ordering
- stable JSON ordering
- stable field naming

8. Acceptance criteria

This hardening pass is complete only if:

- "query-inventory.json" captures method-level entries more reliably
- "@Query", "EntityManager", "JdbcTemplate", and "NamedParameterJdbcTemplate" are handled more robustly
- obvious HQL/JPQL-bearing cases are no longer silently missed
- noise remains bounded
- no unrelated inventory modules are broadly redesigned

9. Required output after changes

After applying the hardening, return a concise summary with exactly these sections:

Query Inventory Hardening Applied

Files updated

Improvements applied

What was intentionally left unchanged

Safe next step

10. Final instruction

Make the smallest correct improvements that materially strengthen "query-inventory.json" for the demo golden path.

Do not redesign the inventory stage.
Do not broaden scope.
Prefer conservative useful extraction over ambitious incomplete parsing.