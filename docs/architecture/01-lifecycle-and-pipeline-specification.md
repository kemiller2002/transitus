---
id: TRN-ARCH-01
title: Processing Lifecycle and Declarative Pipeline Specification
status: proposed
version: 0.1.0
created: 2026-11-26
updated: 2026-11-26
work_item: WI-0001
schema: schemas/pipeline.schema.json
example: examples/pipelines/irs-eo-bmf-ingest.pipeline.json
decisions: [DF-TRN-2026-0002, DF-TRN-2026-0003, DF-TRN-2026-0005]
---

# Processing lifecycle and declarative pipeline specification

## 1. Design stance

A Transitus pipeline is **data, not a program**. It is a versioned JSON
document (canonical form) whose meaning is defined by an F# discriminated-union
model. The engine interprets it; nothing in it is executed as code.

Three representations, one authority:

| Representation | Role | Authority |
|---|---|---|
| F# DU model (`Transitus.Model`) | The semantic definition. Every case has documented semantics. | Normative |
| Canonical JSON (RFC 8785 JCS) | Storage, diffing, hashing, API, AI generation. Content hash = SHA-256 of JCS bytes. | The stored artifact |
| Visual graph (Forma) | A *projection* of the JSON; edits round-trip to JSON. | None of its own (DF-TRN-2026-0010) |

YAML may be accepted as an authoring convenience but is converted to JSON on
save; YAML is never stored or hashed (avoids YAML 1.1/1.2 ambiguity such as
`NO` → `false`).

## 2. Lifecycle stages

> **Revised after TRN-REV-01.** The declarative pipeline document described here is a **phase-2** deliverable (trigger T2, `docs/roadmap.md`). In phase 1, consumers compose the same stage functions directly in F#; the DU model is the phase-2 serialization target, so phase-1 code migrates without semantic change.

The fourteen lifecycle stages from the charter are **stage kinds**; the schema adds two structural kinds (`route`, `union`), for sixteen in total. A pipeline is a DAG
of stage instances; the engine enforces ordering constraints between kinds.

| # | Stage kind | Input | Output | Execution state persisted | Failure behaviour | Provenance emitted |
|---|---|---|---|---|---|---|
| 1 | `discover` | adapter config | `SourceManifest` (objects/pages/partitions available, cursors) | discovery snapshot | retryable per adapter classification | adapter id/version, endpoint, listing hash |
| 2 | `ingest` | `SourceManifest` entry | byte stream | acquisition attempt, bytes received, checksum | retry transient; permanent → exception | acquisition time, source id, ETag/mtime, size |
| 3 | `preserve` | byte stream | `RawObject` (content-addressed) | raw object row + blob | storage failure = execution failure (never proceed without preserved input) | SHA-256, tenant, retention class |
| 4 | `parse` | `RawObject` | typed record stream + parse exceptions | chunk checkpoints (byte offset / row number) | per-record errors → exception store; structural errors → stop | parser id@version, dialect, row/byte locator |
| 5 | `stage` | record stream | `StagedDataset` (typed, chunked) | chunk ledger | idempotent per chunk | dataset id, schema hash, row count, chunk hashes |
| 6 | `profile` | `StagedDataset` | `Profile` (counts, null %, distincts, min/max, patterns, histograms) | profile document | non-blocking unless gate configured | profile hash |
| 7 | `transform` | one or more staged datasets + reference sets | new `StagedDataset` | chunk ledger | per-record errors → exceptions per error policy | operation ids@versions, reference set versions |
| 8 | `validate` | staged dataset | `ValidationReport` | report | **blocking** gates halt before `authorize` | rule ids@versions, results |
| 9 | `reconcile` | staged dataset(s) + control sources | `ReconciliationReport` | report | **blocking** on unexplained difference | rule ids, control values, differences |
| 10 | `authorize` | reports + plan (`LoadPlan`) | `Authorization` (approved / rejected / auto-approved by policy) | approval events | waits (durable) until decision or expiry | approver identity, policy id, plan hash |
| 11 | `load` | authorized `LoadPlan` | `DestinationReceipt` per record/batch | per-item outbox state | retry by destination classification; idempotency keys | destination id, request hash, response id/status |
| 12 | `verify` | receipts + destination read-back | `VerificationReport` | report | discrepancy → exception + alert, never auto-compensate financial data | read-back hashes |
| 13 | `evidence` | all reports | `EvidencePackage` (manifest + hash chain) | evidence record | evidence failure blocks `complete` status | chain head hash |
| 14 | `retain` | retention policy | purge/retain decisions | purge ledger | retried; failures alert | purge evidence |

Stages 3, 8–10 and 13 are **mandatory** for pipelines whose destination is
classified `system-of-record`; the validator rejects such a pipeline without
them (TRN-REQ-PS-003). Lightweight pipelines (e.g. reference-data refresh
into a staging-only destination) may omit `authorize` by declaring an
`autoApprove` policy whose conditions are evaluated and recorded.

### Stage reuse and composition

- A **stage template** is a named, versioned, parameterized stage (e.g.
  `nacha.parse@1`) inside a mapping package. Pipelines instantiate templates
  with parameters. Templates cannot contain other pipelines (no recursion).
- A **sub-pipeline** (`include`) is deliberately *not* supported in v1:
  reuse happens through templates and packages, which keeps the graph flat
  and fully visible in one document (DF-TRN-2026-0003).

## 3. Control flow without a programming language

Supported constructs, all declarative:

| Construct | Expression | Notes |
|---|---|---|
| Dependency | `dependsOn: [stageId]` | DAG; cycles rejected. |
| Branching | `route` stage: ordered `when` predicates → named outputs, plus mandatory `otherwise` | Every record lands in exactly one branch (partition, not filter) — counts reconcile by construction. |
| Merging | `union` (same schema) or `join@1` | Union requires schema equality or an explicit projection. |
| Conditional stage | `runIf: <predicate over execution facts>` (e.g. `profile.rowCount > 0`, `param.mode = "full"`) | Predicates read only execution facts and parameters, not record data. |
| Exception handling | `onError` per stage: `fail` / `quarantine` / `skipWithCount` (non-financial only) + `maxErrorRate` / `maxErrors` thresholds | Thresholds exceeded ⇒ stage fails. |
| Retry | `retry: { attempts, backoff: exponential(base, cap), jitter, on: [errorClass] }` | Applies to I/O stages only (discover/ingest/load/verify). |
| Wait/approval | `authorize` stage | Durable wait. |

Bounded set operators added after review (TRN-REQ-TX-011): ordered scan (fill-down, running totals with an explicit order key), as-of join against date-effective reference data, fiscal-period derivation, unpivot, bounded explode, duplicate clustering with a maximum cluster size, and linear-time regex capture.

Deliberately **excluded**: general loops, recursion, arbitrary variables, user
functions, dynamic stage generation, string-built SQL, embedded scripts.
Expressiveness analysis and escape hatch: TRN-REV-01 challenge C4.

## 4. Pipeline document structure (abridged)

```jsonc
{
  "$schema": "https://echelon-foundry.dev/transitus/pipeline/1.0.json",
  "kind": "transitus.pipeline",
  "specVersion": "1.0",
  "id": "unbound.irs-eo-bmf.ingest",
  "version": "3.1.0",
  "tenant": "{{tenant}}",                   // bound at instantiation
  "classification": "public",               // highest classification of any field handled
  "packages": [{ "id": "irs.eo-bmf", "version": "^2.0.0", "hash": "sha256:…" }],
  "defaults": { "culture": "invariant", "timeZone": "America/New_York", "unicodeForm": "NFC" },
  "parameters": { "region": { "type": "enum", "values": ["eo1","eo2","eo3","eo4"] } },
  "sources": { "bmf": { "adapter": "https@1", "config": { "url": "...", "egress": ["www.irs.gov:443"] } } },
  "destinations": { "charities": { "adapter": "unbound.domain-api@1", "operation": "charity.upsertRegistry", "classification": "system-of-record" } },
  "schemas": { "bmfRow": { "$ref": "package:irs.eo-bmf/schemas/eo-bmf-row@2" } },
  "stages": [
    { "id": "ingest",   "kind": "ingest",   "source": "bmf" },
    { "id": "raw",      "kind": "preserve", "dependsOn": ["ingest"], "retention": "P7Y" },
    { "id": "parse",    "kind": "parse",    "dependsOn": ["raw"], "template": "irs.eo-bmf/parse@2" },
    { "id": "map",      "kind": "transform","dependsOn": ["parse"], "mapping": "irs.eo-bmf/to-unbound-charity@2" },
    { "id": "check",    "kind": "validate", "dependsOn": ["map"], "profile": "irs.eo-bmf/validation@2", "gate": "blocking" },
    { "id": "recon",    "kind": "reconcile","dependsOn": ["check"], "rules": [ { "rule": "count.withinTolerance@1", "args": { "previousRun": true, "maxDeltaPct": 2 } } ] },
    { "id": "approve",  "kind": "authorize","dependsOn": ["recon"], "policy": { "autoApproveIf": "recon.status = 'balanced'", "else": { "approvers": ["role:charity-data-steward"], "count": 1 } } },
    { "id": "load",     "kind": "load",     "dependsOn": ["approve"], "destination": "charities", "batchSize": 500, "idempotencyKey": ["ein", "business.asOf"] },
    { "id": "verify",   "kind": "verify",   "dependsOn": ["load"], "sample": { "rate": 0.01, "min": 50 } },
    { "id": "evidence", "kind": "evidence", "dependsOn": ["verify"] }
  ],
  "errorPolicy": { "default": "quarantine", "maxErrorRate": 0.001 },
  "resources": { "maxInputBytes": "2GiB", "maxRecordBytes": "64KiB", "memoryBudget": "256MiB", "parallelism": 4 },
  "retention": { "raw": "P7Y", "staging": "P30D", "exceptions": "P2Y", "lineage": "P7Y" },
  "schedule": { "cron": "0 6 * * 2", "timeZone": "America/New_York", "misfire": "runOnce" }
}
```

Full schema: `schemas/pipeline.schema.json`.

## 5. Expression language (TEL — Transitus Expression Language)

A small, typed, total expression language for predicates and computed
fields, represented as a typed expression tree (JSON AST); a textual surface
syntax is parsed into the same tree.

```fsharp
// Illustrative only — not production code.
type Expr =
    | Lit      of Value
    | Field    of FieldPath                  // record field
    | Fact     of FactPath                   // execution facts: profile.rowCount, param.x
    | Ref      of ReferenceSetId * key: Expr // pinned lookup
    | Not      of Expr
    | And      of Expr list
    | Or       of Expr list
    | Compare  of CompareOp * Expr * Expr     // = <> < <= > >=  (type-checked)
    | In       of Expr * Value list
    | IsMissing of Expr
    | IsNull   of Expr
    | Arith    of ArithOp * Expr * Expr * DecimalContext  // scale + rounding explicit for ÷
    | Call     of OperationId * Expr list * Parameters    // only catalogued pure operations
    | Case     of (Expr * Expr) list * otherwise: Expr
```

Properties: statically typed; no recursion or iteration, so evaluation
terminates in O(size of tree) per record; three-valued logic for
`Missing`/`Null` is explicit (`Compare` with a missing operand yields
`Error MISSING_OPERAND` unless guarded by `IsMissing`).

## 6. Validation of a pipeline definition (deterministic gates)

Before a definition can be published:

1. JSON Schema validation (`schemas/pipeline.schema.json`).
2. Reference resolution: packages, templates, schemas, reference sets,
   adapters, destinations exist and hashes match.
3. Type checking of every mapping and expression.
4. DAG checks: acyclic, every stage reachable, route branches total.
5. Policy checks: mandatory stages for system-of-record destinations;
   loss acknowledgements present; classification ≤ destination clearance;
   egress allow-lists ⊆ tenant policy; no destination not granted to tenant.
6. Authority-envelope diff against the previous published version
   (new sources, destinations, egress hosts, classification increases,
   relaxed gates) — any widening requires the elevated approval path —
   plus highlighted review of semantic-critical changes (idempotency-key
   fields, auto-approve conditions, financial code mappings, money/date
   field re-mapping, reference-data versions) (TRN-REQ-PS-008, revised).
7. Dry-run against fixtures in the package (if present) must pass.

Identical inputs to this validator produce identical results; the
validator itself is versioned and its version is recorded on publish.

## 7. Versioning

- `specVersion` — the pipeline language; semver; engine supports N and N-1.
- `version` — the pipeline's own semver; published versions are immutable.
- An execution binds: pipeline hash, package hashes, reference-set versions,
  engine version, parameters. That tuple is the **execution manifest**, and
  is the determinism contract (TRN-REQ-AI-005).
