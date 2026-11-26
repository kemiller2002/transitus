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

152 proposed requirements (revised after adversarial review TRN-REV-01; rows carry `revision` in JSON). Phases (owner-directed revision, DF-TRN-2026-0018): 1 = minimal declarative typed linear pipeline, basic mapping packages, checkpoints/replay/idempotency, dry runs; 2 = complex DAGs and set operators (T2); 3 = advanced AI and vendor-specific packages (T3); 4 = visual editing (T4) — see `docs/roadmap.md`. Priority: P0 = required for first production use, P1 = required for the phase, P2 = conditional/deferred. Machine-readable: `requirements/requirements.json`.


## pipeline-spec

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-PS-001 | P0 | 1 | Pipelines MUST be versioned, declarative JSON documents conforming to a published JSON Schema and an F# discriminated-union model; the content hash (SHA-256 of RFC 8785 canonical JSON, excluding annotations) identifies a pipeline version. | Two semantically identical pipelines with different key order or layout annotations produce the same hash; schema-invalid documents are rejected with a located error. | test |
| TRN-REQ-PS-002 | P0 | 1 | Every stage MUST declare its kind, inputs (dependsOn), outputs, failure behaviour and the provenance it emits, per the lifecycle table. | Publish-time validator rejects a stage lacking required fields; documentation lists inputs/outputs/state/failure/provenance for all 14 stage kinds. | test |
| TRN-REQ-PS-003 | P0 | 1 | Pipelines whose destination is classified system-of-record MUST include preserve, blocking validate, blocking reconcile, authorize and evidence stages. | Validator rule PV-12 rejects a system-of-record pipeline missing any of these stages. | test |
| TRN-REQ-PS-004 | P0 | 1 | Published pipeline versions MUST be immutable; publishing MUST require an authorized role, and pipelines handling restricted-financial or phi classifications MUST require a second approver. | Attempting to modify a published version fails; single-approver publish of a financial pipeline is refused. | test |
| TRN-REQ-PS-005 | P0 | 1 | Phase-1 control flow MUST be a linear typed stage sequence per pipeline, with per-stage error policies that route records to quarantine, retries on I/O stages and runIf predicates over execution facts. Branching routes, unions, joins across datasets, the bounded set operators of TRN-REQ-TX-011 and other complex DAG constructs are deferred to phase 2 (trigger T2). General loops, recursion, user functions and dynamic stage generation MUST NOT be expressible in any phase. | JSON Schema and validator reject cycles, missing otherwise branches and any construct outside the list. | test |
| TRN-REQ-PS-006 | P0 | 1 | User-configured pipelines MUST NOT contain or evaluate arbitrary executable code, dynamic SQL, JavaScript or unrestricted scripting; extension MUST occur only via reviewed, compiled F# packages governed by TRN-REQ-EXT-001..004. Because .NET cannot sandbox in-process code, extension safety rests on review, signing and allow-listing, not isolation. | No schema field accepts code; fuzzed pipeline documents never cause code loading; an unlisted package reference fails validation. | test |
| TRN-REQ-PS-007 | P1 | 2 | From phase 2 (trigger T2), predicates and computed fields MAY use the typed, total Transitus Expression Language; phase 1 uses the closed vocabulary of TRN-REQ-PS-012 instead. | Type errors are reported at publish; property tests show termination and no exceptions for generated expressions. | test |
| TRN-REQ-PS-008 | P0 | 1 | Publish-time validation MUST compute an authority-and-semantics diff against the prior version and require elevated approval for any widening (new source, destination, egress host, secret slot, classification increase, relaxed gate or tolerance, new loss acknowledgement) and highlighted review for semantic-critical changes (idempotency-key fields, autoApprove conditions, enum/code mappings on financial fields, re-mapping between money or date fields, reference-data version changes). | A diff adding an egress host is flagged and cannot publish with standard approval. | test |
| TRN-REQ-PS-009 | P1 | 1 | Every operation, configuration field, stage kind and error code MUST have AI-readable semantics documentation, generated from or checked against the model. | Documentation-completeness test fails when a DU case lacks semantics text. | test |
| TRN-REQ-PS-010 | P0 | 1 | The phase-1 specification MUST support source, destination and schema definitions, field mappings, type conversion, validation rules, conditional value mapping, lookups against pinned reference sets, filtering with counts, deduplication within a dataset, normalization, relationship resolution through destination lookup, reconciliation rules, error, retry and approval policies, scheduling, resource limits, retention policy references and security classification. Joins and aggregation across datasets are phase 2. | Each listed construct has a schema element and at least one example fixture. | test |
| TRN-REQ-PS-011 | P0 | 1 | Phase 1 MUST provide a minimal declarative typed pipeline: a canonical-JSON document validated against the DU model at publish time, composed linearly of the stage kinds ingest, preserve, parse, stage, transform, validate, reconcile, authorize, load, verify, evidence and retain (profile optional), with every stage's inputs, outputs, state, failure behaviour and provenance as specified in TRN-ARCH-01 §2. | The three demonstration pipelines in examples/pipelines validate against schemas/pipeline-phase1.schema.json. | test |
| TRN-REQ-PS-012 | P0 | 1 | Phase-1 mappings, rules and approval conditions MUST use a closed vocabulary — field maps, the enumerated operations of TRN-REQ-TX-009, and Compare(field, operator, field-or-literal) combined with and/or over fields and execution facts — with no general expression language. | Validator rejects any predicate outside the vocabulary; the three demonstration pipelines need nothing more. | test |

## storage

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-ST-001 | P0 | 1 | Raw inputs MUST be preserved immutably and content-addressed by SHA-256 with tenant, source identifier, source locator, acquisition timestamp, source metadata, adapter version, classification, rights policy and retention class before any parsing; where the source's rights policy does not permit storing bytes, Transitus MUST store the hash, size and a lawful reference instead and record that the bytes were not retained (aligns with Unbound UNB-KNOW RawEvidence 'store raw bytes only when permitted'). | Parse stage cannot start without a committed raw object; metadata row contains all listed fields. | test |
| TRN-REQ-ST-002 | P0 | 1 | Source-supplied file names, paths and keys MUST be stored only as metadata and never used to derive storage paths. | Zip-slip and path traversal fixtures produce no file outside the blob store namespace. | test |
| TRN-REQ-ST-003 | P0 | 1 | Isolated temporary staging MUST respect the consumer's tenancy model (for Unbound, CNV-ARC-001 schema and role per sponsor) and MUST NOT require runtime DDL: staging tables per schema version are created by the host's Strata-governed migrations; bulk loads MUST NOT rely on COPY into row-level-security tables; purge uses DELETE with measured vacuum cost or a governed partition-maintenance mechanism (DEP-STRATA-01). | Execution role lacks DDL privilege; staging tables exist only after a governed migration. | test |
| TRN-REQ-ST-004 | P0 | 1 | Processing MUST NOT require the full dataset to fit in memory; memory use MUST be bounded by the pipeline memory budget independent of record count. | A 10x larger input does not increase peak working set beyond the configured budget (measured). | test |
| TRN-REQ-ST-005 | P0 | 1 | Transformed datasets MUST be sealed by a Merkle root over chunk hashes, and approval and load MUST bind to that root. | Mutating a staged row after approval causes load to refuse with HASH_MISMATCH. | test |
| TRN-REQ-ST-006 | P0 | 1 | Staging MUST have an enforced TTL, MUST NOT be exposed through general query APIs, and MUST NOT be used as a source by any other tenant or application. | Sweeper purges expired partitions and records purge evidence; no API returns staged rows except bounded, classification-masked previews. | test |
| TRN-REQ-ST-007 | P1 | 1 | The blob store MUST be a port with a PostgreSQL-backed default, subject to sizing evidence, and an optional S3-compatible implementation. | Conformance tests pass for both implementations. | test |
| TRN-REQ-ST-008 | P2 | 4 | File-backed columnar staging MAY be introduced for executions above ~10^7 records only after measured evidence shows database staging is inadequate, without adding a deployment component. | Decision record cites measurements. | review |
| TRN-REQ-ST-009 | P1 | 2 | The recovery model MUST state that UNLOGGED staging is truncated on crash and recovery then requires re-running staged stages from preserved raw input. | Documented and tested crash recovery. | test |
| TRN-REQ-ST-010 | P1 | 2 | Shared reference datasets (e.g. IRS EO BMF) SHOULD be staged once per deployment as public reference data rather than per tenant, when their classification is public and the consumer's tenancy model permits. | Storage model shows single copy. | test |

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
| TRN-REQ-TX-008 | P1 | 2 | Record matching MUST produce scored candidates; financial entities MUST NOT be auto-merged, and candidates between configured thresholds MUST go to review. | Matching fixtures show no automatic merges for financial entity types. | test |
| TRN-REQ-TX-009 | P1 | 1 | Phase 1 MUST provide exactly the operations the three demonstration pipelines need: text.trim, text.case (invariant), field.require, field.default (with acknowledgeDefault on financial fields), number.parse, money.parse (including an implied-decimal parameter), date.parse, enum.map, id.normalize (including a CUSIP kind), lookup against a pinned reference set, dedupe (reject-all), snapshot-diff by natural key, and privacy.hash (HMAC only); any further operation requires a consumer pipeline that uses it. | Catalogue coverage test enumerates all listed operations. | test |
| TRN-REQ-TX-010 | P0 | 1 | Hashing of low-entropy identifiers MUST use keyed HMAC with a tenant-scoped key; unkeyed hashing of such identifiers MUST be rejected. | Validator rejects privacy.hash with sha256 on fields typed ssn/ein/phone. | test |
| TRN-REQ-TX-011 | P1 | 2 | The declarative model MUST provide bounded set operators: ordered scan (fill-down, running total with explicit order key), as-of join against date-effective reference data, date arithmetic and fiscal-period derivation, unpivot of repeated columns, bounded explode of schedules (declared maximum), duplicate clustering (connected components with maximum cluster size) and linear-time regex capture; each terminates in bounded time and space. | Counter-example fixtures from TRN-REV-01 C4 (U1, U9, U10, H1, H2) are expressible. | test |

## adapters

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-AD-001 | P0 | 1 | Adapters MUST be separated into transport, format and destination roles behind published F# contracts, independently packaged, with the core depending only on the abstractions. | A new format adapter is added and passes conformance without changes to Transitus.Engine. | test |
| TRN-REQ-AD-002 | P0 | 1 | Every adapter MUST declare capabilities, configuration schema, secret slots, egress derivation and an error taxonomy mapped to Transient, RateLimited, AuthFailure, PermanentInput, PermanentConfig or Ambiguous. | Descriptor validates against schemas/adapter-descriptor.schema.json; unknown write errors classify as Ambiguous. | test |
| TRN-REQ-AD-003 | P0 | 1 | Adapters MUST support connection testing without mutation and MUST ship synthetic fixtures for conformance testing. | Conformance suite runs every adapter's Test and fixtures offline. | test |
| TRN-REQ-AD-004 | P0 | 1 | Incremental transports MUST persist opaque, versioned checkpoints that advance only after downstream stage commit. | Crash after acquisition but before stage commit re-acquires the same items. | test |
| TRN-REQ-AD-005 | P0 | 1 | Adapters MUST be built only for scenarios in Unbound release scope or a committed second consumer. Phase-1 formats: CSV/TSV (IRS EO BMF, Pub 78, auto-revocation, OFAC SDN, state registries), fixed-width/NACHA (returns, NOC), BAI2 or camt.053 (one bank activity feed), XLSX (read-only, cached values), one custodian file format; transports remain in the host (upload, HTTPS, SFTP) until phase 2. | Adapter catalogue lists the driving scenario for each adapter. | review |
| TRN-REQ-AD-006 | P0 | 1 | Adapters MUST honour rate limits and Retry-After, and MUST NOT implement internal retry loops; retries are engine-owned. | Adapter conformance asserts single attempt per call. | test |
| TRN-REQ-AD-007 | P0 | 1 | Destination adapters MUST declare a delivery guarantee (idempotent-key, natural-upsert, query-before-write, none) and support read-back where the destination allows. | Engine selects retry/verification policy from the declared guarantee. | test |
| TRN-REQ-AD-008 | P0 | 1 | Loads into regulated Unbound workflows MUST occur through Unbound domain APIs or approved domain interfaces; Transitus MUST NOT hold credentials to write business tables directly. | Unbound destination adapter uses only published domain operations; no database credentials for Unbound business schemas exist in Transitus configuration. | test |
| TRN-REQ-AD-009 | P1 | 1 | Snapshot-diff by natural key MUST be supported for full-file feeds. | BMF fixture yields correct adds, changes and removals versus the prior snapshot. | test |
| TRN-REQ-AD-010 | P2 | 2 | Bidirectional synchronization and conflict resolution MUST NOT be built; outbound flows are separate one-directional pipelines. | Scope review. | review |
| TRN-REQ-AD-011 | P0 | 1 | Bulk loads into Unbound MUST use a configurable share of the sponsor's Echelon.Execution queue quota, a lower priority than interactive commands, and a separate worker role, so imports cannot throttle live donor operations. | Load test: interactive command latency within budget during a bulk load. | test |
| TRN-REQ-AD-012 | P0 | 1 | Historical-import (pre-go-live) batch domain operations MAY be used only while the sponsor programme is not live, and only through Unbound-defined operations that preserve per-record idempotency keys and receipts; post-go-live loads use per-record commands. | Unbound operation contract review (UNB-TRN-006). | test |

## execution

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-EX-001 | P0 | 1 | Durable execution MUST be provided by Echelon.Execution, used in place until its shared contract is stable (owner resolution of OQ-01), and reached only through the TRN-REQ-ARC-011 port implemented by the host; Transitus MUST NOT implement a separate queue. | Transitus.Engine has no queue tables; stage commands appear in Echelon.Execution history. | review |
| TRN-REQ-EX-002 | P0 | 1 | The engine MUST implement an explicit pipeline execution state machine including Blocked, PartiallyLoaded and OutcomeUnknown states whose legal transitions are defined by a total pure function. | Exhaustive transition tests; illegal transitions return errors. | test |
| TRN-REQ-EX-003 | P0 | 1 | Phase 1 MUST support manual, host-triggered (including host-scheduled), dry-run and replay execution, batch and file-set incremental; scheduling materialization inside Transitus is phase 2 (EX-012). | Each mode has an acceptance test. | test |
| TRN-REQ-EX-004 | P0 | 1 | Dry runs MUST execute stages 1-9 and produce a load plan without writing to any system of record. | Dry run against the Unbound adapter performs zero domain commands. | test |
| TRN-REQ-EX-005 | P0 | 1 | Phase 1 MUST checkpoint at stage granularity (plus per-item intent and receipt in load, TRN-REQ-EX-008) so that resumption never repeats a committed stage or load item; chunk-level parallelism is phase 2. | Kill a worker mid-run; resumed run produces identical outputs with no duplicate chunks. | test |
| TRN-REQ-EX-006 | P0 | 1 | Each destination record MUST carry a deterministic idempotency key derived from tenant, pipeline, destination, declared natural key and business date. | Replay produces identical keys; destination dedupes. | test |
| TRN-REQ-EX-007 | P0 | 1 | Transitus MUST NOT claim exactly-once delivery; unknown external outcomes MUST NOT be blindly retried: they enter OutcomeUnknown and are resolved by verification, reconciliation or authorized human resolution. | Simulated timeout after send yields OutcomeUnknown and no retry. | test |
| TRN-REQ-EX-008 | P0 | 1 | Load intent MUST be committed before the external call and the receipt after it; no transaction spans the network. | Crash-injection test at each point leaves a resolvable state. | test |
| TRN-REQ-EX-009 | P0 | 1 | Compensation of loaded financial records MUST NOT be automatic. | No code path issues reversal commands. | review |
| TRN-REQ-EX-010 | P0 | 1 | Resource limits (input bytes, record bytes, records, nesting depth, archive entries and ratio, memory budget, parallelism, CPU time) and backpressure MUST be enforced. | Limit fixtures fail fast with typed errors; queue depth stays bounded under slow destinations. | test |
| TRN-REQ-EX-011 | P1 | 1 | Cancellation MUST be cooperative and MUST NOT leave unrecorded external effects. | Cancel during load; all in-flight receipts recorded. | test |
| TRN-REQ-EX-012 | P1 | 2 | Schedules MUST declare an IANA time zone and misfire policy and be materialized as ScheduledCommands, without a separate scheduler service. | DST transition fixtures schedule correctly. | test |
| TRN-REQ-EX-013 | P0 | 1 | Durable command payloads (Echelon.Execution) MUST carry dataset/record references and hashes only, never record values classified restricted-personal or above (consistent with Unbound CNV-ARC-001 vault references). | Payload classification test. | test |
| TRN-REQ-EX-014 | P0 | 1 | Replay of a recorded execution manifest MUST be explicit, MUST reproduce identical staged outputs, and MUST reuse the original idempotency keys so that a replay into a destination produces no duplicate business effects. | Replay fixture: byte-identical staged output hashes; zero additional destination effects. | test |

## validation-reconciliation

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-VR-001 | P0 | 1 | Transitus MUST provide generic validation primitives for required, type, range, pattern, code set, check digit, cross-field, uniqueness, referential integrity, completeness, sequence, freshness and distribution. | Primitive catalogue tests. | test |
| TRN-REQ-VR-002 | P0 | 1 | Transitus MUST provide reconciliation primitives for counts, control totals, hash totals, balance (opening + movements = closing), keyed set matching, cross-file, cross-system and timing differences. | Primitive catalogue tests including NACHA control and hash totals. | test |
| TRN-REQ-VR-003 | P0 | 1 | Monetary reconciliation tolerance MUST default to zero; non-zero tolerances MUST be declared with justification and appear in evidence. | Profile without tolerance treats a one-cent difference as Unbalanced. | test |
| TRN-REQ-VR-004 | P0 | 1 | Blocking validation and reconciliation gates MUST prevent all downstream stages, including load, when they fail. | Failing gate leaves execution Blocked with zero destination effects. | test |
| TRN-REQ-VR-005 | P0 | 1 | In phase 1 blocking gates MUST NOT be overridable: a failed gate stops the execution, and remediation is a corrected mapping, reference data or source followed by a new execution. Evidenced elevated overrides may be introduced later only by decision record. | Override evidence present; staged data hash unchanged. | test |
| TRN-REQ-VR-006 | P0 | 1 | Unbound-specific accounting rules MUST live in Unbound-owned profiles, not in Transitus core. | No Unbound domain terms in Transitus core packages (dependency/term scan). | review |
| TRN-REQ-VR-007 | P0 | 1 | Every stage MUST satisfy the conservation law in = out + rejected + quarantined + deduplicated + filteredWithCount; discards without counts MUST be impossible. | Engine assertion; mutation test that drops a record fails the execution. | test |
| TRN-REQ-VR-008 | P0 | 1 | Record-level exceptions MUST be typed, grouped by code and resolvable only by mapping change, reference data, corrected source or approved exclusion; staged values MUST NOT be hand-edited. | No API mutates staged values. | test |
| TRN-REQ-VR-009 | P0 | 1 | Transitus MUST NOT introduce balancing entries, write-offs, suspense entries or silently discarded records. | Review and tests: no operation emits synthetic financial records. | review |
| TRN-REQ-VR-010 | P0 | 1 | Post-load verification MUST reconcile planned, loaded and read-back counts and totals. | Verify stage report present in evidence for every system-of-record load. | test |
| TRN-REQ-VR-011 | P1 | 1 | Duplicate detection MUST operate within file, execution and destination (via read-back) scopes. | Fixtures for each scope. | test |
| TRN-REQ-VR-012 | P1 | 2 | Timing differences MUST be classified separately from breaks using declared windows. | Settlement fixture classifies T+1 items as timing. | test |
| TRN-REQ-VR-013 | P0 | 1 | Financial-correctness gates (blocking validation and reconciliation for restricted-financial data) and tenant isolation MUST be blocking in every phase and MUST NOT be disableable by pipeline configuration; only an elevated, evidenced override (TRN-REQ-VR-005) may proceed past a failed gate, and nothing may override tenant isolation. | Validator rejects a financial system-of-record pipeline with advisory-only gates; cross-tenant reference rejected. | test |

## ai

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-AI-001 | P1 | 3 | AI assistance MUST produce proposals only as PipelineDiff documents with rationale and confidence; it MUST NOT execute, publish, approve or load. | Assistant tool surface is read-only plus propose. | test |
| TRN-REQ-AI-002 | P1 | 3 | AI-generated configuration MUST pass the same deterministic validation, dry run and authorization gates as human changes. | Proposal acceptance path identical; tests. | test |
| TRN-REQ-AI-003 | P1 | 3 | Source data, documents, external metadata and non-semantic annotations MUST be treated as untrusted and passed as delimited data with provenance tags; annotations MUST be excluded from AI context unless explicitly selected. | Prompt construction tests. | test |
| TRN-REQ-AI-004 | P1 | 3 | Prompt injection MUST NOT be able to change pipeline authority or execution behaviour; an adversarial corpus MUST run in CI. | No authority-widening diff accepted across the corpus. | test |
| TRN-REQ-AI-005 | P0 | 1 | Identical raw inputs, pipeline version, package versions, reference data versions, execution parameters and engine version MUST produce equivalent deterministic results; the runtime path MUST contain no model calls. | Replay determinism test; dependency scan of Engine finds no AI provider. | test |
| TRN-REQ-AI-006 | P1 | 3 | AI proposals MUST record model, provider, prompt template version and input/output hashes in pipeline provenance. | Provenance present on accepted proposals. | test |
| TRN-REQ-AI-007 | P1 | 3 | By default AI MUST receive schema metadata and synthetic or masked samples only; profile statistics inherit their field's classification and MUST be masked accordingly; any use of real samples requires authorization for that tenant and data classification. | Classification-gated prompt builder tests. | test |
| TRN-REQ-AI-008 | P0 | 3 | AI mapping accuracy MUST be measured against ground-truth packages before any accuracy claim is made. | Evaluation harness report. | review |
| TRN-REQ-AI-009 | P1 | 3 | AI enablement per tenant and pipeline class MUST be gated on the TRN-REQ-AI-008 evaluation meeting recorded precision thresholds; below threshold, AI suggestions are disabled for that class. | Gate configuration test. | test |
| TRN-REQ-AI-010 | P1 | 3 | AI assistance MUST be provider-independent; use of any provider MUST be authorized per tenant and data classification, with no blanket provider approval (owner resolution of OQ-08). | Provider authorization check per request. | test |

## mapping-packages

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-MP-001 | P0 | 1 | Basic mapping packages (public-specification and target-side canonical packages) MUST be versioned, content-hashed, configuration-only bundles with no customer data and no code, and MUST be reusable across tenants without requiring a signed customer. | Package lint rejects code files and non-synthetic fixtures. | test |
| TRN-REQ-MP-002 | P0 | 1 | Each package MUST declare the basis of its format knowledge (public specification, public API documentation, customer-authorized sample, synthetic representation); proprietary vendor schemas MUST NOT be invented; packages derived from a vendor export MUST record a licence/contract clearance (e.g. vendor MSA anti-competitive-use and reverse-engineering clauses) before publication. | Manifest basis required by schema; review checklist. | review |
| TRN-REQ-MP-003 | P1 | 2 | Customer-specific configuration MUST be expressed as overlays restricted to package-declared paths, not as forks. | Overlay touching undeclared path is rejected. | test |
| TRN-REQ-MP-004 | P1 | 1 | Packages MUST declare accepted source format versions with detectors and provide a dry-run upgrade diff against fixtures and recent raw inputs. | Upgrade command produces deterministic output diff. | test |
| TRN-REQ-MP-005 | P1 | 3 | Promotion of improvements from customer overlays to base packages MUST carry no customer values, MUST be supported by at least two independent customer samples, and MUST pass disclosure and vendor-licence review. | Promotion checklist and synthetic fixture regeneration. | review |
| TRN-REQ-MP-006 | P0 | 1 | Phase-1 packages MUST be target-side or public-specification packages only: IRS EO BMF (and Pub 78/auto-revocation), NACHA returns/NOC (subject to TRN-REQ-MP-008), the first bank partner's activity format, the Schwab custodian format (subject to obtaining its documentation under acceptable terms) and the Unbound canonical historical import; vendor-specific turnkey packages follow in phase 3. | Roadmap ordering. | review |
| TRN-REQ-MP-007 | P1 | 1 | Package reuse MUST be measured from phase 1 (share of mappings reused unmodified per execution and per sponsor); vendor packages are retired if reuse stays below an agreed threshold after three migrations. | Reuse metric per migration. | test |
| TRN-REQ-MP-008 | P0 | 1 | Redistribution rights for format knowledge MUST be verified before publication: the NACHA Operating Rules licence for nacha.* packages and the Schwab documentation terms for custodian.schwab.* packages; until verified, the package is internal-only. | Rights verification record per package. | review |
| TRN-REQ-MP-009 | P0 | 1 | Phase 1 MUST demonstrate, at least theoretically, three versioned basic packages and pipelines: IRS EO BMF ingestion, a bank (first partner format) or Schwab custodian feed, and the Unbound canonical historical migration including a migration rehearsal (dry run against a sponsor's export with full reconciliation and evidence, no system-of-record effect). | Worked examples in examples/ validate; rehearsal evidence package specified. | test |

## lineage-evidence

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-LN-001 | P0 | 1 | Every material destination record MUST be traceable to original source, source record identifier, source version, pipeline version, mapping version, operations, reference data versions, validation results, authorization decision, execution identifier and destination response. | Lineage query returns all elements for a loaded record. | test |
| TRN-REQ-LN-002 | P0 | 1 | Field-level lineage MUST be provided statically per pipeline version; per-record field values MUST NOT be stored except selection codes for fields marked lineageCaptureValue; natural keys of records classified restricted-personal or above MUST be stored as tenant-keyed HMACs, not in clear text. | Static graph present; storage test shows no per-field value table. | test |
| TRN-REQ-LN-003 | P0 | 1 | Every execution MUST produce an evidence package (manifest, conservation table, validation, reconciliation, approvals, receipts summary, exceptions summary, hash chain). | Evidence stage output validated against schema. | test |
| TRN-REQ-LN-004 | P1 | 2 | Evidence reports MUST be renderable through Folio. | Folio template renders a fixture package. | test |
| TRN-REQ-LN-005 | P0 | 1 | Approvals MUST be recorded as signed events with identity, timestamp, plan hash and validation snapshot hash. | Approval events verify. | test |
| TRN-REQ-LN-006 | P0 | 1 | Evidence MUST be hash-chained per execution and anchored in an append-only per-tenant chain. | Tampering fixture detected. | test |
| TRN-REQ-LN-007 | P1 | 1 | Operational telemetry MUST be emitted via OpenTelemetry through the host; unresolved exceptions and OutcomeUnknown obligations MAY raise Vigila follow-ups when present. | Absent-safe integration test with and without Vigila. | test |
| TRN-REQ-LN-008 | P0 | 1 | Logs, telemetry and evidence MUST NOT contain values of fields classified above internal. | Log-leak test suite. | test |
| TRN-REQ-LN-009 | P2 | 4 | OpenLineage RunEvent export MAY be provided as an optional adapter. | Export validates against OpenLineage spec. | test |
| TRN-REQ-LN-010 | P1 | 1 | Retention for raw input, staging, exceptions, lineage, Transitus-originated Echelon.Execution history and evidence MUST be taken from approved classification and sponsor policy references; Transitus MUST NOT define binding default durations, and durations in examples are illustrative. | Retention configuration test. | test |

## security

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-SEC-001 | P0 | 1 | Parsers MUST be pure over byte streams with no ambient authority, pinned versions and continuous fuzzing. | Fuzz corpus runs in CI. | test |
| TRN-REQ-SEC-002 | P0 | 1 | Archive handling MUST enforce compressed size, uncompressed size, entry count, nesting depth and compression-ratio limits while streaming. | Zip-bomb fixtures rejected before allocation. | test |
| TRN-REQ-SEC-003 | P0 | 1 | XML parsing MUST prohibit DTDs and external resolution and bound document size. | XXE and billion-laughs fixtures rejected. | test |
| TRN-REQ-SEC-004 | P0 | 1 | Transitus-generated CSV/XLSX MUST neutralize formula-leading cells; imported formulas MUST NOT be evaluated. | Formula-injection fixtures. | test |
| TRN-REQ-SEC-005 | P0 | 1 | Path traversal from archive entries or source names MUST be impossible. | Zip-slip fixtures. | test |
| TRN-REQ-SEC-006 | P0 | 1 | Malformed input MUST produce typed, located errors with no silent repair. | Malformed corpus. | test |
| TRN-REQ-SEC-007 | P0 | 1 | Resource exhaustion MUST be bounded by per-pipeline limits and non-backtracking regex with timeouts. | Limit fixtures. | test |
| TRN-REQ-SEC-008 | P0 | 1 | Data poisoning MUST be mitigated through independent control totals, reference validation, anomaly thresholds and approval gates. | Poisoning fixtures blocked by gates. | test |
| TRN-REQ-SEC-009 | P0 | 1 | Secrets MUST be referenced by name only, resolved from the host secret provider and never persisted in pipelines, staging, lineage, logs or prompts. | Secret-leak scan. | test |
| TRN-REQ-SEC-010 | P0 | 1 | Pipeline changes MUST be authorized, versioned and separated by duty for sensitive classifications. | Publish authorization tests. | test |
| TRN-REQ-SEC-011 | P0 | 1 | Tenant isolation MUST apply to raw, staging, lineage, exceptions and evidence; cross-tenant references MUST be inexpressible. | Cross-tenant fixture rejected. | test |
| TRN-REQ-SEC-012 | P0 | 1 | Staging MUST be encrypted at rest per host policy and purged per TTL with evidence. | Purge evidence. | test |
| TRN-REQ-SEC-013 | P0 | 1 | Destinations MUST be registered by the host and granted per tenant; pipelines cannot introduce destinations. | Unregistered destination rejected. | test |
| TRN-REQ-SEC-014 | P0 | 1 | Third-party parser libraries MUST be isolated and limited and tracked for vulnerabilities. | Dependency scan. | test |
| TRN-REQ-SEC-015 | P0 | 1 | Network egress MUST be restricted to per-adapter-instance allow-lists with redirect checks. | Egress test. | test |
| TRN-REQ-SEC-016 | P0 | 1 | Replays MUST be explicit and produce the original idempotency keys; duplicate raw inputs MUST be detected. | Replay fixture zero effects. | test |
| TRN-REQ-SEC-017 | P0 | 1 | Dependencies MUST be pinned with lock files, SBOM and vulnerability scanning. | CI evidence. | test |
| TRN-REQ-SEC-018 | P0 | 1 | Retention MUST be enforced, with per-dataset encryption keys (crypto-shredding) for staging and raw data so that copies in WAL archives and backups become unreadable at purge; where crypto-shredding is not used, the backup retention window MUST be documented as the effective retention. | Retention tests. | test |
| TRN-REQ-SEC-019 | P1 | 2 | Transitus MUST produce automated SOC 2 control evidence per the compliance control mapping. | Evidence generators listed in TRN-SEC-02 produce outputs. | test |
| TRN-REQ-SEC-020 | P0 | 1 | Negative tenant-isolation tests MUST cover raw evidence, staging, exceptions, the evidence chain, reference sets, HMAC keys and the durable-command port (CNV-ARC-001). | Cross-tenant access attempts fail in every listed store. | test |

## visual-administration

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-UI-001 | P2 | 4 | If (and only if) trigger T4 is met, the administration UI MUST be built on Forma components and Forma's portable workflow capability behind Limen; Transitus MUST NOT build its own graph editor. | Dependency review. | review |
| TRN-REQ-UI-002 | P2 | 4 | The visual graph MUST be a projection of the authoritative JSON definition with a tested round-trip; layout is non-semantic annotation. | Round-trip property test. | test |
| TRN-REQ-UI-003 | P1 | 4 | The UI MUST provide the views listed in TRN-ARCH-10 §3. | View checklist. | test |
| TRN-REQ-UI-004 | P2 | 4 | Every drag-and-drop interaction MUST have an accessible, mobile-friendly alternative; WCAG 2.2 AA. | Accessibility audit. | test |
| TRN-REQ-UI-010 | P1 | 1 | All configuration, execution, approval, exception and lineage operations MUST be available as documented library APIs; HTTP exposure is the host application's decision. | OpenAPI coverage check. | test |
| TRN-REQ-UI-011 | P1 | 1 | Exceptions requiring human resolution MUST be surfaced through the consuming application's existing case/work-item system (for Unbound, its case system) rather than a Transitus-specific queue UI. | Integration via library callback. | test |

## architecture

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-ARC-001 | P0 | 1 | Transitus MUST be implemented in F# in a functional style as embeddable libraries hosted in a consuming application (component monolith); no independently deployed microservice without explicit architectural approval. | Repository contains no deployable service project. | review |
| TRN-REQ-ARC-002 | P0 | 1 | Transitus MUST consume existing Echelon capabilities (Echelon.Execution, Strata, Forma, Limen, Folio, Aegis) rather than duplicating them. | Dependency analysis kept current. | review |
| TRN-REQ-ARC-003 | P0 | 1 | Every library MUST have unit tests; pure libraries MUST have property-based tests. | CI coverage of all packages. | test |
| TRN-REQ-ARC-004 | P0 | 1 | Infrastructure dependencies MUST be minimal: the host's PostgreSQL and an optional object store only. | Dependency review. | review |
| TRN-REQ-ARC-005 | P0 | 1 | Each new third-party dependency MUST be approved by decision record with licence and supply-chain review. | Decision records exist for each dependency. | review |
| TRN-REQ-ARC-006 | P0 | 1 | Transitus MUST NOT re-implement a capability that an Echelon component or the consuming application already provides; in particular phase 1 MUST port, not duplicate, the IRS/OFAC parsing in Unbound.Replay/Sources.fs, and MUST adopt Unbound's SourceRegistry/AcquisitionRun/RawEvidence model rather than a competing one. | Duplication review per phase; Unbound.Replay consumes Transitus.Formats or the parsers move. | review |
| TRN-REQ-ARC-007 | P0 | 1 | Each phase MUST declare a maintenance budget and MUST NOT exceed it without a decision record. Phase-1 budget: at most seven code packages (Model including the definition validator, Formats, Transforms, Checks, Evidence, Engine, Storage.Postgres; a five-package variant merging Transforms, Checks and Evidence is acceptable), at most two third-party parser libraries, at most five basic mapping packages, at most thirteen operations, and two cross-repository ports (durable commands, domain destination). | Package count check in CI. | review |
| TRN-REQ-ARC-008 | P0 | 1 | Every phase-1 work item MUST trace to an Unbound release-1 requirement or to the owner-directed phase-1 scope (DF-TRN-2026-0018). | Traceability table in roadmap. | review |
| TRN-REQ-ARC-009 | P0 | 1 | Capabilities beyond phase 1 MUST be gated by recorded triggers: T2 complex DAGs (routes, unions, joins), the expression language, bounded set operators, extensions, chunk parallelism and in-engine scheduling (a demonstrated scenario the phase-1 model cannot express); T3 advanced AI and vendor-specific turnkey packages (AI evaluation thresholds met; customer-authorized sample and licence clearance); T4 visual editing (non-engineer configuration required). Basic mapping packages are not gated. | Decision record per phase gate. | review |
| TRN-REQ-ARC-010 | P0 | 1 | Strata data-interaction virtualization (DIV) virtualizes application interactions; Transitus moves data. Transitus adapters MAY be exercised under DIV replay in tests; neither component re-implements the other's responsibility (owner resolution of OQ-02). | Boundary review at phase-1 exit. | review |
| TRN-REQ-ARC-011 | P0 | 1 | The engine MUST depend only on a durable-command port and a domain-destination port implemented by the host; it MUST NOT reference or copy the Echelon.Execution assembly. A stable port contract is the precondition for extracting Echelon.Execution (OQ-01). | Dependency scan of Transitus packages finds no Echelon.Execution reference; a fake port drives the engine tests. | review |

## performance

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-PF-001 | P0 | 1 | Every assumption in the performance model (A1-A12) MUST be replaced by a measurement, including Echelon.Execution per-command storage and per-record domain-command cost on the Unbound benchmark instance, before capacity or commercial commitments are made; theoretical estimates MUST NOT be presented as benchmarks. | Benchmark report per assumption A1-A11. | review |
| TRN-REQ-PF-002 | P0 | 1 | Bulk loads MUST NOT degrade the sponsor's live OLTP latency beyond an agreed budget; load rate MUST be governed by a configurable share of the sponsor's queue quota (see TRN-REQ-AD-011). | Load test with concurrent OLTP workload. | test |
| TRN-REQ-PF-003 | P1 | 1 | The storage model MUST include Echelon.Execution command, history and outbox rows per loaded record (estimated 1.5-3 KB) in addition to Transitus lineage. | Storage model revised and later measured. | review |
| TRN-REQ-PF-004 | P1 | 1 | The phase-1 approach MUST be measured against hand-written per-feed alternatives for the three demonstration scenarios within six months of phase-1 exit, using effort per feed, defect escape rate and change lead time; if the hand-written alternative is materially better on all three and no second consumer exists, the owner decides whether to retire or fold the engine. The measurement does not gate phase 1 (owner direction). | Comparison in phase-1 exit review. | review |
| TRN-REQ-PF-005 | P0 | 1 | Before Unbound go-live the following MUST be measured: per-record domain-command cost on the RM-05 instance, staging insert rate under row-level security without COPY, and the longest stage handler time against the Echelon.Execution lease. | Benchmark report. | review |

## extensions

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-EXT-001 | P1 | 2 | Extensions MUST be compiled F# packages on a host allow-list, pinned by hash, with signatures that receive no I/O capability (values or bounded record sequences in, Results out). | Allow-list and signature checks. | test |
| TRN-REQ-EXT-002 | P1 | 2 | Extensions MUST pass the conformance suite (determinism across cultures/time zones, totality fuzzing, documentation completeness) and two-person code review before allow-listing. | Conformance report and review record. | test |
| TRN-REQ-EXT-003 | P1 | 2 | Extensions MAY implement set-level stage operators (not only per-value operations) when the declarative catalogue cannot express a demonstrated scenario; each such extension MUST be recorded with the scenario that required it, as input to catalogue evolution. | Extension register. | test |
| TRN-REQ-EXT-004 | P1 | 2 | Extension versions MUST be recorded in the execution manifest and changes MUST be treated as semantic-critical changes under TRN-REQ-PS-008. | Manifest includes extension hashes. | test |

## migration

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-MIG-001 | P0 | 1 | Migration rehearsal MUST run the canonical historical migration pipeline end to end and load only into an isolated, disposable sponsor cell provided by the host (never the live sponsor schema), be repeatable from preserved raw input with identical idempotency keys, and produce a conservation table and per-fund balance reconciliation. | Rehearsal evidence package; repeat run yields identical keys and outputs; live schema untouched. | test |
| TRN-REQ-MIG-002 | P0 | 1 | The canonical-history package MUST stamp source system, source record identifier, import batch and imported_unverified on every imported standing-data and history record (RR-REQ-X-061-r1). | Validation rule fails any record lacking the stamps. | test |
| TRN-REQ-MIG-003 | P0 | 1 | Transitus executions MUST NOT change MigrationRun state; they supply evidence for the Reconciled and ParallelValidated transitions, and a load MUST be refused while the host reports the legacy-writer fence as Unknown (UNB-RCN-WF-020). | Load refused with fence Unknown; MigrationRun transitions only via Unbound. | test |
| TRN-REQ-MIG-004 | P1 | 1 | Documents and acknowledgments in a predecessor export MUST be preserved as RawEvidence and handed unchanged to a host document-import operation, with hash verification on read-back; Transitus does not transform document content. | Document hash equality between raw evidence and destination read-back. | test |

## observability

| ID | P | Phase | Requirement | Acceptance | Verify |
|---|---|---|---|---|---|
| TRN-REQ-OBS-001 | P0 | 1 | Execution state, stage durations, exception counts and OutcomeUnknown obligations MUST be emitted as OpenTelemetry through the host until the portfolio observability owner (GAP-05, OQ-03) is decided. | Telemetry present in host traces and metrics. | test |
