# Adversarial review E: the owner-directed minimal pipeline phase 1

Reviewer stance: independent and adversarial. The owner directive is **fixed scope**. This review asks what the smallest compliant design is, what blocks it, what it costs, and which conflicts remain. It does not reopen whether to build the pipeline. All repositories were read only, on 2026-11-26. Effort figures are theoretical and nothing was measured. Paths are relative to `` unless stated.

## 0. Headline

- **A compliant phase 1 is feasible as a linear, fixed-order pipeline.** It needs 9 stage kinds (down from 16), no expression language, about 13 operations (down from 55), 5 code packages and 4 mapping packages.
- **Phase 1 cannot finish inside Transitus.** Four of its required outcomes depend on work that is not yet defined or decided:
  1. **Authorized domain API load.** Unbound has no domain API.
  2. **Canonical historical migration.** No "Unbound canonical import shape" exists in any Unbound record.
  3. **Migration rehearsal.** It needs a disposable sponsor cell, which Unbound has not specified.
  4. **Schwab format.** No Schwab file specification is in evidence. Unbound itself warns against assuming one exists.
- **Realistic Transitus effort is about 15–24 engineer-weeks.** That is 3–4× the 4–6-week three-library estimate and about 2× the original 6–10-week phase-1 figure. Another **6–12 engineer-weeks** falls on Unbound and Echelon.Execution and is a precondition.

---

## 1. Smallest design that satisfies every element of the directive

### 1.1 The directive decomposed, with the minimal mechanism for each

| Directive element | Minimal compliant mechanism | What can be cut while still complying |
|---|---|---|
| Declarative typed pipeline | An F# DU value with a fixed **linear** stage order, serialized to canonical JSON (JCS) only for hashing, versioning and storage. | DAG, `dependsOn`, `route`, `union`, `runIf`, YAML, a published JSON Schema for hand authoring, sub-pipelines, and TEL (PS-005, PS-007, PS-009, PS-010 stay in phase 2). |
| Ingest | A `ingest` kind over a host-supplied transport: HTTPS for IRS, SFTP or file drop for bank and custodian, an upload handle for migration. | `discover` (the host passes the object list), polling and CDC. |
| Immutable raw evidence | A `preserve` kind using `Transitus.Evidence` RawEvidence aligned to UNB-KNOW-023 (UNB-TRN-002). `IBlobStore` port with the PostgreSQL default only. | The S3 adapter (ST-007, optional half). |
| Isolated temporary staging | **One** fixed-DDL staging table per sponsor schema: `(execution_id, stage_id, dataset_id, ordinal, natural_key, row_hash, payload bytea)`. Created by a Strata migration at deploy time, so there is no runtime DDL. Purged per an approved policy id. | Per-dataset typed tables, UNLOGGED tables (so ST-009 is moot), file-backed staging (ST-008), preview and inspection APIs. |
| Deterministic mapping/transformation | `parse` and `transform` kinds. A mapping is a field map plus a **closed** operation list of about 13 operations (§1.3), with no expressions. | `when@1`, `Case`, `Arith`, `math.eval`, `join`, `aggregate`, `match`, `filter`, privacy ops except HMAC, `address`/`name` ops, and the TX-011 set operators except snapshot-diff and dedupe. |
| Validation | A `validate` kind using the `Transitus.Checks` primitives. Cross-field checks use a closed `Compare(field, op, field \| literal)` form instead of TEL (`06-validation-and-reconciliation.md:36` currently binds `v.crossField` to TEL). | `v.distribution`, `v.freshness` (the host handles freshness), `v.sequence` except where the bank format needs it. |
| Reconciliation | A `reconcile` kind: `r.count`, `r.controlTotal`, `r.balance`, `r.matchSets`, `r.crossSystem` (`06:48-54`). | `r.timing` (VR-012), `r.crossFile` unless the custodian supplies positions and transactions as separate files, and `r.hashTotal` (needed only for NACHA, which is not a demo scenario). |
| Authorized domain API load | `authorize`, then `load` through a **host-registered destination port**. The approval binds to the sealed plan hash (ST-005). Each record becomes one Echelon.Execution command carrying the EX-006 key. | Batching after go-live (A8 withdrawn), the generic HTTP destination, outbound file destinations. |
| Post-load verification | A `verify` kind: read-back through the destination port, then `r.matchSets` and `r.crossSystem` over plan, receipts and read-back (VR-010). | Sampling. Financial pipelines verify 100%; sampling is an optimization, not a phase-1 need. |
| Versioned reusable basic mapping packages | MP-001 manifest (`schemas/mapping-package.schema.json`) plus a loader, content hash, semver and format detectors. Three to four packages (§3.2). | Overlays (MP-003; no customer yet), promotion (MP-005), upgrade-diff tooling beyond "re-run fixtures and diff" (MP-004 narrowed), and vendor packages. |
| Checkpoints | **Stage-granularity** checkpoints. Each stage's output is a sealed dataset, and resume restarts at the first unsealed stage. Ordinal-skip within the load stage comes from per-record idempotency keys. File-set checkpoints apply to the daily custodian and bank feeds (AD-004). | Chunk-parallel execution, chunk-level checkpoints inside pure stages, and backpressure via pause scope (`05-execution-model.md:115-117`). |
| Replay / idempotency | Replay of a manifest (pipeline hash, package hashes, reference versions, raw hash) that reproduces staged hashes and the original keys (SEC-016, AI-005 renamed). | Replay of an exception subset (`replayExceptions`). Defer it and require a full re-run. |
| Dry run | Run through `reconcile`, emit the `LoadPlan`, and mark the evidence `dry-run`. Nothing is written to any system of record (EX-004). | Destination `validateOnly` mode. |
| Reuse Formats/Checks/Evidence and Echelon.Execution | The engine is a **pure state machine** plus an `IDurableCommands` port. The Unbound host binds the port to the in-place Echelon.Execution. | Any Transitus reference to the Echelon.Execution assembly (see §2.2 and C6). |
| Financial correctness and tenant isolation blocking | Mandatory `preserve`, `validate`, `reconcile`, `authorize`, `verify` and evidence for system-of-record destinations (PS-003). Zero monetary tolerance (VR-003), the conservation law (VR-007), no balancing entries (VR-009). Negative isolation tests on every Transitus-owned table. | Nothing. These are blocking by directive. |
| Defer complex DAGs, advanced AI, visual editing | Already deferred (T3, T4). | — |

### 1.2 Stage kinds actually needed (of the 16 in `schemas/pipeline.schema.json:136`)

| Kind | IRS EO BMF | Bank (BAI2 or camt.053) | Custodian (Schwab) | Canonical migration | Keep? |
|---|---|---|---|---|---|
| discover | host | host | host | — | **cut** |
| ingest | ✓ | ✓ | ✓ | ✓ | keep |
| preserve | ✓ | ✓ | ✓ | ✓ | keep |
| parse | ✓ | ✓ | ✓ | ✓ | keep |
| stage | implicit | implicit | implicit | implicit | **cut as a kind.** Staging is a property of every stage boundary. |
| profile | — | — | — | useful, not required | **cut** |
| transform | ✓ (snapshot diff, code maps) | ✓ (type code to direction) | ✓ | ✓ (EIN lookup, imported_unverified) | keep |
| route / union | — | — | — | — | **cut** |
| validate | ✓ | ✓ | ✓ | ✓ | keep |
| reconcile | count vs previous run | ✓ control totals (BAI2 49/98/99 or camt OPBD/CLBD) | ✓ balance | ✓ per-fund balance | keep |
| authorize | auto-approve policy | ✓ | ✓ | ✓ human | keep |
| load | ✓ | ✓ | ✓ | ✓ | keep |
| verify | ✓ | ✓ | ✓ | ✓ | keep |
| evidence | emitted by the runtime | | | | **cut as a kind.** The engine emits evidence automatically; it cannot be omitted. |
| retain | — | — | — | — | **cut as a kind.** A host sweeper command applies the approved policy. |

That leaves **9 kinds**: ingest, preserve, parse, transform, validate, reconcile, authorize, load, verify. A linear order makes the DAG checks in `01-lifecycle…md:169` trivial, and the definition validator shrinks to: mandatory-stage presence, type checking of mappings against package schemas, and the classification ≤ destination check.

### 1.3 Operations needed (of the 55 in `04-transformation-library.md` §3)

These are needed across the three demo scenarios: `text.trim`, `text.case` (invariant), `field.require`, `field.default` (constants such as `imported_unverified`, with `acknowledgeDefault` on financial fields), `number.parse`, `money.parse` (needs an **implied-decimal** parameter for BAI2 amounts, which the catalogue lacks), `date.parse`, `enum.map`, `id.normalize` (needs a **CUSIP** kind for custodian securities, which is missing from `04:142`), `lookup` against a pinned reference set (EIN resolution against BMF for migration, TX-007), `dedupe` (reject-all only), snapshot-diff by natural key (AD-009), and `privacy.hash` HMAC only (TX-010). That is **13 operations**, consistent with adv-D's "likely about 15" (`adv-D.md:105`).

TEL is **not needed**. BAI2 debit/credit direction comes from the type-code range, which is an `enum.map` or a parser output. Conditional mapping for migration status codes is an `enum.map`.

### 1.4 Code packages (maintenance budget, ARC-007)

`Transitus.Formats`, `Transitus.Core` (Checks + Evidence + the 13 Transforms, all pure), `Transitus.Model` (DU, canonical JSON, definition validator, package manifest), `Transitus.Engine` (state machine + ports), and `Transitus.Postgres` (raw store, staging, evidence chain DDL as Strata-governed SQL). That is **5 code packages**, against 3 in the reviewed plan and 12 originally. Merging Checks and Evidence into Core is optional; keeping them separate makes 7.

---

## 2. Feasibility risks and blockers

### 2.1 Unbound has no domain API (blocker)

- adv-D found no domain API, OpenAPI or ledger in `unbound` (`transitus/docs/reviews/agent-reviews/adv-D.md:9`). Echelon.Execution lists "HTTP intake layer, status endpoint" as not implemented (`unbound/execution/README.md:73`).
- UNB-TRN-005 (`unbound/requirements/discovery/2026-11-26-transitus-integration/02-REQUIREMENTS.md:78-94`) asks Unbound to define the ingestion operations, each with natural key, idempotency, read-back and class. It is still `proposed · not implemented`.
- **Consequence.** `load` and `verify` can only be built against a port with fakes. "Authorized domain API load" cannot be demonstrated end to end until Unbound defines at least these operations:
  - charity registry observation;
  - bank activity recording;
  - custodian transaction and position recording;
  - historical import (UNB-TRN-006, still marked conditional at `02-REQUIREMENTS.md:112`).
- The read-back query is what `verify` needs. If Unbound defines operations without read-back, VR-010 fails.

### 2.2 Echelon.Execution gaps (`unbound/execution/README.md`)

| Gap | Evidence | Impact on this phase 1 | Workaround or owner |
|---|---|---|---|
| Unbenchmarked | `:7`, `:80-81` (RM-05 must benchmark first) | PF-001 cannot be met. Load-rate figures stay theoretical (A7 300–800/s idle, 100–250/s live, `12-performance…md:29`). | Echelon.Execution owner: RM-05 |
| No lease renewal | `:71` | A stage-level command over about 2M BMF rows must finish within the lease. | Bound handler time per stage, or chunk the transform stages. That re-introduces chunk checkpoints. |
| Dependency resume partial | `:69` | Fan-in from N per-record load commands to `verify` has no automatic resume. | Outbox counter: "last receipt enqueues verify" (`05:64`). Must be tested against at-least-once relay (EAR-CMD-008). |
| Payload purge not implemented | `:70` | EX-013 limits payloads to references. Migration loads still leave 1.5–3 KB per record of history (A12, `12:31`) with no purge, which conflicts with the "retention by approved policy" directive. | Echelon.Execution owner (EAR-CMD-022) |
| Metrics not implemented | `:72` (blocked on U-07) | A pipeline engine in production with no throughput or lag signal. | See C9 (GAP-05) |
| Tenant isolation partial | `:67`. The command store is one `{schema}` with `tenant_id` (`src/Echelon.Execution.Postgres/Schema.sql:1-5`), not schema-per-sponsor. | Transitus commands for all sponsors share one store. That is acceptable only if CNV-ARC-001's "RLS on every tenant table" is satisfied or waived for it. | Unbound architecture |
| Distinct DB roles not implemented | `:68` (EAR-SEC-002) | Weakens AD-008 ("no credentials to business tables"). | Deployment grants |
| Queue-limit check runs before duplicate lookup | `:77-79`; `04-DECISIONS…md:28` | During a bulk migration, idempotent retries are throttled. Replay behaviour therefore differs under load. | Fix in the module |
| No quota share or separate worker role | Only a per-command `Priority` int exists (`Types.fs:90`, `Policy.fs:74-81`). | AD-011 and UNB-TRN-007 (P0, initial-implementation) need a quota share and an operation-filtered worker. | New Echelon.Execution feature |

"Defer extraction" and "independent repo" are compatible **only** if Transitus never references the Echelon.Execution assembly. Unbound has no licence (DRF-09, `echelon-registry/portfolio/analysis/duplication-and-drift.md:82`), and Transitus is MIT. A source copy would also violate ARC-006, and a NuGet package published from Unbound would be extraction in all but name. The port approach (§1.1) creates a **second contract**, `IDurableCommands`. That contract is the obvious candidate for the directive's "shared contract stable" criterion.

### 2.3 Staging under CNV-ARC-001 with Strata-governed DDL

- CNV-ARC-001 (`unbound/requirements/baseline/baseline.jsonl:1619`; `PLATFORM-UX-API-AND-ASSURANCE-STANDARDS.md:257`) requires a schema and role per sponsor, and **row-level security on every tenant table**.
- PostgreSQL does not support `COPY FROM` into RLS tables. TRN-ARCH-02 already concedes this (`02-storage-architecture.md:72`). Its own workaround, a non-RLS load table or "schema isolation instead of RLS" (`02:79`), **contradicts the literal clause**. Batched `INSERT` keeps RLS but loses COPY throughput (A5 is unmeasured anyway).
- Strata is a pilot (`kemiller2002/strata/README.md:15-20`). Its README documents a single-schema project layout. This reviewer found no documented feature for deploying the same table set into N sponsor schemas (the only tenant reference is `policies/customer_tenant.sql`, `:350`). DEP-STRATA-01 (`11-echelon-dependency-analysis.md:97`) is unfiled. Echelon.Execution works around this with a `{schema}` placeholder (`Schema.sql:1`), which is not a Strata feature.
- **Shared BMF staging** (ST-010, `02:82`) is a cross-tenant store. CNV-TEN-001 (`baseline.jsonl:1643`) requires it to appear in a SharedStoreRegister with fields, writers, readers and inference risks. No entry exists.
- Migration staging holds donor PII, which is restricted-personal. CNV-ARC-001 requires event payloads to reference a PII vault. Staging copies survive in WAL and backups beyond any TTL unless crypto-shredding (SEC-018, phase 2) is pulled into phase 1, or the approved policy accepts the backup window as the effective retention.
- WAL from staging passes through the synchronous standby (`02:74`). Migration rehearsal on the **shared cluster** loads other sponsors' commit path, so PF-002 (phase 2, P0) is needed in phase 1.

### 2.4 Schwab file specification: not in evidence

- Unbound states: "Charles Schwab is a reference integration target, not a claim of an available, public, approved or contracted Schwab API" (`unbound/requirements/integrations/CUSTODIAN-AND-INVESTMENT-MANAGEMENT.md:5`). It then lists a discovery checklist: business channel, entitlement, contract permissions, test environment (`:57-58`) and "which Schwab institutional product … is in scope?" (`:75`).
- The **only** public Schwab feed evidence in the portfolio is a third party (BridgeFT) passing through Schwab *registration codes* (DASCG, DASPL, DASPI, CHGFT) (`daf-landscape/research/mission-2026-11-14/queue-batch36-anonymity-feeds-fees.md:41,113`). That is code-table evidence, not a file layout. Schwab's own sites were not fetched (403 robots, `:7`). daf-landscape's Schwab Online Services Agreement notes concern credentials and aggregators (`:46,217,220`), not file formats.
- To this reviewer's understanding, Schwab's institutional and advisor data-feed layouts are made available to advisors and approved vendors under agreement, not published openly. This could not be verified from the evidence repos and is **not** asserted as fact.
- **Implications.**
  - "Prioritize Schwab documented custodian format" cannot start until a licensed specification is in hand, under a contract that permits building, and preferably publishing, a mapping package (MP-002).
  - If the specification is confidential, the `custodian.schwab` package cannot live in an MIT public repository. It must be a private package, which conflicts with OQ-12.
  - Until then, the custodian demo can only use `basis: synthetic-representation`, which MP-002 forbids presenting as a vendor schema.

### 2.5 NACHA redistribution rights

- No licence analysis exists in any evidence repo. Unbound cites nacha.org rules pages for risk topics only (`unbound/requirements/discovery/2026-11-23-cross-industry/data/findings.csv:2`).
- OQ-16 (`transitus/docs/open-questions.md:33`) marks this "no" owner, and TRN-ARCH-09 says "layouts widely published" (`09-mapping-packages.md:68`). Neither is a rights basis.
- The Nacha Operating Rules are a sold, copyrighted publication. Nacha also runs a public developer guide; whether its terms permit redistributing layouts in an MIT package was not checked.
- NACHA is **not** among the three demo scenarios, but CNV-PAY-005 needs returns and NOC in R1 (`adv-D.md:17`). The directive's "verify NACHA redistribution rights" is therefore on phase 1's critical path even though the demo omits it.
- The same question applies to BAI2. The specification is published by BAI, and successor BTRS is an X9 standard. camt.053 XSDs from ISO 20022 are freely available, but each bank's implementation guide is bank-specific. With no bank partner (OD-M-14), the bank package can only be built against the public base standard.

### 2.6 Migration rehearsal requirements in Unbound

- **RR-REQ-X-061-r1** (`baseline.jsonl:1219`, status adopted) requires:
  - a 10-state MigrationRun: Contracted > Inventoried > Mapped > **ImportedToStaging** > **Reconciled** > **ParallelValidated** > CutoverAuthorized > SingleWriterActive > PostCutoverVerified > Archived;
  - per-record source system, source record id, import batch and `verification_status=imported_unverified`;
  - no payment to imported_unverified destinations;
  - a legacy-writer fence before posting;
  - a declared rollback boundary.
- **UNB-RCN-WF-020** (P0, `ENTERPRISE-GAP-REGISTER-AND-CROSS-DOMAIN-SCENARIOS.md:250-255`): if the fence outcome is unknown, there is no posting, and a run may be abandoned before cutover "with staging evidence retained".
- **CNV-EXP-002** (`baseline.jsonl:1640`, `initial-implementation`, owner-ratified) requires a full fund history, including **acknowledgments and documents**, with a reconciliation report.
- **Rehearsal is not a dry run.**
  - A dry run stops at the `LoadPlan`, so it never exercises domain operations, read-back or per-fund balances in the target.
  - A real rehearsal loads into a target that must then be thrown away. EX-009 forbids automatic compensation, and loaded financial records cannot be "un-loaded".
  - Rehearsal therefore needs Unbound to provision a **disposable rehearsal sponsor cell** (schema and role), using the per-tenant migration machinery of CNV-ARC-005 (`baseline.jsonl:1651`), and to delete it with evidence afterwards. Nothing in the Unbound records specifies this.
- **Documents.** The Transitus value model treats `Binary` as "not transformable except hash/tokenize" (`04-transformation-library.md:92`). Migrating documents means passing blobs through to an Unbound document store, which needs an Unbound document-import operation.
- **"Canonical import shape" does not exist.** It appears only in Transitus (`roadmap.md:48`; MP-006). `grep` across `unbound/requirements` and `unbound/architecture` finds nothing.
  - `daf.grant-record` v0.1 is an Echelon draft and covers grants only (`09:72`).
  - Contributions, acknowledgments, fund balances, advisors, successors and payees have no canonical shape.
  - With no design partner (OD-M-14) there is no predecessor export, so the "canonical historical migration" demo is a **target-side** package fed by synthetic data. The predecessor-to-canonical mapping stays per customer.

### 2.7 Tenant isolation

TRN-REQ-SEC-011 (P0) must hold across:
- raw store;
- staging;
- the evidence chain (LN-006 per tenant);
- the exception store;
- reference sets (BMF is shared, see 2.3);
- the durable command store (2.2, partial);
- HMAC keys (TX-010 is P0 but **phase 2**, and phase 1 migration needs it).

CNV-ARC-001 requires **negative isolation tests**. No Transitus requirement mandates them; SEC-011's acceptance criterion is unstated.

### 2.8 Retention: invented durations already in the docs

The directive says "no invented durations". The proposal contains:
- P7Y, P30D, P2Y in the pipeline example (`01-lifecycle…md:112,124`);
- staging default P30D and max P180D (`02:93`);
- P2Y and P7Y store defaults (`02:127-130`);
- P7Y in the economics model (`12:58,86`).

On the Unbound side, only OFAC's 10 years is established by authority: 31 CFR 501.601, RCD-007 (`unbound/requirements/convergence/2026-11-24-master/02-EVIDENCE-DOSSIERS.md:4212`; `03-AUTHORITATIVE-BASELINE-AND-CONVERGENCE.md:58`). The 7-year floor is a **policy** awaiting sponsor-owner decision. Retention must therefore be a reference to an approved policy class id, with no Transitus defaults.

---

## 3. Effort estimate (theoretical)

**Assumptions:**
- one experienced F# engineer, agent-assisted, with the portfolio's review overhead;
- no measurements;
- Unbound domain operations are defined in time for integration, and only a fake port is used before then;
- a Schwab specification and one bank format are in hand by mid-phase;
- logged staging only;
- no chunk parallelism.

### 3.1 Transitus work

| Item | Engineer-weeks |
|---|---|
| Formats: IRS port (BMF, Pub 78, auto-revocation, OFAC) + fuzzing | 1–1.5 |
| Formats: one bank (BAI2 or camt.053) | 1–1.5 |
| Formats: Schwab custodian (depends on the specification) | 0.5–1.5 |
| Formats: canonical-history reader (multi-entity CSV; documents pass-through) | 0.5–1 |
| Formats: NACHA returns and NOC (R1-required, not a demo scenario) | 0.5–1 |
| Core: Checks + Evidence (raw evidence, keys, L0–L1 lineage, hash chain) | 2–3 |
| Core: 13 operations with conformance and property tests | 1–1.5 |
| Model: DU, JCS hashing, definition validator, package manifest and loader | 2–3 |
| Engine: state machine (Blocked, PartiallyLoaded, OutcomeUnknown), stage checkpoints, dry run, replay, approval wait, load fan-out and fan-in workaround, verify | 3–4.5 |
| Postgres: raw store, staging table, evidence chain DDL via Strata; purge by policy; negative isolation tests | 1.5–2.5 |
| 4 mapping packages with fixtures and detectors | 1.5–2.5 |
| Abuse corpus, determinism suite, PF-001 benchmark harness | 1–1.5 |
| **Total** | **≈15–24** (bottom-up sum 15.5–25.5, rounded) |

### 3.2 Comparison with earlier estimates

| Estimate | Engineer-weeks |
|---|---|
| Three libraries (`roadmap.md:30`) | 4–6 |
| Original phase-1 estimate (`adv-D.md:79`) | 6–10 |
| Old phase 2 engine, DAG and full catalogue (`roadmap.md:73`) | 8–12 |
| Hand-written per-feed baseline (`12:118`) | 3–4 |
| **This phase 1** | **15–24**, roughly old phase 1 + 70% of old phase 2 + part of phase 3 |

### 3.3 Not in that figure (precondition work outside Transitus, 6–12 engineer-weeks)

- Unbound domain operations with read-back for the four destinations;
- MigrationRun state machine, rehearsal cell provisioning and teardown, and the canonical shape definition;
- Echelon.Execution G2 resume, G3 purge, quota share and worker role (AD-011), the queue-limit fix, and the RM-05 benchmark.

### 3.4 Maintenance obligation

- 5 code packages;
- 4 mapping packages (`irs.eo-bmf`, with Pub 78 and revocation as profiles or 2 more packages; `bank.<bai2|camt053>`; `custodian.schwab` (private if the specification is confidential); `unbound.canonical-history`, target-side);
- `nacha.ach` if rights permit;
- 13 operations, about 12 primitives;
- 1–2 third-party parsers (a CSV library; BCL XML for camt.053);
- 2 cross-repository contracts (`IDurableCommands`; the domain destination port).

That is about 2× the three-library budget, and a fraction of the original 12 packages, 55 operations and 18 mapping packages (`adv-D.md:63-73`). Ongoing work is in the 0.1–0.2 FTE band (`12:128`), at its upper end because format versions drift: BMF layout changes, bank specification versions, Schwab specification updates.

---

## 4. Unresolved conflicts and who must resolve them

| # | Conflict | Evidence | Resolver |
|---|---|---|---|
| C1 | The directive supersedes the TRN-REV-01 outcome (three libraries, kill criterion), triggers T2/T3, ARC-009 ("absent the trigger, MUST NOT be built"), and DF-TRN-2026-0016. | `adversarial-review.md:44-58`; `roadmap.md:134-156`; REQUIREMENTS ARC-009 | **Transitus owner.** A new decision record superseding DF-0016; amend ARC-009 and the roadmap. |
| C2 | PF-004 becomes a post-hoc measurement. The kill criterion can no longer prevent the engine from being built, only retire or fold it. | `roadmap.md:181-182` | **Transitus owner.** Restate PF-004 as a retire/fold criterion with a date. |
| C3 | Migration in R1 (directive, CNV-EXP-002) against Unbound records that still defer it: UNB-XIN-OTH-002 "no migration in R1" (`17-RELEASE-1-SCOPE.md:108`); simplification matrix "defer" for RR-REQ-X-061-r1 and UNB-RCN-WF-020 (`02-REQUIREMENT-SIMPLIFICATION-MATRIX.md:1731,1750`); UNB-TRN-006/011 "conditional". | as cited | **Unbound owner.** Record the decision in Unbound owner-decisions, re-scope the matrix rows, and close OQ-13 and TRN-Q-1. |
| C4 | No design partner (OD-M-14), so no predecessor export, and the canonical shape is undefined. | `adv-D.md:11`; §2.6 | **Unbound owner and domain owner.** Define the canonical history shape (entities beyond grants) and its acceptance tests. |
| C5 | CNV-ARC-001 "RLS on every tenant table" against COPY-based staging. | `baseline.jsonl:1619`; `02:72,79` | **Unbound architecture owner.** Either accept INSERT-only staging or grant a documented exception. |
| C6 | Independent Transitus repo vs. deferred extraction of Echelon.Execution, which has no licence in Unbound. | `11:96`; DRF-09 | **Transitus and Unbound owners.** Adopt the port approach; define "shared contract stable" as an exit criterion. |
| C7 | Execution gaps (G1–G4, quota share, EAR-SEC-002, queue-limit bug) and the missing RM-05 benchmark. | §2.2 | **Echelon.Execution owner (Unbound)** |
| C8 | Licensing: Transitus MIT vs portfolio PolyForm (DRF-09, OD-GOV-018 open). Porting unlicensed Unbound.Replay code into MIT. A Schwab specification under NDA cannot go in a public MIT package. NACHA rights. | `open-decisions.md:33`; `open-questions.md:29,33` | **Portfolio owner (OD-GOV-018).** Schwab and NACHA additionally need counsel or contract review. |
| C9 | Observability: GAP-05 is unowned; Execution metrics are blocked on U-07. A production pipeline engine has no monitoring owner. | `open-decisions.md:39` (OD-GOV-024); `execution/README.md:72` | **Portfolio owner (OD-GOV-024)**, and the Unbound owner for U-07 |
| C10 | Retention: the Transitus docs carry invented durations, and the Unbound catalogue (RCD-007) is only partly established. | §2.8 | **Unbound owner, sponsor owners, counsel.** Transitus removes its defaults. |
| C11 | "Schwab documented format" vs Unbound's own statement that no Schwab API or format is assumed. | `CUSTODIAN-AND-INVESTMENT-MANAGEMENT.md:5,58,75` | **Unbound owner.** Name the Schwab channel and obtain a licensed specification. |
| C12 | Bank format "from first partner", but no bank or ODFI partner exists (readiness failure, `adv-D.md:129`). | OQ-06 | **Unbound owner.** Until then, build against the public base standard only and do not claim conformance to any bank. |
| C13 | Rehearsal needs a disposable sponsor cell. EX-009 forbids automatic compensation. Rehearsal on the shared cluster affects live sponsors (PF-002 is phase 2). | §2.3, §2.6 | **Unbound architecture owner** |
| C14 | Shared BMF staging vs the CNV-TEN-001 SharedStoreRegister. | `baseline.jsonl:1643`; ST-010 | **Unbound architecture owner** |
| C15 | Documents and acknowledgments in CNV-EXP-002 vs a Transitus value model with no binary transform path. | `04:92` | **Unbound and Transitus owners** (a scope decision) |
| C16 | The registry already lists Transitus as active against four initiatives before any code exists. | `adv-D.md:80` | **Portfolio owner** (DEP-REG-01) |

---

## 5. Requirement-level recommendations

### 5.1 Re-phase to phase 1, narrowed where stated

| ID | Change |
|---|---|
| PS-001 | Phase 1, P0. Linear typed pipeline: F# DU plus JCS canonical JSON and hash. No YAML. |
| PS-002 | Phase 1. Stages declare kind, outputs, failure behaviour and provenance. Order is fixed and linear. `dependsOn` is deferred. |
| PS-003 | Phase 1, P0. Mandatory stages for system-of-record destinations. |
| PS-004 | Phase 1, P0. Immutable published versions. Separation of duties for restricted-financial. |
| PS-006 | Phase 1. |
| PS-008 | Phase 1, P0, narrowed to the semantic-critical diff: idempotency-key fields, auto-approve conditions, code maps, money and date field re-mapping, reference versions. |
| ST-003 | Phase 1, P0. Fixed DDL per sponsor schema via Strata. Add an acceptance criterion that conforms to the C5 resolution. |
| ST-005 | Phase 1, P0. Approval binds to the plan hash. |
| ST-006 | Phase 1, P0. |
| ST-007 | Phase 1, PostgreSQL default only. |
| SEC-010, SEC-013 | Phase 1. |
| TX-001, TX-004, TX-007 | Phase 1. |
| TX-010 | Phase 1, P0. |
| TX-009 | Phase 1, limited to the 13 enumerated operations. Every other operation needs a consumer pipeline that uses it. |
| AD-004 | Phase 1, file-set checkpoints. |
| AD-007 | Phase 1, P0. |
| AD-009 | Phase 1, for BMF. |
| EX-001 | Phase 1, via a port. |
| EX-002 | Phase 1, P0. |
| EX-003 | Phase 1, narrowed to manual, dry-run and replay. The host schedules. |
| EX-004 | Phase 1, P0. |
| EX-005 | Phase 1, narrowed to stage-granularity checkpoints. Chunk parallelism stays in phase 2. |
| EX-009, EX-010, EX-011 | Phase 1. |
| VR-005 | Phase 1 as "**no overrides in phase 1**". Simpler and stricter. |
| VR-008, VR-011 | Phase 1. |
| LN-002 | Phase 1, static field lineage, which is cheap when the pipeline is linear. |
| LN-005, LN-007, LN-010 | Phase 1. |
| SEC-012 and SEC-018 | Phase 1 for migration staging, or replace with an approved-policy statement of the effective backup retention. |
| MP-001, MP-002 | Phase 1, P0. MP-002 is the rights gate for Schwab, NACHA and BAI2. |
| MP-004 | Phase 1, narrowed to detectors plus fixture diff. |
| MP-006 | Phase 1, P0. |
| MP-007 | Phase 1, measurement only. |
| PF-002 | Phase 1, P0. |
| UI-010 | Phase 1. |

### 5.2 Keep in phase 2 or later

- PS-005, PS-007 (TEL), PS-009, PS-010
- TX-008, TX-011 (except the snapshot-diff and dedupe subset)
- ST-008, ST-009, ST-010 (unless C14 is resolved)
- VR-012, EX-012
- MP-003, MP-005
- the AI-* requirements, UI-001..004, LN-004, LN-009

### 5.3 Amend

- **ARC-007.** Budget: 5 code packages, ≤4 mapping packages plus `nacha.ach` if rights are cleared, 13 operations, ≤2 third-party parsers, 2 cross-repository ports.
- **ARC-008.** Allow tracing to CNV-EXP-002 and RR-REQ-X-061-r1, but only **after** C3 is recorded in Unbound.
- **ARC-009.** Redefine T2 as "DAG, route and union, TEL, chunk parallelism, scheduling". Basic mapping packages are no longer gated on T3. Vendor packages stay gated on MP-002 clearance.
- **PF-004.** Restate as a retire-or-fold criterion with a date and named metrics: effort per feed, defect escape, change lead time.
- **OQ-16.** Becomes an owner-gated phase-1 blocker for publishing `nacha.ach`, extended to BAI2/BTRS and Schwab.
- **Documentation.** Delete every literal retention duration (`01:112,124`; `02:93,127-130`; `12:58,86`).

### 5.4 Add

| ID | Phase / P | Requirement |
|---|---|---|
| TRN-REQ-PS-011 | 1 / P0 | Phase-1 mappings and checks MUST use a closed vocabulary (field map, enumerated operations, `Compare(field, op, field\|literal)`) with no expression language. |
| TRN-REQ-ST-011 | 1 / P0 | Every retention setting MUST reference an approved policy class identifier owned by the consumer. Transitus MUST ship no default durations. |
| TRN-REQ-ARC-010 | 1 / P0 | The engine MUST depend only on an `IDurableCommands` port and a destination port. It MUST NOT reference the Echelon.Execution assembly. A stable port contract is the precondition for extraction. |
| TRN-REQ-SEC-020 | 1 / P0 | Negative tenant-isolation tests MUST cover raw, staging, exceptions, evidence chain, reference sets, HMAC keys and the command port (CNV-ARC-001). |
| TRN-REQ-MIG-001 | 1 / P0 | Migration rehearsal MUST load only into an isolated, disposable sponsor cell provided by the host. It MUST be repeatable from preserved raw input with identical keys, and it MUST produce a conservation table and per-fund balance reconciliation (UNB-TRN-011). |
| TRN-REQ-MIG-002 | 1 / P0 | The canonical-history package MUST stamp source system, source record id, import batch and `imported_unverified` on every standing-data record (RR-REQ-X-061-r1). |
| TRN-REQ-MIG-003 | 1 / P0 | Transitus executions MUST NOT change MigrationRun state. They supply evidence for Reconciled and ParallelValidated, and a load MUST be refused while the host reports the fence as Unknown (UNB-RCN-WF-020). |
| TRN-REQ-MIG-004 | 1 / P1 | Documents MUST be preserved as RawEvidence and handed to a host document-import operation unchanged, with hash verification on read-back. |
| TRN-REQ-OBS-001 | 1 / P0 | Run state, stage durations, exception counts and OutcomeUnknown obligations MUST be emitted as OpenTelemetry through the host until GAP-05 has an owner. |
| TRN-REQ-PF-005 | 1 / P0 | Before Unbound go-live, measure: per-record load cost on the RM-05 instance, staging insert rate under RLS, and BMF stage handler time against the lease. |

### 5.5 File in Unbound (proposals; not applied)

- Make UNB-TRN-005 a precondition, with read-back per operation.
- Move UNB-TRN-006 and UNB-TRN-011 to `initial-implementation` once C3 is recorded.
- New: rehearsal sponsor-cell provisioning and teardown with evidence.
- New: a canonical history shape covering contributions, grants, acknowledgments, documents, opening balances, advisors, successors and payees.
- New: a SharedStoreRegister entry for public reference data.
- Echelon.Execution: G2, G3, quota share and worker role, and the queue-limit fix, before migration rehearsal.

## Bottom line

The directive is buildable as a linear, nine-stage, expression-free pipeline. The engine is about 2–3× bigger than the reviewed three-library plan, not 10×. Its critical path is outside Transitus: Unbound domain operations, the canonical shape, the rehearsal cell, the Schwab and bank specifications, and the NACHA and Schwab rights. Start Transitus work on Formats, Core and Model against fakes. Do not start Engine load or verify integration until UNB-TRN-005 exists, and do not publish any Schwab or NACHA package until C8 and C11 are cleared.
