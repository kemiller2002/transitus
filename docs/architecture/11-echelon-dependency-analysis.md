---
id: TRN-ARCH-11
title: Echelon Dependency and Overlap Analysis
status: proposed
version: 0.1.0
created: 2026-11-26
updated: 2026-11-26
work_item: WI-0001
reviewed_commits: "main branches as cloned 2026-11-26 (shallow)"
decisions: [DF-TRN-2026-0001, DF-TRN-2026-0006, DF-TRN-2026-0015]
---

# Echelon dependency and overlap analysis

Method: every repository named in the charter plus all public Echelon
component repositories listed in `echelon-registry/registry/systems-v2.json`
and `portfolio/repositories.json` were cloned from `main` on 2026-11-26 and
searched for overlapping capability. `grep -ri transitus` across all of them
returned no matches: Transitus is not yet registered, planned or referenced.

## 1. Capability-by-capability ownership

| Capability Transitus needs | Existing owner | Evidence (repo path) | Transitus stance |
|---|---|---|---|
| Durable job queue, leases, retries, idempotency, outbox, approval wait, OutcomeUnknown, per-tenant fairness | **Echelon.Execution** (incubating in Unbound, INIT-012 RM-07) | `unbound/execution/README.md`, `src/Echelon.Execution/Types.fs` | **Consume.** Do not build. Transitus is the "second consumer" that the README names as the extraction trigger. |
| PostgreSQL schema governance (DDL for staging/lineage tables) | **Strata** | `strata/README.md` | **Consume** for DDL. Strata does *not* provide queues, staging or temp-table runtime; those are Transitus/Echelon.Execution runtime concerns. |
| External-interaction contracts, live/mock/replay, virtual clock (proposed) | **Strata DIV proposal** (STRATA-DIV-001, not accepted) | `strata/docs/requirements/data-interaction-virtualization.md`; registry DRF-03 | **Boundary to agree.** DIV virtualizes the *application's* external calls for testing; Transitus *ingests data from* external systems. Proposed boundary: Transitus adapters may run under DIV replay in tests; neither owns the other's contracts (OQ-02). |
| Pipeline graph editor / runtime visualization | **Forma** portable workflow | `forma/docs/decisions/ADR-0006-portable-workflow-capability.md`, `forma/src/workflow/Forma.Workflow/` | **Consume.** Raise gaps as Forma requirements. |
| UI components, design system | **Forma** | `forma/README.md` | Consume. |
| Browser/application authority boundary | **Limen** | `limen/README.md` | Consume (admin UI only). Limen is not a server host or plugin runtime; Transitus's "runtime" is the host application. |
| Typed routing | **Iter** | `iter/README.md` | Consume (admin UI). |
| Printable evidence/reports | **Folio** | `folio/README.md`; registry GAP-06 | Consume for rendering evidence reports. |
| Follow-up tasks for humans | **Vigila** (task/follow-up tracker) | `vigila/README.md` ("Task organizer"), capabilities `followup.*` | Optional consumer: raise follow-ups for exceptions/OutcomeUnknown. **Charter assumption corrected:** Vigila is not an observability platform. |
| Operational observability / runtime monitoring | **Unowned** (registry GAP-05) | `echelon-registry/portfolio/analysis/responsibility-and-capability-matrix.md` | Emit OpenTelemetry through the host; do **not** create a monitoring product. Escalated as OQ-03. |
| Tamper-evident evidence storage, auditor export | **Unowned** (GAP-06, GAP-07) | same | Transitus hash-chains *its own* evidence; a portfolio-wide evidence store is out of scope (OQ-03). |
| Operational fault capture, redaction, recovery | **Aegis** | `aegis/README.md`; Praxis SAF Aegis 1–6 | Consume for unexpected faults; expected validation outcomes stay typed `Result`s. |
| Identity / SSO | **Fides** | `fides/README.md` | Host-provided; Transitus receives principal ids. |
| Security discipline / posture gate | **Tutela** | `tutela/README.md` | Apply its threat/control method; Transitus threat model feeds Tutela posture gate. |
| State-machine legality method | **Ordo** | `ordo/` | Apply method to execution state machine. |
| Code quality evidence | **Dokimos** | `dokimos/README.md` | Consume in CI (phase 2). |
| Repository bootstrap & pinned component install | **Conditor** | `conditor/README.md` | Transitus distributed as pinned NuGet packages installable via Conditor catalogue. Conditor is not application deployment. |
| Governance, work protocol | **Praxis** | `praxis/AGENTS.md` | Followed (this repository runs Praxis 3.26.0). |
| Authoritative record storage in Git (browser WASM) | **Arca** | `arca/docs/requirements/ARCA-STORAGE-REQUIREMENTS.md` | Not used for raw/staging data: ARCA-REC-007 forbids large binary artifacts. Arca-backed apps may be *destinations* via their domain APIs. |
| Ledger self-reconciliation, financial migration | **Summa** (domain-specific) | `summa/src/Summa.Storage/Reconciliation.fs`, `src/Summa.Operations/FinancialMigration.fs` | Not duplicated: Summa's reconciliation is ledger-internal. Transitus provides generic primitives; Summa could become a destination/consumer. |
| Raw source file preservation / object storage | **Unowned** | Arca excludes; no other owner | Transitus defines `IBlobStore` port (OQ-04). |
| Secrets management | **Unowned** (Tutela scans for secrets; Fides handles GitHub tokens) | registry matrix | Host-provided `ISecretProvider` port. |
| Scheduling / clock primitives | Chrona planned "canonical time primitives" (not implemented); Chrona is time recording, not a scheduler | `registry/systems-v2.json` plannedCapabilities | Inject `IClock`; adopt Chrona.Time when it exists. Scheduling uses Echelon.Execution `ScheduledCommand`. |
| Document extraction (OCR) | None (Percepta is semantic UI contracts) | `percepta/` | Out of Transitus scope; Helix Note has its own file extraction (`helix-note-application/api/HelixNote.Data.FileExtraction.fs`). |
| IRS/OFAC file parsing (prior art) | **Unbound replay tooling** | `unbound/requirements/convergence/2026-11-24-master/replay/src/Unbound.Replay/Sources.fs` | Reuse parsing knowledge in `irs.*` packages; replay tool stays Unbound's. |
| Charity knowledge acquisition model (SourceRegistry → AcquisitionRun → RawEvidence → ObservedClaim → VerifiedFact) | **Unbound** (domain) | `unbound/architecture/CHARITY-KNOWLEDGE-MODEL-AND-ACQUISITION-PIPELINE.md` (UNB-KNOW-023/027) | Transitus implements the generic *AcquisitionRun → RawEvidence* half; claims/verified facts stay in Unbound's domain. |
| Migration run state machine (Contracted … Archived) | **Unbound** (domain) | RR-REQ-X-061-r1 | Transitus executions are steps *inside* a MigrationRun; the run's cutover/fencing remain Unbound's. |

**Review correction (TRN-REV-01 C1).** Unbound already designs `SourceRegistry → AcquisitionRun → RawEvidence`, and its replay tooling already parses the IRS files. Transitus phase 1 therefore *adopts* that model and *moves* those parsers into `Transitus.Formats`; it does not build parallel versions (TRN-REQ-ARC-006). Summa and Helix Note have their own migration and extraction code, so they are **candidate** consumers, not committed ones.

**Conclusion:** after removing what is owned elsewhere, Transitus's unique
responsibility is: *the declarative pipeline model, the transformation and
validation/reconciliation primitive libraries, the adapter contracts and a
small standard adapter set, raw/staging/lineage management, and the
pipeline-level execution state machine on top of Echelon.Execution.*
No existing Echelon component provides these (DF-TRN-2026-0001).

## 2. Library boundaries (revised after TRN-REV-01)

The original proposal had eleven code packages; its text miscounted them as
eight. Review found that excessive for a single-owner portfolio (C11) and
ahead of demand (C12). The revised boundaries are below.

### Phase 1 (owner-directed, DF-TRN-2026-0018): minimal declarative pipeline

The owner superseded the three-library phase 1 (DF-TRN-2026-0016). Phase 1 delivers a minimal declarative typed linear pipeline built on the three pure libraries. The maintenance budget is set by TRN-REQ-ARC-007 (revised per TRN-REV-02): at most 7 code packages (a 5-package variant is acceptable), 2 third-party parser libraries, 5 basic mapping packages, 13 operations, and 2 cross-repository ports.

| Package | Phase-1 contents | Depends on |
|---|---|---|
| `Transitus.Model` | DU model for the phase-1 profile; canonical JSON (JCS) codec; publish-time definition validator (types, linearity, closed vocabulary, policy, authority-and-semantics diff); package manifest loader | none |
| `Transitus.Transforms` | The 13 phase-1 operations (TRN-REQ-TX-009) | Model |
| `Transitus.Formats` | Strict parsers with limits. Port of `Unbound.Replay/Sources.fs` (IRS, OFAC); CSV, fixed-width/NACHA, first bank format, Schwab format once documented, read-only XLSX | BCL + at most 2 vetted parser libraries |
| `Transitus.Checks` | Validation and reconciliation primitives; conservation law | Model |
| `Transitus.Evidence` | RawEvidence aligned to UNB-KNOW-023; idempotency keys; L0–L2 lineage; evidence package with hash chain | Model |
| `Transitus.Engine` | Linear stage executor behind two host-implemented ports, durable commands and domain destination (TRN-REQ-ARC-011), so Echelon.Execution is used in place and never referenced. Provides stage checkpoints, replay, dry run, OutcomeUnknown handling, quota share | Model, Transforms, Formats, Checks, Evidence |
| `Transitus.Storage.Postgres` | Raw metadata, tenant-schema staging, lineage and evidence stores; DDL as Strata-governed SQL | Engine, Npgsql |
| Basic mapping packages | `irs.eo-bmf`, `nacha.ach` (rights pending), first bank format (illustrated by `iso20022.camt053`), `custodian.schwab` (placeholder), `unbound.canonical-history` | configuration only |

### Later phases (each gated by a recorded trigger, TRN-REQ-ARC-009)

| Phase | Adds | Trigger |
|---|---|---|
| 2 | Complex DAGs (routes, unions, joins), bounded set operators (TX-011), governed extensions (EXT-*), Folio evidence reports; extraction of Echelon.Execution once its shared contract is stable | **T2:** a demonstrated scenario the linear model cannot express |
| 3 | `Transitus.Assist` (advanced AI, provider-independent), vendor-specific turnkey packages | **T3:** AI evaluation thresholds met; customer-authorized sample and licence clearance for vendor packages |
| 4 | `Transitus.Admin` (Forma/Limen visual editing) | **T4:** operators other than engineers must configure pipelines |

## 3. Proposed requirements on other components (not applied here)

These are recorded for the owning repositories per governance; Transitus
does **not** change their responsibilities.

| ID | Target | Proposal | Filed where |
|---|---|---|---|
| DEP-EXEC-01 | Echelon.Execution (Unbound) | Extraction deferred **until the shared contract is stable** (owner resolution of OQ-01); Transitus phase 1 uses it in place. Before Transitus relies on it, the module needs: Transitus needs G1 lease renewal, G2 dependency resume, G3 payload protection/purge, G4 metrics | `unbound/requirements/discovery/2026-11-26-transitus-integration/` (this initiative) |
| DEP-STRATA-01 | Strata | Accept schema fragments contributed by an embedded library (staging/lineage DDL) under the host's governed migration path | recorded here; to be raised in Strata by its owner (read-only from this session) |
| DEP-STRATA-02 | Strata DIV | Agree boundary between DIV interaction virtualization and Transitus source adapters | registry INIT-018 boundary review |
| DEP-FORMA-01 | Forma workflow | Partition-routing node with mandatory `otherwise`; layout-as-annotation; mapping-table pattern with non-drag alternative | recorded here |
| DEP-FOLIO-01 | Folio | Evidence package → printable report template | recorded here |
| DEP-VIGILA-01 | Vigila | None required; optional `followup.create` consumer. Observability gap (GAP-05) needs a portfolio owner decision | registry |
| DEP-REG-01 | Echelon Registry | Register Transitus repository (requirements maturity, no `provides` until implemented) | `echelon-registry/portfolio/repositories.json` (this initiative) |

## 4. Licensing note

The charter directs "MIT licensing for public repository content". The
registry records that component repositories currently use PolyForm
Noncommercial 1.0.0, with the portfolio licence decision open (registry
DRF-09, OD-GOV-018). Following the explicit instruction, Transitus documents
are MIT-licensed; the conflict with the portfolio-wide decision is escalated
as OQ-12 rather than resolved silently.
