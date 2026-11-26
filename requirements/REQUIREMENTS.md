---
id: TRN-REQ-REGISTER
title: Transitus Requirements Register
status: proposed
version: 0.1.0
created: 2026-11-26
updated: 2026-11-26
generated_by: tools/render_requirements.py (do not hand-edit)
---

# Requirements register

115 proposed requirements. Priority: P0 = required for first production use, P1 = required for the phase, P2 = conditional/deferred. Machine-readable: `requirements/requirements.json`.


## pipeline-spec

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-PS-001 | P0 | 1 | Pipelines MUST be versioned, declarative JSON documents conforming to a published JSON Schema and an F# discriminated-union model; the content hash (SHA-256 of RFC 8785 canonical JSON, excluding annotations) identifies a pipeline version. | Two semantically identical pipelines with different key order or layout annotations produce the same hash; schema-invalid documents are rejected with a located error. | test |
| TRN-REQ-PS-002 | P0 | 1 | Every stage MUST declare its kind, inputs (dependsOn), outputs, failure behaviour and the provenance it emits, per the lifecycle table. | Publish-time validator rejects a stage lacking required fields; documentation lists inputs/outputs/state/failure/provenance for all 14 stage kinds. | test |
| TRN-REQ-PS-003 | P0 | 1 | Pipelines whose destination is classified system-of-record MUST include preserve, blocking validate, blocking reconcile, authorize and evidence stages. | Validator rule PV-12 rejects a system-of-record pipeline missing any of these stages. | test |
| TRN-REQ-PS-004 | P0 | 1 | Published pipeline versions MUST be immutable; publishing MUST require an authorized role, and pipelines handling restricted-financial or phi classifications MUST require a second approver. | Attempting to modify a published version fails; single-approver publish of a financial pipeline is refused. | test |
| TRN-REQ-PS-005 | P0 | 1 | Control flow MUST be limited to DAG dependencies, total partitioning routes with a mandatory otherwise branch, union/join merges, runIf predicates over execution facts, per-stage error policies and retries; loops, recursion, user functions and dynamic stage generation MUST NOT be expressible. | JSON Schema and validator reject cycles, missing otherwise branches and any construct outside the list. | test |
| TRN-REQ-PS-006 | P0 | 1 | User-configured pipelines MUST NOT contain or evaluate arbitrary executable code, dynamic SQL, JavaScript or unrestricted scripting; extension MUST occur only via reviewed, compiled F# operation packages on a host allow-list. | No schema field accepts code; fuzzed pipeline documents never cause code loading; an unlisted package reference fails validation. | test |
| TRN-REQ-PS-007 | P0 | 1 | Predicates and computed fields MUST use the typed, total Transitus Expression Language whose evaluation terminates in time linear in expression size. | Type errors are reported at publish; property tests show termination and no exceptions for generated expressions. | test |
| TRN-REQ-PS-008 | P0 | 1 | Publish-time validation MUST compute an authority-envelope diff against the prior version and require elevated approval for any widening (new source, destination, egress host, secret slot, classification increase, relaxed gate or tolerance, new loss acknowledgement). | A diff adding an egress host is flagged and cannot publish with standard approval. | test |
| TRN-REQ-PS-009 | P1 | 1 | Every operation, configuration field, stage kind and error code MUST have AI-readable semantics documentation, generated from or checked against the model. | Documentation-completeness test fails when a DU case lacks semantics text. | test |
| TRN-REQ-PS-010 | P1 | 1 | The pipeline specification MUST support source, destination and schema definitions, field mappings, type conversion, validation, conditional transformation, lookups, joins, aggregation, filtering, deduplication, normalization, relationship resolution, reference data, reconciliation, error, retry and approval policies, scheduling, resource limits, retention and security classification. | Each listed construct has a schema element and at least one example fixture. | test |

## storage

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-ST-001 | P0 | 2 | Raw inputs MUST be preserved immutably and content-addressed by SHA-256 with tenant, source identifier, source locator, acquisition timestamp, source metadata, adapter version, classification and retention class before any parsing. | Parse stage cannot start without a committed raw object; metadata row contains all listed fields. | test |
| TRN-REQ-ST-002 | P0 | 2 | Source-supplied file names, paths and keys MUST be stored only as metadata and never used to derive storage paths. | Zip-slip and path traversal fixtures produce no file outside the blob store namespace. | test |
| TRN-REQ-ST-003 | P0 | 2 | Staging MUST be typed, tenant-partitioned, chunked and isolated, with DDL produced at publish time through the host's Strata-governed migration path and no runtime ad hoc DDL. | Execution role lacks DDL privilege; staging tables exist only after a governed migration. | test |
| TRN-REQ-ST-004 | P0 | 2 | Processing MUST NOT require the full dataset to fit in memory; memory use MUST be bounded by the pipeline memory budget independent of record count. | A 10x larger input does not increase peak working set beyond the configured budget (measured). | test |
| TRN-REQ-ST-005 | P1 | 2 | Transformed datasets MUST be sealed by a Merkle root over chunk hashes, and approval and load MUST bind to that root. | Mutating a staged row after approval causes load to refuse with HASH_MISMATCH. | test |
| TRN-REQ-ST-006 | P0 | 2 | Staging MUST have an enforced TTL, MUST NOT be exposed through general query APIs, and MUST NOT be used as a source by any other tenant or application. | Sweeper purges expired partitions and records purge evidence; no API returns staged rows except bounded, classification-masked previews. | test |
| TRN-REQ-ST-007 | P1 | 2 | The blob store MUST be a port with a PostgreSQL-backed default and an optional S3-compatible implementation. | Conformance tests pass for both implementations. | test |
| TRN-REQ-ST-008 | P2 | 4 | File-backed columnar staging MAY be introduced for executions above ~10^7 records only after measured evidence shows database staging is inadequate, without adding a deployment component. | Decision record cites measurements. | review |

## transformation

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-TX-001 | P0 | 1 | Every transformation operation MUST be versioned (name@major) and pinned by pipelines; behavioural change requires a new major version. | Changing golden output of an operation without a major bump fails CI. | test |
| TRN-REQ-TX-002 | P0 | 1 | Transformations MUST be pure and total: they return Ok or a typed error, never throw for data-dependent reasons and never perform I/O. | Property tests with arbitrary inputs observe no exceptions; operations have no I/O dependencies. | test |
| TRN-REQ-TX-003 | P0 | 1 | Culture, locale, time zone (with pinned tzdb version), Unicode normalization form and rounding mode MUST be explicit parameters; host ambient settings MUST NOT influence results. | Tests run under different host cultures and TZ produce identical outputs. | test |
| TRN-REQ-TX-004 | P0 | 1 | Operations that may lose information MUST be rejected unless the stage carries an acknowledgeLoss with reason; reversible, reversible-with-key and irreversible operations MUST be classified. | Validator rejects truncate/round/mask without acknowledgement; descriptor lists reversibility for every operation. | test |
| TRN-REQ-TX-005 | P0 | 1 | Financial values MUST use decimal types only and MUST NEVER be silently truncated, rounded, discarded or reinterpreted; scale reduction requires an explicit rounding operation with declared mode and approval reference. | Parsing 1.005 into a 2-scale money field returns PRECISION_LOSS; floats are rejected for Money fields. | test |
| TRN-REQ-TX-006 | P0 | 1 | Missing, explicit-null and present values MUST be distinguished, and every operation MUST declare its behaviour for each. | Coalescing occurs only via explicit operations; tests cover all three cases per operation. | test |
| TRN-REQ-TX-007 | P0 | 1 | Lookups MUST reference versioned reference sets whose versions are recorded in the execution manifest. | Replaying with the same manifest yields identical lookup results after reference data has changed. | test |
| TRN-REQ-TX-008 | P0 | 2 | Record matching MUST produce scored candidates; financial entities MUST NOT be auto-merged, and candidates between configured thresholds MUST go to review. | Matching fixtures show no automatic merges for financial entity types. | test |
| TRN-REQ-TX-009 | P1 | 1 | The standard library MUST provide the operation catalogue in TRN-ARCH-04 §3 (string, Unicode, whitespace, date/time/zone, decimal, currency, enum, identifier, address, null, default, split, concat, conditional, math, lookup, matching, duplicate detection, relationship resolution, aggregation, masking, redaction, hashing, tokenization). | Catalogue coverage test enumerates all listed operations. | test |
| TRN-REQ-TX-010 | P0 | 1 | Hashing of low-entropy identifiers MUST use keyed HMAC with a tenant-scoped key; unkeyed hashing of such identifiers MUST be rejected. | Validator rejects privacy.hash with sha256 on fields typed ssn/ein/phone. | test |

## adapters

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-AD-001 | P0 | 1 | Adapters MUST be separated into transport, format and destination roles behind published F# contracts, independently packaged, with the core depending only on the abstractions. | A new format adapter is added and passes conformance without changes to Transitus.Engine. | test |
| TRN-REQ-AD-002 | P0 | 1 | Every adapter MUST declare capabilities, configuration schema, secret slots, egress derivation and an error taxonomy mapped to Transient, RateLimited, AuthFailure, PermanentInput, PermanentConfig or Ambiguous. | Descriptor validates against schemas/adapter-descriptor.schema.json; unknown write errors classify as Ambiguous. | test |
| TRN-REQ-AD-003 | P0 | 1 | Adapters MUST support connection testing without mutation and MUST ship synthetic fixtures for conformance testing. | Conformance suite runs every adapter's Test and fixtures offline. | test |
| TRN-REQ-AD-004 | P0 | 2 | Incremental transports MUST persist opaque, versioned checkpoints that advance only after downstream stage commit. | Crash after acquisition but before stage commit re-acquires the same items. | test |
| TRN-REQ-AD-005 | P0 | 1 | Phase-1 adapters MUST cover upload, HTTPS, CSV/TSV, fixed-width, XLSX, JSON/NDJSON, staging-only sink and the Unbound domain API destination; further adapters MUST be justified by a consumer scenario. | Adapter catalogue lists the driving scenario for each adapter. | review |
| TRN-REQ-AD-006 | P0 | 1 | Adapters MUST honour rate limits and Retry-After, and MUST NOT implement internal retry loops; retries are engine-owned. | Adapter conformance asserts single attempt per call. | test |
| TRN-REQ-AD-007 | P0 | 2 | Destination adapters MUST declare a delivery guarantee (idempotent-key, natural-upsert, query-before-write, none) and support read-back where the destination allows. | Engine selects retry/verification policy from the declared guarantee. | test |
| TRN-REQ-AD-008 | P0 | 1 | Loads into regulated Unbound workflows MUST occur through Unbound domain APIs or approved domain interfaces; Transitus MUST NOT hold credentials to write business tables directly. | Unbound destination adapter uses only published domain operations; no database credentials for Unbound business schemas exist in Transitus configuration. | test |
| TRN-REQ-AD-009 | P1 | 2 | Snapshot-diff by natural key MUST be supported for full-file feeds. | BMF fixture yields correct adds, changes and removals versus the prior snapshot. | test |
| TRN-REQ-AD-010 | P2 | 2 | Bidirectional synchronization and conflict resolution MUST NOT be built; outbound flows are separate one-directional pipelines. | Scope review. | review |

## execution

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-EX-001 | P0 | 2 | Durable execution (queueing, leases, retries, idempotent intake, ordering, approval waits, quarantine, OutcomeUnknown, per-tenant fairness, pause) MUST be provided by Echelon.Execution; Transitus MUST NOT implement a separate queue. | Transitus.Engine has no queue tables; stage commands appear in Echelon.Execution history. | review |
| TRN-REQ-EX-002 | P0 | 2 | The engine MUST implement an explicit pipeline execution state machine including Blocked, PartiallyLoaded and OutcomeUnknown states whose legal transitions are defined by a total pure function. | Exhaustive transition tests; illegal transitions return errors. | test |
| TRN-REQ-EX-003 | P0 | 2 | Batch, incremental, scheduled, manual, event-triggered, dry-run and replay modes MUST be supported. | Each mode has an acceptance test. | test |
| TRN-REQ-EX-004 | P0 | 2 | Dry runs MUST execute stages 1-9 and produce a load plan without writing to any system of record. | Dry run against the Unbound adapter performs zero domain commands. | test |
| TRN-REQ-EX-005 | P0 | 2 | Processing MUST be chunked with per-chunk checkpoints enabling resumption, cancellation and parallelism where declared. | Kill a worker mid-run; resumed run produces identical outputs with no duplicate chunks. | test |
| TRN-REQ-EX-006 | P0 | 2 | Each destination record MUST carry a deterministic idempotency key derived from tenant, pipeline, destination, declared natural key and business date. | Replay produces identical keys; destination dedupes. | test |
| TRN-REQ-EX-007 | P0 | 2 | Transitus MUST NOT claim exactly-once delivery; ambiguous external effects MUST enter OutcomeUnknown and be resolved by verification or reconciliation, never by blind retry. | Simulated timeout after send yields OutcomeUnknown and no retry. | test |
| TRN-REQ-EX-008 | P0 | 2 | Load intent MUST be committed before the external call and the receipt after it; no transaction spans the network. | Crash-injection test at each point leaves a resolvable state. | test |
| TRN-REQ-EX-009 | P0 | 2 | Compensation of loaded financial records MUST NOT be automatic. | No code path issues reversal commands. | review |
| TRN-REQ-EX-010 | P0 | 2 | Resource limits (input bytes, record bytes, records, nesting depth, archive entries and ratio, memory budget, parallelism, CPU time) and backpressure MUST be enforced. | Limit fixtures fail fast with typed errors; queue depth stays bounded under slow destinations. | test |
| TRN-REQ-EX-011 | P1 | 2 | Cancellation MUST be cooperative and MUST NOT leave unrecorded external effects. | Cancel during load; all in-flight receipts recorded. | test |
| TRN-REQ-EX-012 | P1 | 2 | Schedules MUST declare an IANA time zone and misfire policy and be materialized as ScheduledCommands, without a separate scheduler service. | DST transition fixtures schedule correctly. | test |

## validation-reconciliation

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-VR-001 | P0 | 2 | Transitus MUST provide generic validation primitives for required, type, range, pattern, code set, check digit, cross-field, uniqueness, referential integrity, completeness, sequence, freshness and distribution. | Primitive catalogue tests. | test |
| TRN-REQ-VR-002 | P0 | 2 | Transitus MUST provide reconciliation primitives for counts, control totals, hash totals, balance (opening + movements = closing), keyed set matching, cross-file, cross-system and timing differences. | Primitive catalogue tests including NACHA control and hash totals. | test |
| TRN-REQ-VR-003 | P0 | 2 | Monetary reconciliation tolerance MUST default to zero; non-zero tolerances MUST be declared with justification and appear in evidence. | Profile without tolerance treats a one-cent difference as Unbalanced. | test |
| TRN-REQ-VR-004 | P0 | 2 | Blocking validation and reconciliation gates MUST prevent all downstream stages, including load, when they fail. | Failing gate leaves execution Blocked with zero destination effects. | test |
| TRN-REQ-VR-005 | P0 | 2 | Gate overrides MUST be elevated authorizations with justification, recorded in evidence, and MUST NOT modify data. | Override evidence present; staged data hash unchanged. | test |
| TRN-REQ-VR-006 | P0 | 2 | Unbound-specific accounting rules MUST live in Unbound-owned profiles, not in Transitus core. | No Unbound domain terms in Transitus core packages (dependency/term scan). | review |
| TRN-REQ-VR-007 | P0 | 2 | Every stage MUST satisfy the conservation law in = out + rejected + quarantined + deduplicated + filteredWithCount; discards without counts MUST be impossible. | Engine assertion; mutation test that drops a record fails the execution. | test |
| TRN-REQ-VR-008 | P0 | 2 | Record-level exceptions MUST be typed, grouped by code and resolvable only by mapping change, reference data, corrected source or approved exclusion; staged values MUST NOT be hand-edited. | No API mutates staged values. | test |
| TRN-REQ-VR-009 | P0 | 2 | Transitus MUST NOT introduce balancing entries, write-offs, suspense entries or silently discarded records. | Review and tests: no operation emits synthetic financial records. | review |
| TRN-REQ-VR-010 | P0 | 2 | Post-load verification MUST reconcile planned, loaded and read-back counts and totals. | Verify stage report present in evidence for every system-of-record load. | test |
| TRN-REQ-VR-011 | P1 | 2 | Duplicate detection MUST operate within file, execution and destination (via read-back) scopes. | Fixtures for each scope. | test |
| TRN-REQ-VR-012 | P1 | 2 | Timing differences MUST be classified separately from breaks using declared windows. | Settlement fixture classifies T+1 items as timing. | test |

## ai

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-AI-001 | P1 | 3 | AI assistance MUST produce proposals only as PipelineDiff documents with rationale and confidence; it MUST NOT execute, publish, approve or load. | Assistant tool surface is read-only plus propose. | test |
| TRN-REQ-AI-002 | P0 | 3 | AI-generated configuration MUST pass the same deterministic validation, dry run and authorization gates as human changes. | Proposal acceptance path identical; tests. | test |
| TRN-REQ-AI-003 | P0 | 3 | Source data, documents and external metadata MUST be treated as untrusted, passed as delimited data with provenance tags. | Prompt construction tests. | test |
| TRN-REQ-AI-004 | P0 | 3 | Prompt injection MUST NOT be able to change pipeline authority or execution behaviour; an adversarial corpus MUST run in CI. | No authority-widening diff accepted across the corpus. | test |
| TRN-REQ-AI-005 | P0 | 1 | Identical raw inputs, pipeline version, package versions, reference data versions, execution parameters and engine version MUST produce equivalent deterministic results; the runtime path MUST contain no model calls. | Replay determinism test; dependency scan of Engine finds no AI provider. | test |
| TRN-REQ-AI-006 | P1 | 3 | AI proposals MUST record model, provider, prompt template version and input/output hashes in pipeline provenance. | Provenance present on accepted proposals. | test |
| TRN-REQ-AI-007 | P0 | 3 | By default AI MUST receive schema metadata and synthetic or masked samples only; real samples require tenant policy permission and an approved provider for the data classification. | Classification-gated prompt builder tests. | test |
| TRN-REQ-AI-008 | P2 | 3 | AI mapping accuracy MUST be measured against ground-truth packages before any accuracy claim is made. | Evaluation harness report. | review |

## mapping-packages

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-MP-001 | P0 | 1 | Mapping packages MUST be versioned, content-hashed, configuration-only bundles that contain no customer data and no code. | Package lint rejects code files and non-synthetic fixtures. | test |
| TRN-REQ-MP-002 | P0 | 1 | Each package MUST declare the basis of its format knowledge (public specification, public API documentation, customer-authorized sample, synthetic representation); proprietary vendor schemas MUST NOT be invented. | Manifest basis required by schema; review checklist. | review |
| TRN-REQ-MP-003 | P0 | 1 | Customer-specific configuration MUST be expressed as overlays restricted to package-declared paths, not as forks. | Overlay touching undeclared path is rejected. | test |
| TRN-REQ-MP-004 | P1 | 3 | Packages MUST declare accepted source format versions with detectors and provide a dry-run upgrade diff against fixtures and recent raw inputs. | Upgrade command produces deterministic output diff. | test |
| TRN-REQ-MP-005 | P1 | 3 | Promotion of improvements from customer overlays to base packages MUST carry no customer values and require disclosure review. | Promotion checklist and synthetic fixture regeneration. | review |

## lineage-evidence

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-LN-001 | P0 | 2 | Every material destination record MUST be traceable to original source, source record identifier, source version, pipeline version, mapping version, operations, reference data versions, validation results, authorization decision, execution identifier and destination response. | Lineage query returns all elements for a loaded record. | test |
| TRN-REQ-LN-002 | P0 | 2 | Field-level lineage MUST be provided statically per pipeline version; per-record field values MUST NOT be stored except for fields marked lineageCaptureValue (selection codes only). | Static graph present; storage test shows no per-field value table. | test |
| TRN-REQ-LN-003 | P0 | 2 | Every execution MUST produce an evidence package (manifest, conservation table, validation, reconciliation, approvals, receipts summary, exceptions summary, hash chain). | Evidence stage output validated against schema. | test |
| TRN-REQ-LN-004 | P1 | 4 | Evidence reports MUST be renderable through Folio. | Folio template renders a fixture package. | test |
| TRN-REQ-LN-005 | P0 | 2 | Approvals MUST be recorded as signed events with identity, timestamp, plan hash and validation snapshot hash. | Approval events verify. | test |
| TRN-REQ-LN-006 | P0 | 2 | Evidence MUST be hash-chained per execution and anchored in an append-only per-tenant chain. | Tampering fixture detected. | test |
| TRN-REQ-LN-007 | P1 | 2 | Operational telemetry MUST be emitted via OpenTelemetry through the host; unresolved exceptions and OutcomeUnknown obligations MAY raise Vigila follow-ups when present. | Absent-safe integration test with and without Vigila. | test |
| TRN-REQ-LN-008 | P0 | 2 | Logs, telemetry and evidence MUST NOT contain values of fields classified above internal. | Log-leak test suite. | test |
| TRN-REQ-LN-009 | P2 | 4 | OpenLineage RunEvent export MAY be provided as an optional adapter. | Export validates against OpenLineage spec. | test |

## security

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-SEC-001 | P0 | 2 | Parsers MUST be pure over byte streams with no ambient authority, pinned versions and continuous fuzzing. | Fuzz corpus runs in CI. | test |
| TRN-REQ-SEC-002 | P0 | 2 | Archive handling MUST enforce compressed size, uncompressed size, entry count, nesting depth and compression-ratio limits while streaming. | Zip-bomb fixtures rejected before allocation. | test |
| TRN-REQ-SEC-003 | P0 | 2 | XML parsing MUST prohibit DTDs and external resolution and bound document size. | XXE and billion-laughs fixtures rejected. | test |
| TRN-REQ-SEC-004 | P0 | 2 | Transitus-generated CSV/XLSX MUST neutralize formula-leading cells; imported formulas MUST NOT be evaluated. | Formula-injection fixtures. | test |
| TRN-REQ-SEC-005 | P0 | 2 | Path traversal from archive entries or source names MUST be impossible. | Zip-slip fixtures. | test |
| TRN-REQ-SEC-006 | P0 | 2 | Malformed input MUST produce typed, located errors with no silent repair. | Malformed corpus. | test |
| TRN-REQ-SEC-007 | P0 | 2 | Resource exhaustion MUST be bounded by per-pipeline limits and non-backtracking regex with timeouts. | Limit fixtures. | test |
| TRN-REQ-SEC-008 | P0 | 2 | Data poisoning MUST be mitigated through independent control totals, reference validation, anomaly thresholds and approval gates. | Poisoning fixtures blocked by gates. | test |
| TRN-REQ-SEC-009 | P0 | 2 | Secrets MUST be referenced by name only, resolved from the host secret provider and never persisted in pipelines, staging, lineage, logs or prompts. | Secret-leak scan. | test |
| TRN-REQ-SEC-010 | P0 | 2 | Pipeline changes MUST be authorized, versioned and separated by duty for sensitive classifications. | Publish authorization tests. | test |
| TRN-REQ-SEC-011 | P0 | 2 | Tenant isolation MUST apply to raw, staging, lineage, exceptions and evidence; cross-tenant references MUST be inexpressible. | Cross-tenant fixture rejected. | test |
| TRN-REQ-SEC-012 | P0 | 2 | Staging MUST be encrypted at rest per host policy and purged per TTL with evidence. | Purge evidence. | test |
| TRN-REQ-SEC-013 | P0 | 2 | Destinations MUST be registered by the host and granted per tenant; pipelines cannot introduce destinations. | Unregistered destination rejected. | test |
| TRN-REQ-SEC-014 | P0 | 2 | Third-party parser libraries MUST be isolated and limited and tracked for vulnerabilities. | Dependency scan. | test |
| TRN-REQ-SEC-015 | P0 | 2 | Network egress MUST be restricted to per-adapter-instance allow-lists with redirect checks. | Egress test. | test |
| TRN-REQ-SEC-016 | P0 | 2 | Replays MUST be explicit and produce the original idempotency keys; duplicate raw inputs MUST be detected. | Replay fixture zero effects. | test |
| TRN-REQ-SEC-017 | P0 | 2 | Dependencies MUST be pinned with lock files, SBOM and vulnerability scanning. | CI evidence. | test |
| TRN-REQ-SEC-018 | P0 | 2 | Retention MUST be enforced, with crypto-shredding where physical erasure cannot be guaranteed. | Retention tests. | test |
| TRN-REQ-SEC-019 | P1 | 2 | Transitus MUST produce automated SOC 2 control evidence per the compliance control mapping. | Evidence generators listed in TRN-SEC-02 produce outputs. | test |

## visual-administration

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-UI-001 | P2 | 4 | The administration UI MUST be built on Forma components and Forma's portable workflow capability behind Limen; Transitus MUST NOT build its own graph editor. | Dependency review. | review |
| TRN-REQ-UI-002 | P0 | 4 | The visual graph MUST be a projection of the authoritative JSON definition with a tested round-trip; layout is non-semantic annotation. | Round-trip property test. | test |
| TRN-REQ-UI-003 | P1 | 4 | The UI MUST provide the views listed in TRN-ARCH-10 §3. | View checklist. | test |
| TRN-REQ-UI-004 | P0 | 4 | Every drag-and-drop interaction MUST have an accessible, mobile-friendly alternative; WCAG 2.2 AA. | Accessibility audit. | test |
| TRN-REQ-UI-010 | P0 | 2 | All configuration, execution, approval, exception and lineage operations MUST be available through documented, versioned APIs before any UI exists. | OpenAPI coverage check. | test |

## architecture

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-ARC-001 | P0 | 1 | Transitus MUST be implemented in F# in a functional style as embeddable libraries hosted in a consuming application (component monolith); no independently deployed microservice without explicit architectural approval. | Repository contains no deployable service project. | review |
| TRN-REQ-ARC-002 | P0 | 1 | Transitus MUST consume existing Echelon capabilities (Echelon.Execution, Strata, Forma, Limen, Folio, Aegis) rather than duplicating them. | Dependency analysis kept current. | review |
| TRN-REQ-ARC-003 | P0 | 1 | Every library MUST have unit tests; pure libraries MUST have property-based tests. | CI coverage of all packages. | test |
| TRN-REQ-ARC-004 | P1 | 1 | Infrastructure dependencies MUST be minimal: the host's PostgreSQL and an optional object store only. | Dependency review. | review |
| TRN-REQ-ARC-005 | P1 | 1 | Each new third-party dependency MUST be approved by decision record with licence and supply-chain review. | Decision records exist for each dependency. | review |

## performance

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-PF-001 | P0 | 2 | Every assumption in the performance model MUST be replaced by a measurement before capacity or commercial commitments are made, and theoretical estimates MUST NOT be presented as benchmarks. | Benchmark report per assumption A1-A11. | review |
| TRN-REQ-PF-002 | P1 | 2 | The engine MUST process 10^6-record executions within the host database's capacity without degrading concurrent OLTP latency beyond an agreed budget. | Load test with concurrent OLTP workload. | test |
