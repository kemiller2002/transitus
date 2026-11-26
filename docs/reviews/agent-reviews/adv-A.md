# Adversarial review A: Transitus

Reviewer stance: try to refute the proposal using evidence; concede where the evidence supports it.
Scope: `transitus/docs/**`, `requirements/REQUIREMENTS.md`, `schemas/*.json`, and the read-only evidence repositories listed in the brief. The review modified no repository files.

## Headline

Transitus answers a real gap: no Echelon component ingests external files with raw preservation, control totals and evidence. But the proposal is sized for a product that has no user yet. It is not sized for the consumer it names. Unbound Release 1 has **no migration**. It has one sponsor, one custodian and one bank, and it is deferring acquisition that no decision consumes. That leaves roughly six fixed, publicly specified or bank-specified feeds. For that workload the proposal specifies 115 requirements, 89 of them P0, plus 16 stage kinds, a typed expression language, packages with overlays, authority-envelope diffs and AI assistance, at an estimated 26–40 engineer-weeks plus 0.1–0.2 FTE. The project's own charter asks for "one outcome that can be delivered and evaluated in two to four weeks" (`PROJECT-CHARTER.md`, "First bounded outcome").

---

## C1. Transitus duplicates Strata or other existing Echelon capabilities

### Strongest case against

1. **Echelon.Execution already owns the load-side semantics. Transitus re-specifies them.**
   - Execution provides "Intake, idempotency, ordering, leases, retries, quarantine, unknown outcomes, lifecycle history, status and the outbox" (`unbound/execution/README.md:18`). It also provides "OutcomeUnknown is never retried; replay is refused" (`:61`).
   - Transitus nonetheless defines the same things again:
     - its own per-record idempotency keys (TRN-REQ-EX-006; `schemas/pipeline.schema.json:154,160`);
     - its own OutcomeUnknown rule (TRN-REQ-EX-007);
     - its own intent and receipt protocol (TRN-REQ-EX-008);
     - its own delivery-guarantee taxonomy (TRN-REQ-AD-007);
     - its own `retry` block with backoff and jitter (`pipeline.schema.json:122,151`);
     - its own durable approval wait (stage 10).
   - When Transitus is embedded in Unbound, the "Unbound domain API destination" can only mean submitting Execution commands. A second retry, idempotency and unknown-outcome layer on top of that one is duplication, and it risks semantic conflict: two components deciding whether a retry is safe.

2. **Unbound already designs the acquisition half.**
   - `unbound/architecture/CHARITY-KNOWLEDGE-MODEL-AND-ACQUISITION-PIPELINE.md` already defines the following:
     - `AcquisitionRun` with cursor, counts, errors, retries and checksum (line 9);
     - `RawEvidence` with content hash, rights policy and retention (line 10);
     - the pipeline "snapshot/change retrieval -> immutable ingestion manifest -> validation/quarantine -> raw evidence capture if permitted -> parser" with "append-only evidence and idempotent, resumable checkpoints" (lines 40–42);
     - per-connector retry and cadence declarations (UNB-KNOW-024);
     - drift and implausible-delta quarantine (UNB-KNOW-026);
     - resumable, idempotent ingestion (UNB-KNOW-027, line 82).
   - That is Transitus stages 1–6 and part of 8–9.
   - TRN-ARCH-11 claims Transitus "implements the generic AcquisitionRun → RawEvidence half". The two models already **conflict**:
     - Unbound stores raw bytes "only when permitted; otherwise lawful references/derived claims" (line 10).
     - TRN-REQ-ST-001 says raw inputs "MUST be preserved immutably … before any parsing", and `preserve` is mandatory for system-of-record pipelines (TRN-REQ-PS-003).
   - Transitus has no rights-policy concept that could make preservation conditional.

3. **The parsers Transitus would build already exist as a working baseline.**
   - `Unbound.Replay/Sources.fs` (186 lines) already parses Pub 78, auto-revocation, EO BMF, OFAC SDN/ALT and Form 990 XML as pure F#. For example, `parseBmf` is at lines 51–60 and `parseReturn` at line 139.
   - Those parsers *are* the R1 feed set (proposal U2 and U3, plus screening).

4. **Summa will not consume Transitus.**
   - `summa/src/Summa.Operations/FinancialMigration.fs:1–15,25–38` already implements its own pipeline: a migration `Definition` with `Transform: Record -> Result<Record,string>`, a declared rollback, conservation verification ("no record lost without lineage, the trial balance unchanged"), backup, Arca copy, read-back and reconcile.
   - `Summa.Storage/Reconciliation.fs` is pure ledger self-reconciliation.
   - Summa stores in Arca (Git/WASM). Transitus explicitly cannot stage there (TRN-ARCH-11 row "Arca"). Listing Summa as the "second financial consumer" (`02-use-cases.md` §C) is speculative.

5. **Helix Note already owns its own extraction provenance.**
   - `helix-note-application/api/HelixNote.Data.FileExtraction.fs` (380 lines) holds extraction jobs, entity-to-source links and review status (lines 7–10, 94–133, 212–264).
   - Helix use cases H1–H5 are hypothetical. None cites a Helix requirement that asks for Transitus.

6. **Strata DIV overlaps at the adapter boundary.**
   - DIV-002 (adapters routed through replaceable contracts), DIV-008 (record and replay after redaction) and DIV-015 (every external contract ships a mock adapter) (`strata/docs/requirements/data-interaction-virtualization.md:12,18,25`) would cover Transitus transports such as HTTPS and SFTP.
   - Transitus proposes its own adapter conformance suite and fixtures (TRN-REQ-AD-003) instead.

7. **The extraction trigger is mis-cited.** Echelon.Execution extracts when "a second transactional **application** needs it" (`README.md:5`). Transitus is a library embedded in Unbound, not a second application. DEP-EXEC-01 overstates the case.

### Concessions

- Strata is schema management only (`strata/README.md`). It has no staging, parsing or reconciliation, so Transitus does **not** duplicate Strata itself.
- TRN-ARCH-11 is an unusually honest overlap analysis. It already consumes Execution for queueing (TRN-REQ-EX-001).
- `Sources.fs` illustrates the gap Transitus targets:
  - malformed rows silently become `None` (`parseBmf`, lines 51–60);
  - there are no conservation counts and no raw preservation.
- There is no generic raw-evidence and control-total library anywhere in the portfolio.

### Verdict: **partially upheld**

Strata duplication is rejected. Duplication of Echelon.Execution load semantics and of Unbound's acquisition model is upheld.

### Required revisions

- **R1-a.** Delete TRN-REQ-EX-006/007/008 and AD-007 as Transitus mechanisms. Restate them as "a load is an Echelon.Execution command submission; the idempotency key, OutcomeUnknown and receipts are Execution's." Remove the pipeline-level `retry` block for `load`.
- **R1-b.** Make Unbound's `AcquisitionRun`/`RawEvidence` the single model. Transitus implements it as a library; it does not define a parallel `RawObject`. Add a rights-policy input so preservation is conditional: change TRN-REQ-ST-001 and PS-003.
- **R1-c.** Port `Unbound.Replay/Sources.fs` parsers into the first Transitus format modules, adding typed errors and counts. Do not re-derive them as packages.
- **R1-d.** Drop Summa and Helix as validating consumers until either team files a requirement. Genericity claims in `02-use-cases.md` §D must cite consumer requirements, not hypotheses.
- **R1-e.** Agree the DIV boundary before building transport adapters (DEP-STRATA-02 becomes a phase-1 gate). Use DIV mocks for transport conformance.

---

## C2. Existing products would be more economical

### Strongest case against

- Cash cost is not the argument. The proposal itself concedes that commercial tools are "hundreds to low thousands of dollars per year" at Echelon volumes (`12-performance-and-economics.md` §5).
- Engineering is the dominant cost: 26–40 engineer-weeks plus 0.1–0.2 FTE ongoing (§6). That estimate is theoretical, and it predates the 115-requirement register.

**dlt (SRC-112–114)**
- dlt is Apache-2.0, "a library, not a platform", with schema contracts (`evolve`/`freeze`/`discard_row`) and incremental state.
- A dlt sidecar could land the four IRS files and OFAC into PostgreSQL staging tables. F# would then apply checks and submit Execution commands.
- That would cost days, not weeks.

**Meltano/Singer (SRC-110–111)** offers the same tap model, with existing taps for SFTP and CSV.

**Apache Hop (SRC-094–095)**
- Hop already has metadata-driven pipelines and golden-dataset unit tests, which is exactly what Transitus proposes to build.
- The research itself names Hop "the closest open-source analogue".

**Airbyte**
- Airbyte's connector-builder approach covers HTTPS and file sources.
- Self-hosting costs about 0.5 FTE per quarter (SRC-068). That is comparable to Transitus's own 0.1–0.2 FTE maintenance estimate.

### Concessions (substantial)

1. **The no-second-runtime constraint is real and binding.**
   - dlt and Meltano are Python. Hop is JVM.
   - Unbound is an F# component monolith (REQ-X-057, cited in the Unbound register at `requirements/discovery/2026-11-24-simplification-economics/data/register.jsonl:1280`).
   - A Python sidecar adds a second dependency supply chain and a second SBOM. It also adds a process boundary that handles donor and financial data.

2. **The regulated-data argument is real.**
   - SaaS ELT tools (Fivetran SRC-001/002, Airbyte Cloud SRC-003) make a third party a processor of donor PII and financial records.
   - Fivetran pricing changed mid-contract (§5, failure mode 1). Licence instability is documented across the category (failure mode 7: SRC-043, SRC-058, SRC-066, SRC-117).

3. **None of the products loads through domain commands with blocking gates.**
   - dlt, Airbyte and Fivetran target warehouses or lakes.
   - The hard part of Unbound's feeds is reconciliation: NACHA entry hash, control totals and timing windows. That has to be written regardless of the tool.

4. **dbt is irrelevant.** It neither extracts nor loads (SRC-080).

### What the proposal gets wrong

- The proposal compares Transitus against products. The cheapest credible alternative is neither a product nor Transitus: it is **hand-written, typed F# per feed plus a small shared kernel**. `Unbound.Replay` shows that costs hundreds of lines per source.
- `12-performance-and-economics.md` §5 has no row for this baseline. The charter requires "a declared lightweight baseline" ("Success criteria").
- The proposal also ignores buy-at-library-level options. Mature .NET parsers exist for CSV, XLSX and SFTP. Their reuse should be stated explicitly; reinvention would compete with the "buy" argument.

### Verdict: **partially upheld**

- **Rejected** for the external products named: they fail the F#-only and regulated-data constraints and do not do domain loading.
- **Upheld** in substance: the economical option is not the full Transitus. It is a minimal F# library justified against a hand-coded baseline.

### Required revisions

- **R2-a.** Add a "hand-coded F# per feed" baseline row to TRN-ARCH-12 §5. Re-estimate cost from the register as it now stands, not the earlier scope.
- **R2-b.** Add a requirement: every third-party parser is an existing maintained .NET library, recorded under TRN-REQ-ARC-005. No in-house CSV or XLSX parser.
- **R2-c.** Add a kill criterion. If phase 1 cannot replace `Unbound.Replay` ingestion plus one bank file in less than or equal to the hand-coded estimate × 1.5, stop at the kernel.
- **R2-d.** Remove the OPP-10 migration revenue claim ($25–75k, `daf-landscape/data/commercial-opportunity/ai-native-capital-minimization/opportunities.csv:11`) as a justification for phase 1. It is hypothesised, and Unbound R1 has "no migration in R1" (`unbound/requirements/discovery/2026-11-24-simplification-economics/01-REVERSE-REQUIREMENTS-ANALYSIS.md:571`).

---

## C3. The pipeline model is too complex

### Strongest case against

1. **Scope versus consumer.**
   - The R1 consumer set is narrow. Unbound R1 has one custodian and a single sponsor, with Unbound as book of record (`17-RELEASE-1-SCOPE.md:14–16, 30`). It is deferring acquisition "no decision consumes" (`01-REVERSE-REQUIREMENTS-ANALYSIS.md:243`). Payroll is not in R1 (OD-M-02, which `02-use-cases.md` U6 itself notes), and migration is out (`:571`).
   - So use cases U1, U6, U9, U10 and U12 have no R1 driver.
   - What remains:
     - BMF, Pub 78 and revocation;
     - OFAC;
     - one custodian file;
     - ACH returns and settlement, whose bank specification is not yet obtained (`17-RELEASE-1-SCOPE.md:64`).
   - That is a handful of fixed formats owned by developers. Nothing requires end-user-authored pipelines.

2. **The stage-kind count is inflated and internally inconsistent.**
   - The docs say "fourteen". `pipeline.schema.json:136` enumerates **16** (adding `route` and `union`).
   - `discover`/`ingest`/`preserve` and `parse`/`stage` are implementation steps of one acquisition, not user-meaningful nodes.
   - `profile` is non-blocking by default. `retain` is a background sweeper, not a pipeline stage.

3. **A bespoke expression language (TEL) is a second language to specify, type-check, document and fuzz.**
   - TRN-REQ-PS-007 and PS-009 require it, and its AST includes `Case`, `Call`, `Ref` and `Arith` with decimal contexts.
   - The safety goal is "no arbitrary code" (TRN-REQ-PS-006). F# already meets that goal for developer-authored pipelines: they are compiled, reviewed and typed.
   - The research lists Jinja/dbt string-templating as a top complaint (SRC-083, SRC-085), so a new mini-language repeats a category failure mode.

4. **Packages with overlays, semver detectors, upgrade diffs and promotion review (TRN-ARCH-09, TRN-REQ-MP-003..005) only pay off for repeated vendor migrations.**
   - That is the deferred use case.
   - TRN-ARCH-09 §3 itself shows six vendor packages as "placeholder only" and several more as "skeleton".

5. **Authority-envelope diffs (TRN-REQ-PS-008) protect against untrusted pipeline authors widening egress, destinations or classification.**
   - With developer-authored code, the same control already exists: code review plus TRN-REQ-SEC-013 (host-registered destinations) and SEC-015 (egress allow-lists in host configuration).
   - The control only becomes necessary once non-developers or AI publish pipelines. That is phase 3–4.

6. **Several control mechanisms protect against the same mutation of approved data.**
   - Merkle sealing (TRN-REQ-ST-005);
   - a per-execution hash chain plus a per-tenant anchored chain (LN-006);
   - signed approval events (LN-005);
   - SOC 2 evidence generators (SEC-019).
   - These are layered on an engine with no code. 89 P0s is not a "first production use" bar.

7. **Traceability is weak.** The decisions cited (DF-TRN-2026-0001…0015) have no records: `docs/decisions/` contains only `README.md`. `PROJECT-CHARTER.md` is still the unfilled template.

### Concessions

- The *invariants* are sound and cheap to implement as library functions:
  - the conservation law (TRN-REQ-VR-007);
  - decimal-only money with no silent rounding (TX-005);
  - missing, null and present kept distinct (TX-006);
  - zero default monetary tolerance (VR-003);
  - no auto-compensation (EX-009);
  - parser hardening (SEC-001..007).
- `Unbound.Replay` would benefit from them immediately.
- The DAG restrictions are a sensible bound *if* a DSL is ever needed: no loops, a total `route` with `otherwise`.
- Excluding sub-pipelines (DF-TRN-2026-0003) and bidirectional sync (AD-010) shows restraint.

### Verdict: **upheld**

### Required revisions

- **R3-a.** Defer the JSON pipeline document, TEL, stage templates, packages, overlays and authority-envelope diffs to a conditional phase. Gate that phase on a named consumer requirement for non-developer-authored pipelines, such as an enabled R2 migration.
  - Requirements affected, re-prioritised to P2: TRN-REQ-PS-001, 005, 007, 008, 009, 010; MP-001..005; UI-001..004; AI-001..008.
- **R3-b.** Collapse the stage kinds to five library steps:
  - `acquire` = discover + ingest + preserve, preservation subject to rights policy;
  - `parse` = parse + stage;
  - `check` = validate + reconcile + profile-as-check;
  - `load` = an Execution command plus verify;
  - `evidence`.
  - Authorization is Execution's approval wait. Retention becomes a host sweeper.
- **R3-c.** Express pipelines as F# functions over typed records, using a small combinator module. Keep TRN-REQ-PS-006 as "no runtime-loaded code".
- **R3-d.** Replace Merkle sealing and the two hash chains with one SHA-256 over the staged dataset bound to the approval record. Defer the anchored tenant chain and SOC 2 generators (LN-006 and SEC-019 to P2).
- **R3-e.** Reduce the P0 set to what the R1 feeds need, about 30. Write the missing DF-TRN decision records or remove the citations. Fill in the charter.

---

## Smallest viable architecture

**One repository with three packages, all F# and in-process, consuming Echelon.Execution and Strata.**

### 1. `Transitus.Evidence` (pure)

- Implements Unbound's `AcquisitionRun`/`RawEvidence` model:
  - content-addressed raw capture, gated by rights policy;
  - an `IBlobStore` port with a PostgreSQL default;
  - a run manifest;
  - a conservation table (in = out + rejected + quarantined + dedup + filtered);
  - an evidence document that hashes inputs, outputs, checks and approval.
- Its DDL is Strata-governed.

### 2. `Transitus.Formats` (pure)

- Streaming, typed parsers built on existing .NET libraries:
  - CSV and pipe-delimited;
  - fixed-width, including NACHA;
  - XLSX;
  - Form 990 XML, with XXE disabled.
- Each parser returns `Result<Record, LocatedError>` per row, and no row is dropped silently.
- It starts by porting `Unbound.Replay/Sources.fs`. Parsers are fuzzed.

### 3. `Transitus.Checks` (pure)

- Required, type, code-set and check-digit validation;
- uniqueness;
- count, control-total and hash-total checks;
- opening + movements = closing balance;
- keyed set match;
- snapshot diff by natural key;
- timing windows;
- zero default money tolerance.

### Feeds

- Each feed is a ~50–150-line F# module in the host: `acquire >> parse >> check >> plan`.
- A blocking result stops the feed.
- The load plan becomes Echelon.Execution commands, which carry idempotency keys, OutcomeUnknown handling and approval waits.
- Post-load read-back runs as a `Checks` call.

### Cost

- The first slice is BMF, Pub 78, revocation and OFAC, replacing the Replay ingestion with evidence.
- That is roughly 3–4 engineer-weeks, consistent with the charter.

### Deferred, each behind a named consumer requirement

- the JSON pipeline DSL and TEL;
- packages and overlays;
- authority-envelope diffs;
- AI assistance;
- the Forma designer;
- per-record L2 lineage tables beyond Execution history;
- generic matching;
- file-backed staging.

Revisit when Unbound enables migration (REQ-X-061) or a second application files an ingestion requirement.
