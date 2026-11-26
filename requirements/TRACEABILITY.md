---
id: TRN-REQ-TRACE
title: Transitus Requirements Traceability
status: proposed
version: 0.1.0
created: 2026-11-26
updated: 2026-11-26
generated_by: tools/render_requirements.py (do not hand-edit)
---

# Requirements traceability

Charter section → requirement → design → decision → verification. Charter sections refer to the initiating brief (§1–§22) captured in `PROJECT-CHARTER.md`.

| Requirement | Charter | Design | Decisions | Verification |
|---|---|---|---|---|
| TRN-REQ-PS-001 | §6 | TRN-ARCH-01 §1, §4; schemas/pipeline.schema.json | DF-TRN-2026-0002 | test: Two semantically identical pipelines with different key order or layout annotations produce the same hash; schema-invalid documents are rejected with a located error. |
| TRN-REQ-PS-002 | §4 | TRN-ARCH-01 §2 | DF-TRN-2026-0003 | test: Publish-time validator rejects a stage lacking required fields; documentation lists inputs/outputs/state/failure/provenance for all 14 stage kinds. |
| TRN-REQ-PS-003 | §4, §12 | TRN-ARCH-01 §2; TRN-ARCH-06 §4 | DF-TRN-2026-0011 | test: Validator rule PV-12 rejects a system-of-record pipeline missing any of these stages. |
| TRN-REQ-PS-004 | §14 | TRN-SEC-01 T11 | DF-TRN-2026-0002 | test: Attempting to modify a published version fails; single-approver publish of a financial pipeline is refused. |
| TRN-REQ-PS-005 | §4 | TRN-ARCH-01 §3 | DF-TRN-2026-0003 | test: JSON Schema and validator reject cycles, missing otherwise branches and any construct outside the list. |
| TRN-REQ-PS-006 | §6 | TRN-ARCH-01 §5; TRN-ARCH-04 §5 | DF-TRN-2026-0005 | test: No schema field accepts code; fuzzed pipeline documents never cause code loading; an unlisted package reference fails validation. |
| TRN-REQ-PS-007 | §6 | TRN-ARCH-01 §5 | DF-TRN-2026-0004 | test: Type errors are reported at publish; property tests show termination and no exceptions for generated expressions. |
| TRN-REQ-PS-008 | §9, §14 | TRN-ARCH-01 §6; TRN-ARCH-07 §4 | DF-TRN-2026-0012 | test: A diff adding an egress host is flagged and cannot publish with standard approval. |
| TRN-REQ-PS-009 | §6 | TRN-ARCH-00 P15 | — | test: Documentation-completeness test fails when a DU case lacks semantics text. |
| TRN-REQ-PS-010 | §6 | TRN-ARCH-01 §4; TRN-ARCH-04 §3 | — | test: Each listed construct has a schema element and at least one example fixture. |
| TRN-REQ-ST-001 | §5 | TRN-ARCH-02 §1 | DF-TRN-2026-0008 | test: Parse stage cannot start without a committed raw object; metadata row contains all listed fields. |
| TRN-REQ-ST-002 | §5, §14 | TRN-ARCH-02 §1; TRN-SEC-01 T05 | — | test: Zip-slip and path traversal fixtures produce no file outside the blob store namespace. |
| TRN-REQ-ST-003 | §5 | TRN-ARCH-02 §2 | DF-TRN-2026-0008 | test: Execution role lacks DDL privilege; staging tables exist only after a governed migration. |
| TRN-REQ-ST-004 | §5 | TRN-ARCH-12 §2 | — | test: A 10x larger input does not increase peak working set beyond the configured budget (measured). |
| TRN-REQ-ST-005 | §5 | TRN-ARCH-02 §3 | — | test: Mutating a staged row after approval causes load to refuse with HASH_MISMATCH. |
| TRN-REQ-ST-006 | §5 | TRN-ARCH-02 §6 | — | test: Sweeper purges expired partitions and records purge evidence; no API returns staged rows except bounded, classification-masked previews. |
| TRN-REQ-ST-007 | §5, §16 | TRN-ARCH-02 §1 | DF-TRN-2026-0008 | test: Conformance tests pass for both implementations. |
| TRN-REQ-ST-008 | §5, §18 | TRN-ARCH-12 §3 | DF-TRN-2026-0008 | review: Decision record cites measurements. |
| TRN-REQ-TX-001 | §7 | TRN-ARCH-04 §1 | DF-TRN-2026-0004 | test: Changing golden output of an operation without a major bump fails CI. |
| TRN-REQ-TX-002 | §7 | TRN-ARCH-04 §1 | DF-TRN-2026-0004 | test: Property tests with arbitrary inputs observe no exceptions; operations have no I/O dependencies. |
| TRN-REQ-TX-003 | §7 | TRN-ARCH-04 §4 | — | test: Tests run under different host cultures and TZ produce identical outputs. |
| TRN-REQ-TX-004 | §7 | TRN-ARCH-04 §1, §3 | — | test: Validator rejects truncate/round/mask without acknowledgement; descriptor lists reversibility for every operation. |
| TRN-REQ-TX-005 | §7, §12 | TRN-ARCH-04 §3.2 | — | test: Parsing 1.005 into a 2-scale money field returns PRECISION_LOSS; floats are rejected for Money fields. |
| TRN-REQ-TX-006 | §7 | TRN-ARCH-04 §1 | — | test: Coalescing occurs only via explicit operations; tests cover all three cases per operation. |
| TRN-REQ-TX-007 | §7, §9 | TRN-ARCH-04 §1 | — | test: Replaying with the same manifest yields identical lookup results after reference data has changed. |
| TRN-REQ-TX-008 | §7 | TRN-ARCH-04 §3.6 | — | test: Matching fixtures show no automatic merges for financial entity types. |
| TRN-REQ-TX-009 | §7 | TRN-ARCH-04 §3 | — | test: Catalogue coverage test enumerates all listed operations. |
| TRN-REQ-TX-010 | §7, §14 | TRN-ARCH-04 §3.7 | — | test: Validator rejects privacy.hash with sha256 on fields typed ssn/ein/phone. |
| TRN-REQ-AD-001 | §8 | TRN-ARCH-03 §1, §5 | DF-TRN-2026-0009 | test: A new format adapter is added and passes conformance without changes to Transitus.Engine. |
| TRN-REQ-AD-002 | §8 | TRN-ARCH-03 §1, §2; schemas/adapter-descriptor.schema.json | — | test: Descriptor validates against schemas/adapter-descriptor.schema.json; unknown write errors classify as Ambiguous. |
| TRN-REQ-AD-003 | §8 | TRN-ARCH-03 §3 | — | test: Conformance suite runs every adapter's Test and fixtures offline. |
| TRN-REQ-AD-004 | §8, §11 | TRN-ARCH-03 §3; TRN-ARCH-05 §4 | — | test: Crash after acquisition but before stage commit re-acquires the same items. |
| TRN-REQ-AD-005 | §8 | TRN-ARCH-03 §4 | DF-TRN-2026-0009 | review: Adapter catalogue lists the driving scenario for each adapter. |
| TRN-REQ-AD-006 | §8 | TRN-ARCH-03 §3 | — | test: Adapter conformance asserts single attempt per call. |
| TRN-REQ-AD-007 | §8, §11 | TRN-ARCH-05 §6 | DF-TRN-2026-0007 | test: Engine selects retry/verification policy from the declared guarantee. |
| TRN-REQ-AD-008 | §5, §14 | TRN-ARCH-02 §4; TRN-ARCH-00 P6 | — | test: Unbound destination adapter uses only published domain operations; no database credentials for Unbound business schemas exist in Transitus configuration. |
| TRN-REQ-AD-009 | §8 | TRN-ARCH-03 §6 | — | test: BMF fixture yields correct adds, changes and removals versus the prior snapshot. |
| TRN-REQ-AD-010 | §8 | TRN-ARCH-03 §6 | — | review: Scope review. |
| TRN-REQ-EX-001 | §11, §16 | TRN-ARCH-05 §2 | DF-TRN-2026-0006 | review: Transitus.Engine has no queue tables; stage commands appear in Echelon.Execution history. |
| TRN-REQ-EX-002 | §11 | TRN-ARCH-05 §3 | DF-TRN-2026-0007 | test: Exhaustive transition tests; illegal transitions return errors. |
| TRN-REQ-EX-003 | §11 | TRN-ARCH-05 §4 | — | test: Each mode has an acceptance test. |
| TRN-REQ-EX-004 | §11 | TRN-ARCH-05 §4 | — | test: Dry run against the Unbound adapter performs zero domain commands. |
| TRN-REQ-EX-005 | §11 | TRN-ARCH-05 §5 | — | test: Kill a worker mid-run; resumed run produces identical outputs with no duplicate chunks. |
| TRN-REQ-EX-006 | §11, §14 | TRN-ARCH-05 §6 | DF-TRN-2026-0007 | test: Replay produces identical keys; destination dedupes. |
| TRN-REQ-EX-007 | §11 | TRN-ARCH-05 §6 | DF-TRN-2026-0007 | test: Simulated timeout after send yields OutcomeUnknown and no retry. |
| TRN-REQ-EX-008 | §11 | TRN-ARCH-05 §7 | — | test: Crash-injection test at each point leaves a resolvable state. |
| TRN-REQ-EX-009 | §11, §12 | TRN-ARCH-05 §8 | — | review: No code path issues reversal commands. |
| TRN-REQ-EX-010 | §11, §14 | TRN-ARCH-05 §5; TRN-SEC-01 T07 | — | test: Limit fixtures fail fast with typed errors; queue depth stays bounded under slow destinations. |
| TRN-REQ-EX-011 | §11 | TRN-ARCH-05 §9 | — | test: Cancel during load; all in-flight receipts recorded. |
| TRN-REQ-EX-012 | §11 | TRN-ARCH-05 §4 | — | test: DST transition fixtures schedule correctly. |
| TRN-REQ-VR-001 | §12 | TRN-ARCH-06 §2 | DF-TRN-2026-0011 | test: Primitive catalogue tests. |
| TRN-REQ-VR-002 | §12 | TRN-ARCH-06 §3 | DF-TRN-2026-0011 | test: Primitive catalogue tests including NACHA control and hash totals. |
| TRN-REQ-VR-003 | §12 | TRN-ARCH-06 §3 | — | test: Profile without tolerance treats a one-cent difference as Unbalanced. |
| TRN-REQ-VR-004 | §12 | TRN-ARCH-06 §4 | — | test: Failing gate leaves execution Blocked with zero destination effects. |
| TRN-REQ-VR-005 | §12 | TRN-ARCH-06 §4 | — | test: Override evidence present; staged data hash unchanged. |
| TRN-REQ-VR-006 | §12, §21 | TRN-ARCH-06 §1 | DF-TRN-2026-0011 | review: No Unbound domain terms in Transitus core packages (dependency/term scan). |
| TRN-REQ-VR-007 | §12 | TRN-ARCH-06 §5 | — | test: Engine assertion; mutation test that drops a record fails the execution. |
| TRN-REQ-VR-008 | §12 | TRN-ARCH-06 §6 | — | test: No API mutates staged values. |
| TRN-REQ-VR-009 | §12 | TRN-ARCH-06 §1 | — | review: Review and tests: no operation emits synthetic financial records. |
| TRN-REQ-VR-010 | §11, §12 | TRN-ARCH-05 §6; TRN-ARCH-06 §3; docs/research/03-daf-phase3-dispositions.md | DF-TRN-2026-0025 | test: Verify stage report present in evidence for every system-of-record load. |
| TRN-REQ-VR-011 | §12 | TRN-ARCH-06 §2 | — | test: Fixtures for each scope. |
| TRN-REQ-VR-012 | §12 | TRN-ARCH-06 §3 | — | test: Settlement fixture classifies T+1 items as timing. |
| TRN-REQ-AI-001 | §9 | TRN-ARCH-07 §1, §4 | DF-TRN-2026-0012 | test: Assistant tool surface is read-only plus propose. |
| TRN-REQ-AI-002 | §9 | TRN-ARCH-07 §1 | DF-TRN-2026-0012 | test: Proposal acceptance path identical; tests. |
| TRN-REQ-AI-003 | §9 | TRN-ARCH-07 §4 | — | test: Prompt construction tests. |
| TRN-REQ-AI-004 | §9, §14 | TRN-ARCH-07 §4; TRN-SEC-01 T09 | — | test: No authority-widening diff accepted across the corpus. |
| TRN-REQ-AI-005 | §9 | TRN-ARCH-01 §7; TRN-ARCH-07 §3 | DF-TRN-2026-0012 | test: Replay determinism test; dependency scan of Engine finds no AI provider. |
| TRN-REQ-AI-006 | §9 | TRN-ARCH-07 §3 | — | test: Provenance present on accepted proposals. |
| TRN-REQ-AI-007 | §9, §14 | TRN-ARCH-07 §4; TRN-SEC-01 T23 | — | test: Classification-gated prompt builder tests. |
| TRN-REQ-AI-008 | §9, §19 | TRN-ARCH-07 §5 | — | review: Evaluation harness report. |
| TRN-REQ-MP-001 | §10 | TRN-ARCH-09 §1; schemas/mapping-package.schema.json | DF-TRN-2026-0014 | test: Package lint rejects code files and non-synthetic fixtures. |
| TRN-REQ-MP-002 | §10 | TRN-ARCH-09 §2 | DF-TRN-2026-0014 | review: Manifest basis required by schema; review checklist. |
| TRN-REQ-MP-003 | §10 | TRN-ARCH-09 §1 | — | test: Overlay touching undeclared path is rejected. |
| TRN-REQ-MP-004 | §10 | TRN-ARCH-09 §4; docs/research/03-daf-phase3-dispositions.md | DF-TRN-2026-0023 | test: Upgrade command produces deterministic output diff. |
| TRN-REQ-MP-005 | §10 | TRN-ARCH-09 §5 | — | review: Promotion checklist and synthetic fixture regeneration. |
| TRN-REQ-LN-001 | §13 | TRN-ARCH-08 §2 | DF-TRN-2026-0013 | test: Lineage query returns all elements for a loaded record. |
| TRN-REQ-LN-002 | §13 | TRN-ARCH-08 §1 | DF-TRN-2026-0013 | test: Static graph present; storage test shows no per-field value table. |
| TRN-REQ-LN-003 | §13 | TRN-ARCH-08 §3 | — | test: Evidence stage output validated against schema. |
| TRN-REQ-LN-004 | §13 | TRN-ARCH-08 §3 | — | test: Folio template renders a fixture package. |
| TRN-REQ-LN-005 | §13, §14 | TRN-SEC-01 T20 | — | test: Approval events verify. |
| TRN-REQ-LN-006 | §13, §14 | TRN-ARCH-08 §3 | — | test: Tampering fixture detected. |
| TRN-REQ-LN-007 | §13 | TRN-ARCH-08 §3; TRN-ARCH-11 §1 | DF-TRN-2026-0015 | test: Absent-safe integration test with and without Vigila. |
| TRN-REQ-LN-008 | §13, §14 | TRN-ARCH-08 §4 | — | test: Log-leak test suite. |
| TRN-REQ-LN-009 | §13 | TRN-ARCH-08 §3 | — | test: Export validates against OpenLineage spec. |
| TRN-REQ-SEC-001 | §14 | TRN-SEC-01 T01 | — | test: Fuzz corpus runs in CI. |
| TRN-REQ-SEC-002 | §14 | TRN-SEC-01 T02 | — | test: Zip-bomb fixtures rejected before allocation. |
| TRN-REQ-SEC-003 | §14 | TRN-SEC-01 T03 | — | test: XXE and billion-laughs fixtures rejected. |
| TRN-REQ-SEC-004 | §14 | TRN-SEC-01 T04 | — | test: Formula-injection fixtures. |
| TRN-REQ-SEC-005 | §14 | TRN-SEC-01 T05 | — | test: Zip-slip fixtures. |
| TRN-REQ-SEC-006 | §14 | TRN-SEC-01 T06 | — | test: Malformed corpus. |
| TRN-REQ-SEC-007 | §14 | TRN-SEC-01 T07 | — | test: Limit fixtures. |
| TRN-REQ-SEC-008 | §14 | TRN-SEC-01 T08 | — | test: Poisoning fixtures blocked by gates. |
| TRN-REQ-SEC-009 | §14 | TRN-SEC-01 T10 | — | test: Secret-leak scan. |
| TRN-REQ-SEC-010 | §14 | TRN-SEC-01 T11 | — | test: Publish authorization tests. |
| TRN-REQ-SEC-011 | §14 | TRN-SEC-01 T12 | — | test: Cross-tenant fixture rejected. |
| TRN-REQ-SEC-012 | §14 | TRN-SEC-01 T13 | — | test: Purge evidence. |
| TRN-REQ-SEC-013 | §14 | TRN-SEC-01 T15 | — | test: Unregistered destination rejected. |
| TRN-REQ-SEC-014 | §14 | TRN-SEC-01 T01 | — | test: Dependency scan. |
| TRN-REQ-SEC-015 | §14 | TRN-SEC-01 T16 | — | test: Egress test. |
| TRN-REQ-SEC-016 | §14 | TRN-SEC-01 T17 | — | test: Replay fixture zero effects. |
| TRN-REQ-SEC-017 | §14 | TRN-SEC-01 T19 | — | test: CI evidence. |
| TRN-REQ-SEC-018 | §14 | TRN-SEC-01 §4.10 | — | test: Retention tests. |
| TRN-REQ-SEC-019 | §14 | TRN-SEC-02 | — | test: Evidence generators listed in TRN-SEC-02 produce outputs. |
| TRN-REQ-UI-001 | §15, §16 | TRN-ARCH-10 §1 | DF-TRN-2026-0010 | review: Dependency review. |
| TRN-REQ-UI-002 | §15 | TRN-ARCH-10 §2 | DF-TRN-2026-0010 | test: Round-trip property test. |
| TRN-REQ-UI-003 | §15 | TRN-ARCH-10 §3 | — | test: View checklist. |
| TRN-REQ-UI-004 | §15 | TRN-ARCH-10 §4 | — | test: Accessibility audit. |
| TRN-REQ-UI-010 | §15 | TRN-ARCH-10 §5 | — | test: OpenAPI coverage check. |
| TRN-REQ-ARC-001 | §16 | TRN-ARCH-11 §2 | DF-TRN-2026-0015 | review: Repository contains no deployable service project. |
| TRN-REQ-ARC-002 | §2, §16 | TRN-ARCH-11 §1 | DF-TRN-2026-0001 | review: Dependency analysis kept current. |
| TRN-REQ-ARC-003 | §16 | TRN-ARCH-04 §6 | — | test: CI coverage of all packages. |
| TRN-REQ-ARC-004 | §16 | TRN-ARCH-02 | DF-TRN-2026-0008 | review: Dependency review. |
| TRN-REQ-ARC-005 | §16 | TRN-ARCH-03 §4 | — | review: Decision records exist for each dependency. |
| TRN-REQ-PF-001 | §18 | TRN-ARCH-12 §1 | — | review: Benchmark report per assumption A1-A11. |
| TRN-REQ-PF-002 | §18 | TRN-ARCH-12 §3 | — | test: Load test with concurrent OLTP workload. |
| TRN-REQ-ARC-006 | §2 | TRN-ARCH-11 §1; TRN-REV-01 C1 | DF-TRN-2026-0001 | review: Duplication review per phase; Unbound.Replay consumes Transitus.Formats or the parsers move. |
| TRN-REQ-ARC-007 | §19 | docs/roadmap.md; TRN-REV-01 C11 | DF-TRN-2026-0016 | review: Package count check in CI. |
| TRN-REQ-ARC-008 | §19, §21 | docs/roadmap.md; TRN-REV-01 C12 | DF-TRN-2026-0016 | review: Traceability table in roadmap. |
| TRN-REQ-ARC-009 | §19 | docs/roadmap.md; docs/research/03-daf-phase3-dispositions.md | DF-TRN-2026-0016, DF-TRN-2026-0022, DF-TRN-2026-0023 | review: Decision record per phase gate. |
| TRN-REQ-EX-013 | §11, §14 | TRN-ARCH-05 §2; TRN-REV-01 C8 | — | test: Payload classification test. |
| TRN-REQ-AD-011 | §11 | TRN-ARCH-05 §5; TRN-REV-01 C9 | — | test: Load test: interactive command latency within budget during a bulk load. |
| TRN-REQ-AD-012 | §11, §21 | TRN-ARCH-12 §3; TRN-REV-01 C9 | — | test: Unbound operation contract review (UNB-TRN-006). |
| TRN-REQ-MP-006 | §10 | TRN-ARCH-09 §3; TRN-REV-01 C7 | — | review: Roadmap ordering. |
| TRN-REQ-MP-007 | §10, §19 | TRN-REV-01 C7 | — | test: Reuse metric per migration. |
| TRN-REQ-LN-010 | §13 | TRN-ARCH-08; TRN-REV-01 C8 | — | test: Retention configuration test. |
| TRN-REQ-PF-003 | §18 | TRN-ARCH-12 §2 | — | review: Storage model revised and later measured. |
| TRN-REQ-PF-004 | §18, §19 | TRN-ARCH-12 §6; TRN-REV-01 C2 | DF-TRN-2026-0016 | review: Comparison in phase-1 exit review. |
| TRN-REQ-UI-011 | §15 | TRN-ARCH-10; TRN-REV-01 C10 | — | test: Integration via library callback. |
| TRN-REQ-TX-011 | §6, §7 | TRN-ARCH-04 §3.6; TRN-REV-01 C4 | DF-TRN-2026-0004 | test: Counter-example fixtures from TRN-REV-01 C4 (U1, U9, U10, H1, H2) are expressible. |
| TRN-REQ-EXT-001 | §6 | TRN-ARCH-04 §5 | DF-TRN-2026-0005 | test: Allow-list and signature checks. |
| TRN-REQ-EXT-002 | §6 | TRN-ARCH-04 §6 | — | test: Conformance report and review record. |
| TRN-REQ-EXT-003 | §6 | TRN-REV-01 C4 | — | test: Extension register. |
| TRN-REQ-EXT-004 | §6, §9 | TRN-ARCH-01 §7 | — | test: Manifest includes extension hashes. |
| TRN-REQ-AI-009 | §9 | TRN-ARCH-07 §5; TRN-REV-01 C6 | — | test: Gate configuration test. |
| TRN-REQ-ST-009 | §5, §11 | TRN-ARCH-12 §2; TRN-REV-01 C5 | — | test: Documented and tested crash recovery. |
| TRN-REQ-ST-010 | §5 | TRN-REV-01 C5 | — | test: Storage model shows single copy. |
| TRN-REQ-PS-011 | §4, §6 | TRN-ARCH-01 §2; schemas/pipeline-phase1.schema.json | DF-TRN-2026-0018 | test: The three demonstration pipelines in examples/pipelines validate against schemas/pipeline-phase1.schema.json. |
| TRN-REQ-EX-014 | §9, §11 | TRN-ARCH-05 §4 | DF-TRN-2026-0018 | test: Replay fixture: byte-identical staged output hashes; zero additional destination effects. |
| TRN-REQ-VR-013 | §12, §14 | TRN-ARCH-06 §4; TRN-SEC-01 T12 | DF-TRN-2026-0018 | test: Validator rejects a financial system-of-record pipeline with advisory-only gates; cross-tenant reference rejected. |
| TRN-REQ-MP-008 | §10 | TRN-ARCH-09 §2 | DF-TRN-2026-0019 | review: Rights verification record per package. |
| TRN-REQ-ARC-010 | §2, §16 | TRN-ARCH-11 §1 | DF-TRN-2026-0021 | review: Boundary review at phase-1 exit. |
| TRN-REQ-AI-010 | §9, §14 | TRN-ARCH-07 §6 | DF-TRN-2026-0021 | test: Provider authorization check per request. |
| TRN-REQ-MP-009 | §10, §17 | TRN-RES-02; examples/ | DF-TRN-2026-0018, DF-TRN-2026-0019 | test: Worked examples in examples/ validate; rehearsal evidence package specified. |
| TRN-REQ-PS-012 | §6 | TRN-ARCH-01 §5; TRN-REV-02 | DF-TRN-2026-0018 | test: Validator rejects any predicate outside the vocabulary; the three demonstration pipelines need nothing more. |
| TRN-REQ-ARC-011 | §11, §16 | TRN-ARCH-05 §2; TRN-REV-02 | DF-TRN-2026-0021 | review: Dependency scan of Transitus packages finds no Echelon.Execution reference; a fake port drives the engine tests. |
| TRN-REQ-SEC-020 | §14 | TRN-SEC-01 T12; TRN-REV-02 | — | test: Cross-tenant access attempts fail in every listed store. |
| TRN-REQ-MIG-001 | §10, §17 | examples/pipelines/migration-rehearsal.pipeline.json; TRN-REV-02; docs/research/03-daf-phase3-dispositions.md | DF-TRN-2026-0018, DF-TRN-2026-0025 | test: Rehearsal evidence package; repeat run yields identical keys and outputs; live schema untouched. |
| TRN-REQ-MIG-002 | §10 | TRN-ARCH-09 | — | test: Validation rule fails any record lacking the stamps. |
| TRN-REQ-MIG-003 | §12, §21 | TRN-REV-02 | — | test: Load refused with fence Unknown; MigrationRun transitions only via Unbound. |
| TRN-REQ-MIG-004 | §10, §21 | TRN-REV-02 | — | test: Document hash equality between raw evidence and destination read-back. |
| TRN-REQ-OBS-001 | §13 | TRN-ARCH-08 §3; TRN-REV-02 | — | test: Telemetry present in host traces and metrics. |
| TRN-REQ-PF-005 | §18 | TRN-ARCH-12; TRN-REV-02 | — | review: Benchmark report. |
| TRN-REQ-PRF-001 | §4, §12 | TRN-ARCH-01 §2 (profile); docs/research/03-daf-phase3-dispositions.md | DF-TRN-2026-0022 | test: Given a policy with minimum contributor count k and a grouping with fewer than k contributors, When the profile stage runs, Then that cell is emitted as suppressed with its reason and no value. Given a monetary cell in which one contributor exceeds the declared dominance share, When the profile runs, Then the cell is suppressed. Given identical input and policy, When the profile runs twice, Then the profile document hashes are identical. |
| TRN-REQ-PRF-002 | §8 | TRN-ARCH-03 §1; docs/research/03-daf-phase3-dispositions.md | DF-TRN-2026-0022 | test: Given a file whose fingerprint matches two package detectors, When discovery runs, Then both candidates and their scores are reported and no pipeline is selected. Given the same bytes, When discovery runs twice, Then the inferred-schema hashes are identical. Given a file matching no detector, Then the result is 'no candidate' with the inferred schema. |
| TRN-REQ-PRF-003 | §9, §10 | TRN-ARCH-07 §1; docs/research/03-daf-phase3-dispositions.md | DF-TRN-2026-0022 | test: Given a source field whose name matches a target alias and whose profiled values match the target type, When the suggester runs, Then a proposed PipelineDiff naming the rule is emitted. Given an unaccepted suggestion, When a rehearsal is started, Then the suggestion is not part of the executed mapping version. |
| TRN-REQ-VR-014 | §12, §13 | TRN-ARCH-06 §3; docs/research/03-daf-phase3-dispositions.md | DF-TRN-2026-0011, DF-TRN-2026-0025 | test: Given a profile that declares a sampled check on a money field, When it is published, Then validation rejects it. Given the same seed and data, When sampling runs twice, Then the same records are selected. Given one deviation in a stratum whose declared tolerable deviation count is zero, When the gate runs, Then it fails and the deviation is itemized with source, canonical and read-back values classified per TRN-REQ-LN-008. |
| TRN-REQ-MIG-005 | §10, §12 | TRN-ARCH-06; docs/research/03-daf-phase3-dispositions.md | DF-TRN-2026-0011 | test: Given a mapping that swaps two restriction codes between equal-amount records, When the harness runs, Then the round-trip totals pass, an invariant or mutation check fails, and the evidence names the detecting check. Given an unchanged mapping and dataset, When the harness runs twice, Then results are identical. |
| TRN-REQ-MIG-006 | §7, §10 | TRN-ARCH-04 §1; docs/research/03-daf-phase3-dispositions.md | DF-TRN-2026-0022 | test: Given a legacy grant without a payment date and a contract declaring NotProvidedBySource, When transformed, Then the field carries NotProvidedBySource and the source-row hash link. Given a pipeline applying field.default to that field, When published, Then validation rejects it. |
| TRN-REQ-MIG-007 | §11, §13 | TRN-ARCH-05 §6-§8; docs/research/03-daf-phase3-dispositions.md | DF-TRN-2026-0007 | test: Given a load whose third item ends OutcomeUnknown, When the effects manifest is produced, Then every attempted item appears with its outcome and the unknown item is flagged for host resolution. Given cancellation before the first load intent, When the execution ends, Then the manifest is empty and staging purge evidence exists. |
| TRN-REQ-MP-010 | §10 | TRN-ARCH-09 §3; docs/research/03-daf-phase3-dispositions.md; Unbound requirements/discovery/2026-11-26-competitive-displacement-decisions (UNB-CDD-ONB-002) | DF-TRN-2026-0023, DF-TRN-2026-0019 | review: Given no consumer selection record (Unbound UNB-CDD-ONB-002) naming source A, When a vendor-specific package for A is proposed for publication, Then publication is refused. Given a recorded selection naming source A, When a package for source B is proposed, Then publication is refused until a further consumer record names B. Given a package for A, When it is published, Then its manifest cites the selection record identifier and version. |
| TRN-REQ-MET-001 | §13, §18 | docs/research/03-daf-phase3-dispositions.md | DF-TRN-2026-0024 | test: Given a rehearsal for which the host supplies no go-live time, When evidence is produced, Then the go-live fact is 'unavailable', not zero. Given two rehearsals of the same source, When the second completes, Then its evidence contains the control-total delta against the first. |
| TRN-REQ-MET-002 | §18, §19 | docs/research/03-daf-phase3-dispositions.md | DF-TRN-2026-0024 | review: Given two measured migrations and a metric whose minimum sample is three, When the level is computed, Then it reads 'not evidenced'. Given no recorded DEC-010 gate, When an external report is generated, Then maturity levels are omitted. |
| TRN-REQ-MET-003 | §12, §18 | docs/research/03-daf-phase3-dispositions.md | DF-TRN-2026-0024 | test: Given an extract without its declared control file, When conformance runs, Then it is non-conforming with reasons and no clock start is recorded. Given a conforming extract, When conformance runs, Then the clock start equals the determination time and a validation summary is produced for approval. |
| TRN-REQ-ASM-001 | §14, §17 | docs/research/03-daf-phase3-dispositions.md; daf-landscape competitive-displacement 08 §3 | DF-TRN-2026-0022 | review: Given a T1 engagement, When a record-level file is submitted, Then it is rejected before persistence and the rejection is recorded. Given a T2 request without MSA and DPA references, When it is started, Then the execution does not start. Given an engagement at T2, When a T1 run is requested, Then it is refused as non-monotonic. |
| TRN-REQ-ASM-002 | §10, §17 | docs/research/03-daf-phase3-dispositions.md | DF-TRN-2026-0022 | review: Given a completed template that omits history years for grants, When it is validated, Then the report lists grant history depth as 'not provided' and names the tier that would resolve it. Given the same template twice, Then identical output. |
| TRN-REQ-ASM-003 | §14, §17 | docs/research/03-daf-phase3-dispositions.md; daf-landscape charity-network-and-onboarding 13 §2 | DF-TRN-2026-0022 | review: Given a book below the minimum population, When the profiler runs, Then it emits schema and coverage only and no aggregates. Given an output cell matching an email or SSN pattern, When emission is attempted, Then it is refused and the reason recorded locally. Given network egress disabled, When the profiler runs, Then it completes. |
| TRN-REQ-ASM-004 | §5, §14 | docs/research/03-daf-phase3-dispositions.md | DF-TRN-2026-0022 | review: Given a T2 assessment, When it completes, Then zero destination effects are recorded. Given the retention deadline passes, When the sweeper runs, Then raw and staged assessment data are purged and purge evidence is produced. |
| TRN-REQ-ASM-005 | §10, §17 | docs/research/03-daf-phase3-dispositions.md | DF-TRN-2026-0022, DF-TRN-2026-0025 | test: Given a synthetic run, When the assessment report is rendered, Then the data-quality, effort and timeline sections read 'not assessable from synthetic data' and the report is marked conformance-only. |
| TRN-REQ-ASM-006 | §13, §17 | docs/research/03-daf-phase3-dispositions.md; daf-landscape charity-network-and-onboarding 13 §6-§7 | DF-TRN-2026-0022, DF-TRN-2026-0024 | review: Given a T1-only engagement, When the report is produced, Then record-level matching reads 'not assessable at T1; resolved by T2+'. Given identical inputs twice, Then identical report hashes. Given any report, Then the effort section contains no currency figure and every assumption is labelled. |
| TRN-REQ-ASM-007 | §10 | docs/research/03-daf-phase3-dispositions.md | DF-TRN-2026-0022 | test: Given a mapping element derived from a vendor screenshot description, When the report is rendered, Then the element is flagged vendor-assumption-unverified and excluded from evidenced totals. |
| TRN-REQ-ASM-008 | §10 | docs/research/03-daf-phase3-dispositions.md | DF-TRN-2026-0022 | test: Given a fixture without a synthetic mark, When package lint runs, Then it fails. Given no customer-authorized sample for a source, When a package for that source is linted, Then its basis is synthetic-representation or public-specification only. |

## Charter coverage

| Charter § | Requirements |
|---|---|
| §2 | 3: TRN-REQ-ARC-002, TRN-REQ-ARC-006, TRN-REQ-ARC-010 |
| §4 | 5: TRN-REQ-PS-002, TRN-REQ-PS-003, TRN-REQ-PS-005, TRN-REQ-PS-011, TRN-REQ-PRF-001 |
| §5 | 12: TRN-REQ-ST-001, TRN-REQ-ST-002, TRN-REQ-ST-003, TRN-REQ-ST-004, TRN-REQ-ST-005, TRN-REQ-ST-006, TRN-REQ-ST-007, TRN-REQ-ST-008, TRN-REQ-AD-008, TRN-REQ-ST-009, TRN-REQ-ST-010, TRN-REQ-ASM-004 |
| §6 | 12: TRN-REQ-PS-001, TRN-REQ-PS-006, TRN-REQ-PS-007, TRN-REQ-PS-009, TRN-REQ-PS-010, TRN-REQ-TX-011, TRN-REQ-EXT-001, TRN-REQ-EXT-002, TRN-REQ-EXT-003, TRN-REQ-EXT-004, TRN-REQ-PS-011, TRN-REQ-PS-012 |
| §7 | 12: TRN-REQ-TX-001, TRN-REQ-TX-002, TRN-REQ-TX-003, TRN-REQ-TX-004, TRN-REQ-TX-005, TRN-REQ-TX-006, TRN-REQ-TX-007, TRN-REQ-TX-008, TRN-REQ-TX-009, TRN-REQ-TX-010, TRN-REQ-TX-011, TRN-REQ-MIG-006 |
| §8 | 10: TRN-REQ-AD-001, TRN-REQ-AD-002, TRN-REQ-AD-003, TRN-REQ-AD-004, TRN-REQ-AD-005, TRN-REQ-AD-006, TRN-REQ-AD-007, TRN-REQ-AD-009, TRN-REQ-AD-010, TRN-REQ-PRF-002 |
| §9 | 15: TRN-REQ-PS-008, TRN-REQ-TX-007, TRN-REQ-AI-001, TRN-REQ-AI-002, TRN-REQ-AI-003, TRN-REQ-AI-004, TRN-REQ-AI-005, TRN-REQ-AI-006, TRN-REQ-AI-007, TRN-REQ-AI-008, TRN-REQ-EXT-004, TRN-REQ-AI-009, TRN-REQ-EX-014, TRN-REQ-AI-010, TRN-REQ-PRF-003 |
| §10 | 20: TRN-REQ-MP-001, TRN-REQ-MP-002, TRN-REQ-MP-003, TRN-REQ-MP-004, TRN-REQ-MP-005, TRN-REQ-MP-006, TRN-REQ-MP-007, TRN-REQ-MP-008, TRN-REQ-MP-009, TRN-REQ-MIG-001, TRN-REQ-MIG-002, TRN-REQ-MIG-004, TRN-REQ-PRF-003, TRN-REQ-MIG-005, TRN-REQ-MIG-006, TRN-REQ-MP-010, TRN-REQ-ASM-002, TRN-REQ-ASM-005, TRN-REQ-ASM-007, TRN-REQ-ASM-008 |
| §11 | 22: TRN-REQ-AD-004, TRN-REQ-AD-007, TRN-REQ-EX-001, TRN-REQ-EX-002, TRN-REQ-EX-003, TRN-REQ-EX-004, TRN-REQ-EX-005, TRN-REQ-EX-006, TRN-REQ-EX-007, TRN-REQ-EX-008, TRN-REQ-EX-009, TRN-REQ-EX-010, TRN-REQ-EX-011, TRN-REQ-EX-012, TRN-REQ-VR-010, TRN-REQ-EX-013, TRN-REQ-AD-011, TRN-REQ-AD-012, TRN-REQ-ST-009, TRN-REQ-EX-014, TRN-REQ-ARC-011, TRN-REQ-MIG-007 |
| §12 | 21: TRN-REQ-PS-003, TRN-REQ-TX-005, TRN-REQ-EX-009, TRN-REQ-VR-001, TRN-REQ-VR-002, TRN-REQ-VR-003, TRN-REQ-VR-004, TRN-REQ-VR-005, TRN-REQ-VR-006, TRN-REQ-VR-007, TRN-REQ-VR-008, TRN-REQ-VR-009, TRN-REQ-VR-010, TRN-REQ-VR-011, TRN-REQ-VR-012, TRN-REQ-VR-013, TRN-REQ-MIG-003, TRN-REQ-PRF-001, TRN-REQ-VR-014, TRN-REQ-MIG-005, TRN-REQ-MET-003 |
| §13 | 15: TRN-REQ-LN-001, TRN-REQ-LN-002, TRN-REQ-LN-003, TRN-REQ-LN-004, TRN-REQ-LN-005, TRN-REQ-LN-006, TRN-REQ-LN-007, TRN-REQ-LN-008, TRN-REQ-LN-009, TRN-REQ-LN-010, TRN-REQ-OBS-001, TRN-REQ-VR-014, TRN-REQ-MIG-007, TRN-REQ-MET-001, TRN-REQ-ASM-006 |
| §14 | 38: TRN-REQ-PS-004, TRN-REQ-PS-008, TRN-REQ-ST-002, TRN-REQ-TX-010, TRN-REQ-AD-008, TRN-REQ-EX-006, TRN-REQ-EX-010, TRN-REQ-AI-004, TRN-REQ-AI-007, TRN-REQ-LN-005, TRN-REQ-LN-006, TRN-REQ-LN-008, TRN-REQ-SEC-001, TRN-REQ-SEC-002, TRN-REQ-SEC-003, TRN-REQ-SEC-004, TRN-REQ-SEC-005, TRN-REQ-SEC-006, TRN-REQ-SEC-007, TRN-REQ-SEC-008, TRN-REQ-SEC-009, TRN-REQ-SEC-010, TRN-REQ-SEC-011, TRN-REQ-SEC-012, TRN-REQ-SEC-013, TRN-REQ-SEC-014, TRN-REQ-SEC-015, TRN-REQ-SEC-016, TRN-REQ-SEC-017, TRN-REQ-SEC-018, TRN-REQ-SEC-019, TRN-REQ-EX-013, TRN-REQ-VR-013, TRN-REQ-AI-010, TRN-REQ-SEC-020, TRN-REQ-ASM-001, TRN-REQ-ASM-003, TRN-REQ-ASM-004 |
| §15 | 6: TRN-REQ-UI-001, TRN-REQ-UI-002, TRN-REQ-UI-003, TRN-REQ-UI-004, TRN-REQ-UI-010, TRN-REQ-UI-011 |
| §16 | 10: TRN-REQ-ST-007, TRN-REQ-EX-001, TRN-REQ-UI-001, TRN-REQ-ARC-001, TRN-REQ-ARC-002, TRN-REQ-ARC-003, TRN-REQ-ARC-004, TRN-REQ-ARC-005, TRN-REQ-ARC-010, TRN-REQ-ARC-011 |
| §17 | 7: TRN-REQ-MP-009, TRN-REQ-MIG-001, TRN-REQ-ASM-001, TRN-REQ-ASM-002, TRN-REQ-ASM-003, TRN-REQ-ASM-005, TRN-REQ-ASM-006 |
| §18 | 9: TRN-REQ-ST-008, TRN-REQ-PF-001, TRN-REQ-PF-002, TRN-REQ-PF-003, TRN-REQ-PF-004, TRN-REQ-PF-005, TRN-REQ-MET-001, TRN-REQ-MET-002, TRN-REQ-MET-003 |
| §19 | 7: TRN-REQ-AI-008, TRN-REQ-ARC-007, TRN-REQ-ARC-008, TRN-REQ-ARC-009, TRN-REQ-MP-007, TRN-REQ-PF-004, TRN-REQ-MET-002 |
| §21 | 5: TRN-REQ-VR-006, TRN-REQ-ARC-008, TRN-REQ-AD-012, TRN-REQ-MIG-003, TRN-REQ-MIG-004 |
