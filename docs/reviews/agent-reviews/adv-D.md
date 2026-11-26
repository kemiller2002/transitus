# Adversarial review D: Transitus claims C10, C11, C12

Reviewer stance: architecture and business strategy, trying to refute. Date 2026-11-26. All evidence is read-only from the repositories named. Line numbers refer to files as they were on that date.

## Evidence baseline: what Unbound release 1 actually is

The verdicts below rest on four facts about the first consumer.

1. **Unbound has no application yet.** The only F# code in `unbound` is the `execution/` slice (2,558 lines; the README says "first implementation slice … not benchmarked … not deployed anywhere"), the replay tool under `requirements/convergence/2026-11-24-master/replay/`, and requirements tooling (`tools/fs`). There is no domain API, no OpenAPI and no ledger. `10-MISSION-REPORT-AND-READINESS.md:23,70,239` records **"FAIL for production implementation"**. Registry INIT-005 is still `research`, and its success criteria are "Formal requirements review gate passed" and "Open decisions reduced".
2. **Release 1 has no institutional migration.** `requirements/discovery/2026-11-23-cross-industry/17-RELEASE-1-SCOPE.md:16,108` gives release 1 as one legal sponsor ("the Unbound reference sponsor") and one custodian, and says "no migration in R1" (UNB-XIN-OTH-002). The simplification matrix `discovery/2026-11-24-simplification-economics/02-REQUIREMENT-SIMPLIFICATION-MATRIX.md:1731,1750,1796` defers RR-REQ-X-061-r1, UNB-RCN-WF-020 and UNB-XIN-OTH-002 with "No migration in R1". Lines 480 and 493 do the same for custodian migration (UNB-CUST-023, UNB-INV-008). The recommended build sequence in `10-MISSION-REPORT…md:206-217` never mentions migration.
   - **Counter-evidence:** CNV-EXP-002 (baseline.jsonl, `release_scope: initial-implementation`, owner-ratified, `AUTHORITATIVE-BASELINE.md:98`) requires a sponsor migration that imports "each donor's full fund history … with a reconciliation report". OD-M-14 (owner-decisions.jsonl line 22) says "No design-partner sponsor will be available". The first paying sponsor's contract carries a 12-month shadow replay. Unbound's own records therefore conflict. The most a reader can conclude is that a *single* predecessor-platform import may be needed around the first paying sponsor. It is not needed for the release-1 reference sponsor.
3. **What release 1 does need is recurring feed ingestion:**
   - IRS Pub 78, EO BMF and auto-revocation, checked at approval and at release: CNV-GRT-003 (initial-implementation).
   - OFAC list delta screening: CNV-GRT-006.
   - California Attorney General Registry status: CNV-GRT-015.
   - One bank feed, either BAI2/BTRS or a bank API, plus one payment-partner adapter: CNV-PAY-007 ("Release 1 SHALL ship one bank-feed adapter …"). Bank activity is ingested daily and every debit is matched: UNB-XIN-BNK-003 (R1).
   - ACH return and NOC matching for grant payments "from release 1": CNV-PAY-005 says "never auto-post" for fallback matches.
   - One custodian's positions and transactions: OD-M-07 (line 6) and CNV-FIN-013, which requires raw feed preservation and queuing of unmatched deliveries.
   - Feed-completeness watermarks and control totals: UNB-XIN-EVA-004 (R1).
   - Source-derived idempotency keys: UNB-XIN-EVA-005 (R1).
   - Continuous reconciliation in ProvisionalCalibration: CNV-FIN-004.
   - Outbound positive-pay issue files: CNV-PAY-002 and UNB-XIN-BNK-006 (R1).
4. **Some of this already exists in Unbound.** `replay/src/Unbound.Replay/Sources.fs` (186 lines) and `Csv.fs` (38 lines) already parse Pub 78, revocations, EO BMF, OFAC SDN/ALT and IRS 990 e-file XML. Report 14 (`14-PUBLIC-DATA-REPLAY.md:32,42`) ran them over 151,567 Schedule I rows and 369,247 revocations. Unbound also has its own acquisition model (`architecture/CHARITY-KNOWLEDGE-MODEL-AND-ACQUISITION-PIPELINE.md:9-10`, with AcquisitionRun and RawEvidence including contentHash and checksum) and its own exception machinery: the Case kernel (UNB-XIN-SVC-002, R1) and WorkItems for provider Unknowns (RR-REQ-X-048-r2, R1).

---

## C10. "A visual pipeline designer (Forma-based admin UI) is necessary"

### Strongest case against

- **It fails Transitus's own genericity test.** `docs/research/02-use-cases.md:12-15` says a feature is in scope "only if at least two scenarios (ideally across two applications) need it". The genericity table at line 93 marks the visual designer as Unbound-only ("✓ | — | —"). Helix Note, Summa and Chrona do not need it.
- **No release-1 user exists for a designer.** Release-1 configuration is "Platform-maintained default packs … Sponsor-authored packs [out]" (`17-RELEASE-1-SCOPE.md`, Configuration row). Unbound has already rejected a general no-code rules engine (SPR-CFG-002, `19-REJECTED-APPROACHES.md:50`) and deferred its visual email designer (REQ-X-031, simplification matrix line 1655). Release-1 pipeline authors are Unbound engineers and agents. Under Transitus's own principles they work on JSON, in Git, with semantic diffs; the designer is a projection of that JSON (TRN-ARCH-10 §2).
- **The competitive research argues against designer-first tools.** `01-competitive-research.md:129,958` cites designer-coupled XML (SSIS `.dtsx`, PDI) as a failure mode.
- **The requirements contradict themselves.** TRN-ARCH-10 §1 calls the UI "phase 4 and optional". Yet TRN-REQ-UI-002 and TRN-REQ-UI-004 are **P0**, which the register defines as "required for first production use". TRN-REQ-UI-003 binds 16 views. TRN-REQ-UI-010 (P0, phase 2) commits the host to a versioned OpenAPI for "all configuration, execution, approval, exception and lineage operations". For a host whose domain API does not yet exist, that is a large obligation.
- **Most of the "views" duplicate Unbound surfaces.** Exception queues, approval workflow, reconciliation results and execution history (TRN-ARCH-10 §3) overlap Unbound's R1 Case kernel, WorkItem and SourceFeedGapDetected/DuplicateKeyConflict cases (UNB-XIN-EVA-004/005). They also overlap UNB-CUST-020 (Forma views of discrepancies and approvals) and UNB-CUST-021 (Folio reconciliation packs). A separate Transitus admin would give staff a second exception inbox. That works against the minimum-touch operating model.
- **The dependency is not ready.** Forma ADR-0006 (`kemiller2002/forma/docs/decisions/ADR-0006…md`) says Limen's `BrowserKernel` "cannot host a component inside a page whose host already runs its own kernel". Transitus already needs DEP-FORMA-01, because Forma's workflow model lacks partition routing with a mandatory `otherwise`.

### Concessions

The proposal does not claim the designer is needed now. It defers it to phase 4, forbids a bespoke graph editor (TRN-REQ-UI-001) and makes JSON authoritative. That is the right shape. A *read-only* projection of lineage and run status could be useful for auditors later.

### Verdict: **Upheld**, against necessity

A designer is not necessary for Unbound release 1, or for any identified consumer within the planning horizon.

### Required revisions

- Rename TRN-ARCH-10 to "Visual administration (conditional)". Add a trigger: build it only when (a) a second application, or sponsor-authored pipelines, is approved, **and** (b) a measured authoring-time study shows JSON plus validator plus diff is a bottleneck.
- Downgrade **TRN-REQ-UI-002** and **TRN-REQ-UI-004** from P0 to P2 (conditional). Mark **TRN-REQ-UI-001** and **TRN-REQ-UI-003** "deferred / conditional".
- Rewrite **TRN-REQ-UI-010**. It should require a library API (F# functions plus JSON documents) for the operations release 1 uses. Host HTTP/OpenAPI exposure belongs to Unbound's API standards (CNV-EXP-001, RR-UNB-API-STD-003-r1), not to Transitus. Move it to phase 2 at P1.
- Add **TRN-REQ-UI-011** (P0): exceptions, approvals and feed gaps MUST surface through the host's case and work-item system (Unbound Case kernel), with no Transitus-owned inbox.
- Add **TRN-REQ-UI-012** (P1, phase 2): a CLI or static Folio and Forma HTML rendering of the pipeline graph, run evidence and semantic diff, using Forma.Workflow's static renderer. Read-only, with no WASM editor.
- Drop **TRN-REQ-LN-004** (Folio) from phase 4 to phase 2 only if Unbound's UNB-CUST-021 requires it. Otherwise keep it deferred.

---

## C11. "Transitus will not introduce excessive maintenance obligations"

### Strongest case against

**The obligation inventory, as proposed:**

| Obligation | Count | Source |
|---|---|---|
| Code packages | 11 named, plus the Conformance suite, so **12**. The doc says "eight". | TRN-ARCH-11 §2 table (lines 146-161); `03-adapter-architecture.md:142` |
| Adapters planned (phase 1–3) | **16**, plus 2 "not planned" | `03-adapter-architecture.md:105-124` |
| Third-party parser and transport libraries | Sylvan.Data.Csv, ExcelDataReader or Open XML SDK, SSH.NET, Parquet.Net, Npgsql, Microsoft.Data.SqlClient, AWS/Azure SDKs: **about 7**, each needing an ADR (TRN-REQ-ARC-005), fuzzing (SEC-001) and vulnerability tracking (SEC-014/017) | same table |
| Transformation operations | **55**, each versioned `name@major` with golden tests (TX-001) | `04-transformation-library.md` §3 |
| Validation and reconciliation primitives | **21** | `06-validation-and-reconciliation.md` |
| Mapping packages | **18** in the Unbound catalogue, 6 of which are placeholder vendor packages with no public schema. Each has schemas, mappings, reference code sets, fixtures, detectors and a changelog, with semver and upgrade diffs. | `09-mapping-packages.md:60-75` |
| Transitus schemas | 4 (`pipeline`, `mapping-package`, `adapter-descriptor`, `evidence`), plus 22 Praxis schemas carried in the repo | `transitus/schemas` |
| Requirements | **115**, of which 89 are P0 | `requirements/requirements.json` |
| Cross-repository obligations | 7 (DEP-EXEC-01 … DEP-REG-01), including forcing extraction of Echelon.Execution | TRN-ARCH-11 §3 |

**Team size.** `echelon-registry/portfolio/analysis/duplication-and-drift.md:21` describes "One accountable owner, ~64 Echelon repositories (57 public), 32 registered systems, 29 initiatives, most work performed by autonomous agents". Every shallow clone under `kemiller2002/*` shows a single human committer. Unbound's last 30 days show 170 commits: 120 by the agent and 50 by the owner. Human review capacity, not agent typing, is the binding constraint. Transitus's own estimate of 0.1–0.2 FTE ongoing (`12-performance-and-economics.md:122`) would be 10–20% of the portfolio's only accountable human. That does not count the phase 1–4 build of 26–40 engineer-weeks.

**The portfolio's own drift diagnosis predicts the failure.** PF-ANL-003 §1 says "Creation is cheap, reconciliation is not … Agents create repositories, systems and documents faster than any process updates shared records". It also notes drift is present "in released, depended-on foundations". Evidence of that pattern already shows in this proposal:

- `TRACEABILITY.md` says charter sections §1–§22 are "captured in PROJECT-CHARTER.md". The charter is an unfilled template about a "communication problem", with no owner, users or bounded outcome (DRF-05 pattern). It also requires a first outcome "delivered and evaluated in two to four weeks", while phase 1 is estimated at 6–10 engineer-weeks.
- The registry already lists Transitus as `active` against four initiatives (`portfolio/generated/repositories.md:21`) before any code exists.
- Internal inconsistencies:
  - "eight code packages" against the 12 actually named.
  - The phase-1 `Transitus.Checks` package against TRN-REQ-VR-001/002 (phase 2).
  - "dry run" in the phase-1 cost row (TRN-ARCH-12 §6) against TRN-REQ-EX-004 (phase 2).
  - P0 requirements in an "optional" phase 4.

**Duplication risk is the DUP-06 pattern.** Raw preservation and acquisition runs would exist twice: Transitus TRN-REQ-ST-001 and Unbound's RawEvidence/AcquisitionRun (UNB-KNOW-023/027). Exception handling would exist twice: Transitus queues and Unbound's Case kernel. Parsers would exist twice: `Unbound.Replay/Sources.fs` and the `irs.*` packages. TRN-ARCH-11 line 133 states the replay tool "stays Unbound's". That guarantees two IRS parsers.

**The mapping-package placeholders are a maintenance trap.** Six vendor packages have "none public" as their basis (`09-mapping-packages.md`), and daf-landscape confirms no public export schemas. Their maintenance cost is paid before any customer sample exists, and each first real sample will rewrite them.

### Concessions

- The design keeps several obligations low: no deployed service (TRN-REQ-ARC-001), host PostgreSQL only (ARC-004), consumption of Echelon.Execution rather than a second queue (EX-001), and P12 "smallest sufficient adapter set".
- Four of the code packages are pure, so their maintenance is cheap.
- Configuration-only packages carry less risk than connector code.
- Commercial alternatives were honestly costed, and the cash-cost argument was conceded (TRN-ARCH-12 §5).

### Verdict: **Upheld**, against the claim

As scoped (12 packages, 16 adapters, 55 operations, 18 mapping packages, 115 requirements) the proposal is excessive for a one-owner, agent-staffed portfolio with documented drift. It is defensible only if cut to the phase-1 scope below and gated on a second consumer.

### Required revisions

- Collapse phase 1 to **three packages at most**: `Transitus.Model` (including Validation.Definition), `Transitus.Core` (Transforms plus Checks, pure), and `Transitus.Formats` (CSV, fixed-width and the release-1 bank and NACHA formats). Abstractions, Engine, Storage.Postgres, Lineage, Assist and Admin should be created only when an exit criterion is met.
- Amend **TRN-REQ-TX-009**: the phase-1 catalogue is limited to operations used by the release-1 pipelines (likely about 15). Every further operation needs a consumer pipeline that uses it.
- Amend **TRN-REQ-AD-005**: remove XLSX, JSON/NDJSON and the generic "upload" path from phase 1 (see C12). Add a rule that every adapter cites a release-scoped consumer requirement ID.
- Amend **TRN-REQ-MP-001/002**: no package is created with basis `synthetic-representation` for a named vendor until a customer-authorized sample exists. Delete the six vendor placeholders from the catalogue.
- Add **TRN-REQ-ARC-006** (P0): Transitus MUST NOT duplicate Unbound's RawEvidence/AcquisitionRun or the IRS/OFAC parsers. The Unbound.Replay parsers are *moved* into Transitus.Formats (one copy), or they stay in Unbound and Transitus does not build `irs.*`.
- Add **TRN-REQ-ARC-007** (P0): a maintenance budget. Before each phase, declare the owner-review hours per month and the count of packages, adapters, operations and third-party dependencies, measured against the Praxis pilot. Exceeding the budget blocks phase entry.
- Fix the traceability defect: fill in `PROJECT-CHARTER.md` (owner, users, bounded outcome) or stop citing it. Reconcile the package count, VR phase and dry-run phase inconsistencies.
- Change the registry entry to `requirements` maturity with no initiative claims beyond INIT-005 until a second consumer commits (DEP-REG-01).

---

## C12. "Transitus does not distract from Unbound"

### Strongest case against

- **Phase 1 is aimed at the part of Unbound that release 1 deferred.** Phase 1 (TRN-REQ-AD-005; TRN-ARCH-12 §6) is upload, HTTPS, CSV/TSV, fixed-width, XLSX, JSON/NDJSON, mapping-package machinery (MP-001..003) and an Unbound domain-API destination. Its driving scenarios are migrations and bulk import: U1, U9 and U10, and "spreadsheet administration, migrations" for XLSX at `03-adapter-architecture.md:116`. Release 1 says "no migration in R1" (above).
- **What release 1 needs is mostly in Transitus phase 2.**
  - NACHA returns/NOC is phase 2, but CNV-PAY-005 requires it from release 1.
  - BAI2 and camt.053 are phase 2 (`09-mapping-packages.md`), but CNV-PAY-007 and UNB-XIN-BNK-003 need them in release 1.
  - SFTP is phase 2, but bank and custodian files need it.
  - Raw preservation (ST-001), control-total reconciliation (VR-002), idempotency keys (EX-006) and the engine are all phase 2. CNV-FIN-013 and UNB-XIN-EVA-004/005 need them in release 1.
  - OFAC (CNV-GRT-006), the California AG registry (CNV-GRT-015) and positive-pay issue files (CNV-PAY-002 and BNK-006, outbound) do not appear in 02-use-cases at all.
  - No use case is mapped to a `release_scope` value.
- **Phase 1's only P0 destination cannot be built.** TRN-REQ-AD-005 and AD-008 require loading "through Unbound domain APIs", and none exist. The phase-1 destination would be designed against a guessed contract, then rewritten.
- **It pulls on Unbound's critical path.** DEP-EXEC-01 asks Unbound to extract Echelon.Execution "now that a second consumer is defined". That module is an unbenchmarked first slice whose falsification criteria (RM-05, CNV-ARC-001 benchmark) have not run. Extracting it early moves Unbound's most safety-critical infrastructure into a shared repository with two masters. Proposal UNB-TRN-012 (batch-capable domain operations, TRN-ARCH-12 A8) asks Unbound to shape its domain API around Transitus's throughput.
- **The owner's stated priority is evidence and a first sponsor.** OD-M-14 says "build it now", with the first paying sponsor's shadow replay and time study as the evidence. Readiness fails on economics measurement and executed dependencies (licence, ODFI/rail, identity provider, auditor). Ingestion is not among the blockers. Every engineer-week spent on 55 generic operations is one not spent on the readiness blockers.
- **An Unbound-internal module would suffice.** The IRS/OFAC half already exists in about 225 lines of F#. One BAI2 parser, one NACHA return/NOC parser and one custodian file mapping, each with control totals, an idempotency key (EVA-005), raw hash preservation (CNV-FIN-013) and routing to the Case kernel, is a bounded module inside Unbound. It is a few thousand lines and needs no pipeline language, expression language, mapping-package semver, overlays or AI assist.

### Concessions

- Migration *is* commercially important. daf-landscape OPP-10 (`data/commercial-opportunity/ai-native-capital-minimization/opportunities.csv:11`) records demonstrated demand (Ren sells a migration add-on; 8 CF migrations; $25–75k per project hypothesis) and recommends "Build early; sell as onboarding + independent assurance". CNV-EXP-002 is owner-ratified as initial-implementation, and the first paying sponsor will come from some predecessor platform.
- OPP-10 rates disconnected-product risk "Low: the importer is the onboarding tool" and lists shared components with Unbound as "Import pipelines, canonical grant record, reconciliation". That supports building migration as *an Unbound onboarding capability*, not as a portfolio engine.
- The Transitus design does correctly keep the domain in Unbound (MigrationRun, cutover and accounting profiles: TRN-REQ-VR-006).
- Its gate discipline matches Unbound's controls: zero monetary tolerance (VR-003), no auto-merge of financial entities (TX-008) and OutcomeUnknown handling (EX-007).

### Verdict: **Upheld**, against the claim

As phased, Transitus is a distraction. It is out of step with release-1 demand, depends on an API that does not exist, and asks Unbound to extract critical infrastructure early. The contested point is CNV-EXP-002 against "no migration in R1". That conflict must be resolved by the Unbound owner, not by Transitus.

### Required revisions

- Add **TRN-REQ-ARC-008** (P0): every phase-1 requirement MUST cite an Unbound requirement with `release_scope` ∈ {R1, initial-implementation} from `requirements/baseline/baseline.jsonl`. Untraced items move to a later phase.
- Re-phase as follows:

  | Requirement | Change |
  |---|---|
  | **TRN-REQ-AD-005** | phase 1 = HTTPS, SFTP (moved up from phase 2), CSV/pipe-delimited, fixed-width, BAI2/BTRS **or** the selected bank API format, NACHA returns/NOC, the selected custodian's file format, and a staging-only sink |
  | XLSX, JSON/NDJSON (unless the chosen bank or custodian API needs JSON), upload, Unbound domain-API destination | defer until CNV-EXP-002 is scheduled and the domain API exists |
  | **TRN-REQ-ST-001** (raw preservation, minimal form: content hash plus metadata in host PostgreSQL) and **TRN-REQ-VR-002** (counts, control totals, hash totals only) | move to phase 1, because CNV-FIN-013 and UNB-XIN-EVA-004 need them in R1 |
  | **TRN-REQ-EX-006** | replace with conformance to UNB-XIN-EVA-005's key and payload-hash rule; Unbound owns the key registry |
  | **TRN-REQ-MP-001..005**, **TRN-REQ-AI-***, **TRN-REQ-TX-008**, **TRN-REQ-EX-003** (all modes), **TRN-REQ-EX-012** | defer to phase 3 or later (conditional on migration) |

- Withdraw **DEP-EXEC-01** (extraction now). Replace it with "extract after the RM-05 benchmark passes and a second consumer is in production". Withdraw **UNB-TRN-012** until load measurements exist (TRN-REQ-PF-001).
- Add use cases for OFAC delta screening, the California AG registry and the positive-pay issue file. If outbound files stay out of scope, record that explicitly.
- File an Unbound open question asking the owner to reconcile CNV-EXP-002 (initial-implementation) with "no migration in R1" (17-RELEASE-1-SCOPE, simplification matrix). The answer decides whether migration (U1, U10) moves to phase 2.

---

## Minimal viable phase 1 justified by Unbound release-1 demand

**Form.** Start as an Unbound-internal module, `Unbound.Ingestion`, inside the Unbound solution. Use Transitus's design constraints but none of its packaging. Extract it to Transitus only when a second application (Helix Note FHIR, or Summa bank feeds) commits to a dated need. This follows the Echelon.Execution precedent of "incubate in Unbound; extract on the second consumer" (`unbound/execution/README.md`).

**Scope (each item traced to a release-1 requirement):**

| Area | Content | Traces to |
|---|---|---|
| Sources | IRS Pub 78, EO BMF and auto-revocation over HTTPS, by moving the existing `Unbound.Replay/Sources.fs` parsers rather than rewriting them; OFAC SDN/ALT; California AG registry | CNV-GRT-003/006/015 |
| Bank and payments | One bank feed (BAI2/BTRS or the chosen bank API) over SFTP or HTTPS; NACHA return/NOC files | CNV-PAY-007, UNB-XIN-BNK-003, CNV-PAY-005 |
| Custodian | The single custodian's position and transaction file | OD-M-07, CNV-FIN-013 |
| Primitives | SHA-256 raw preservation with source metadata; snapshot diff by natural key (EIN); count, control-total and hash-total checks with zero monetary tolerance; expected-delivery calendar and watermark; EVA-005 idempotency key and payload hash; typed, located parse errors; resource limits | UNB-XIN-EVA-004/005, CNV-FIN-004 ProvisionalCalibration |
| Runtime | Echelon.Execution commands, in place, as it is incubated in Unbound today | — |
| Exceptions | Routed to the Unbound Case kernel and WorkItems | — |
| Outbound | Positive-pay issue file generation, if it is assigned here | CNV-PAY-002 |

**Out of phase 1:**

- Pipeline JSON language and the expression language beyond what these fixed pipelines need.
- The 55-operation catalogue, mapping packages and overlays, XLSX, the generic upload, and migration.
- AI assistance, lineage L2, evidence hash chains beyond the host's (use the Unbound evidence model), and any UI.

**Exit criteria to create Transitus proper:**

1. A second application commits to a dated need.
2. The Unbound owner schedules CNV-EXP-002 migration with a named predecessor platform and an authorized export sample.
3. The ingestion module has run against real release-1 feeds for one close cycle, so TRN-REQ-PF-001 has measurements.

Until then, Transitus stays a requirements repository (`maturity: requirements`). Its 115 requirements are retained as a design reference, not as a build commitment.
