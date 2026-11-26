# Adversarial review C: Transitus claims C7, C8, C9

Reviewer stance: try to refute; concede where the evidence supports the proposal. Line references are to files as they stand on 2026-11-26. "TRN-ARCH-12 L29" means line 29 of `transitus/docs/architecture/12-performance-and-economics.md`.

---

## C7. Reusable migration mapping packages are practical

### Strongest case against

1. **There is no vendor schema to reuse, and the evidence shows exports are produced on demand, not as stable products.** The Ren iPhi MSA §10.5 promises only that customer content is "made available in industry-standard format for 15 days" after termination. Its scope "may not encompass all platform-generated audit events or approval provenance" (`daf-landscape/research/ren-iphi-platform-contract-architecture-integration-audit-2026-11-12.md` L29). Ren sells "data migration" and "API integration" as paid add-ons (same file L48; `12-incremental-commercial-opportunities.md` L52). An export made by professional services when a customer terminates has no published version. So TRN-ARCH-09 §4's detectors and `accepts: ["2024.*"]` version ranges (L79–82) have nothing stable to detect. A header signature taken from customer A's dump does not show that customer B's dump has the same meaning.
2. **One vendor name hides several systems.** Ren runs at least iPhi CoreEnterprise, DFX/DonorFirstX and the Ren Giving Platform. The audit's hypothesis H1 ("distinct accounting stores, linked via APIs and batch files") is rated plausible (audit L63). The commercial analysis says each incumbent is "a separate data model" (`12-incremental-commercial-opportunities.md` L44). `vendor.ren-iphi` (TRN-ARCH-09 L74) is therefore at least two source packages.
3. **Reuse frequency is very low.** The Ren/iPhi tenant census has 76 rows (`data/mission-2026-11-14/ren-iphi-tenant-census.csv`). Its summary gives annualised attrition of about 2.8% (upper 3.8%) (`ren-iphi-attrition-summary.json`). That is about 2 to 3 sponsor exits a year across the whole industry, before Unbound wins any of them. The historical record is "8 migrations, 6 to Foundant" (`12-*.md` L38). A realistic expectation is that each vendor package is used 0 to 2 times in the first three years. At that rate the package does not pay back the cost of building it, versioning it, generating synthetic fixtures for it and running a disclosure review for each change.
4. **Most of the mapping content is defined by the customer, not the vendor.** The data portability schema in the runbook (`migration-runbook-2026.md` L50–60) lists what really varies: fund types, restriction codes, fee components, pools/NAV, permission roles, successor chains, correction chains. These are set up per sponsor. The runbook's hard cases are the same: pending in-kind gifts, reversed or corrected grants, mapping old grant IDs to new ones, successor rights (L27–41). They are about semantics and state, not columns. TRN-ARCH-09 §5 step 2 asks reviewers to decide whether a rule is "general (true of the vendor format)" or customer-specific. From a single authorized sample that question cannot be answered.
5. **Confidentiality covers more than customer data: vendor licence terms also apply. The proposal does not address this.** iPhi MSA §3.4 "forbids use/view of services to create commercially competitive product, in addition to reverse-engineering" (audit L21). Suppose Echelon takes structural knowledge from customer A's export, promotes it into a base package (TRN-ARCH-09 L90–106), and sells it as part of a $25–75k migration offering (TRN-ARCH-12 L94–96). That exposes customer A (the licensee) and Echelon to a breach or trade-secret claim. TRN-REQ-MP-005 checks only for leaks of *customer values*.
6. **`daf.grant-record` is overstated.** TRN-ARCH-09 L72 calls it "public" and "buildable now". The schema calls itself "Minimal open DAF grant record, v0.1 (draft, unendorsed)" (`standards/daf-grant-record/schema-v0.1.json`). It covers grants only and no vendor emits it. It can be a target, not a reusable source.

### Concessions
TRN-ARCH-09 is careful in several places. It does not invent vendor schemas (L51–58, TRN-REQ-MP-002). It marks vendor packages "placeholder only" (L74). It forbids forks (MP-003). Packages built from public specifications (IRS EO BMF, Pub78, auto-revocation, 990 e-file, NACHA, BAI2/camt.053) really are reusable. The target-side canonical model, validation profiles and reconciliation profiles (fund tie-out, grant state machine, EIN checks, opening-balance tie-out per Unbound UI S-051) are reusable for every migration whatever the source.

### Quantified reuse (reviewer's estimate; not measured)

| Layer | Share of migration effort | Reuse across sponsors |
|---|---|---|
| Public-spec packages (IRS, NACHA, bank) | small | 90–100% |
| Target canonical model + validation/reconciliation profiles + `spreadsheet.admin` template | ~25–35% | 70–90% |
| Vendor source schema/parse templates | ~10% | 30–60% *after* the first authorized sample; 0% before |
| Code-set and semantic mappings (status, fund type, fees, pools, corrections) | ~25–30% | 10–25% |
| Exception resolution, break investigation, opening-balance sign-off | ~30–40% | ~0% (packages do not touch it) |

Net: for a second migration from the same vendor, reusable *vendor-specific* content cuts total effort by about **10–20%**. Reusable *vendor-independent* content (target profiles, public specs) cuts it by about **20–30%** for every migration. The value is in the target side, not in the vendor catalogue.

### Verdict: **partially upheld**
Rejected for the vendor packages (Ren/iPhi, TIFIN Give, GiftingNetwork, DAFtech, CF systems, custodians, payroll). Upheld for public-spec packages and target-side packages.

### Required revisions
- **TRN-REQ-MP-002 (change):** add a `vendor-licence-clearance` field to the provenance of `customer-authorized-sample`, recording the customer's authorization *and* a review of the vendor contract's confidentiality, reverse-engineering and competitive-use terms (Ren iPhi MSA §3.4). Without clearance the package must not be promoted beyond that customer's overlay.
- **TRN-REQ-MP-005 (change):** promotion to a base package requires at least two independent customer samples that agree on the rule. One sample cannot tell vendor-defined codes from customer-configured codes.
- **TRN-REQ-MP-006 (add, P1):** reorder the catalogue so the **Unbound target package** (canonical model, validation and reconciliation profiles, opening-balance tie-out, old-ID→new-ID cross-reference per runbook M10) is the primary reusable asset. Vendor packages become per-engagement overlays until a reuse count of at least 2 is recorded.
- **TRN-REQ-MP-007 (add, P1):** a package reuse metric (engagements per package version, share of mapping rules inherited versus overridden). It must be reported before any commercial claim that packages reduce migration cost.
- **TRN-REQ-MP-004 (change):** detectors must report `unknown-provenance` when an export has no vendor version identifier. A header match alone must never produce `compatible`.
- Fix TRN-ARCH-09 L72: `daf.grant-record` basis is "Echelon draft (unendorsed)", target-only.

---

## C8. Lineage does not create excessive storage or performance overhead

### Arithmetic check
I recomputed every row of TRN-ARCH-12 §2 (L37–42) from A1–A11. Raw, peak staging (3 × N × 600 B), L2 (N × 300 B), core time (N/400k + 3N/50k + N/30k), unbatched load (N/1,000), batched load (N/20,000) and WAL (1.5 × staging) all reproduce within rounding. Memory (80 MB), the 47 MB/s database write rate at 10⁷ records, BMF raw retention (600 MB/week, about 31 GB/yr, 4–6 GB compressed) and peak staging for 5M records (9 GB) are also correct.

**Errors found:**
1. **TRN-ARCH-12 L85 (lineage per year) is wrong at the low end.** The custodian feed alone is 50k × 250 business days × 300 B = **3.75 GB/yr**. BMF diffs at 5% are 100k × 52 × 300 B = 1.56 GB/yr. Together that is **≈5.3 GB/yr**, not "1.5–5 GB/year". The expression "2M × 52 changed-subset" is also garbled.
2. **A9 (300 B) is the most optimistic end of TRN-ARCH-08's own range.** TRN-ARCH-08 L20 gives 300–400 MB per 10⁶ records *with one index*. Lineage must be queryable by destination id, by execution and by source natural key, so at least two or three indexes are needed. If hashes and keys are stored as text (64-character hex hash, 52-character base32 idempotency key, 36-character UUIDs), **400–600 B/record** is more realistic. That gives 7–11 GB/yr, or 50–75 GB held at a 7-year steady state.
3. **Unmodelled: the Echelon.Execution command store becomes the real per-record lineage.** With one command per record, each record also writes:
   - a `command` row whose `payload text NOT NULL` holds the full record (`execution/src/Echelon.Execution.Postgres/Schema.sql` L14), with the 4-column text unique index `command_identity` (L32);
   - 2–3 `command_history` rows (Insert L144 plus history; claim history `PostgresStore.fs` ~L497–508; completion);
   - an `outbox` row (Schema L54–63).

   I estimate **1.5–3 KB per record**, which is 5–10× the L2 figure. That is about 27–53 GB/yr for the §4 scenario. Purging it is listed as **not implemented** (EAR-CMD-022, `execution/README.md` L70). TRN-ARCH-05 gap G3 (L59) says payloads must carry references, not values. For *Unbound domain* commands, though, the payload is the business data. So either record values sit indefinitely in Unbound's command table, or Unbound handlers read Transitus staging, which TRN-REQ-ST-006 forbids. The proposal does not resolve this.
4. **Transitus's own load-item intent and receipt rows** (TRN-ARCH-05 L153) add one or two more rows per record and are not in the model.

### Strongest case against
In dollars, storage is cheap. 50–75 GB of lineage plus perhaps 100–300 GB of command history over 7 years is tens of dollars a month, even counting CNV-ARC-001's synchronous standby (RPO 0) and backups at 2–3×. **Cost is not the problem.** The real problems are:
- **Personal data in lineage for 7 years.** L2 stores the "source natural key" in clear (TRN-ARCH-08 L20). For donors this is often a name, email or legacy account number. CNV-ARC-001 (`PLATFORM-UX-API-AND-ASSURANCE-STANDARDS.md` L257) requires "event payloads SHALL carry references to a PII vault". Command payloads holding full donor records break the same rule. TRN-REQ-SEC-018 (crypto-shredding) cannot shred a clear-text key held inside a hash-chained evidence structure without an explicit design.
- **Growth in the OLTP cluster**, which affects vacuum, backup and restore time, and so the RTO that CNV-ARC-001 requires per data class.

Performance overhead of L2 itself is small: one row per record, inside a transaction that already exists. **This part of C8 holds.** Static field lineage (L3-static, DF-TRN-2026-0013) is a sound design.

### Verdict: **rejected on cost, partially upheld on scope**
The overhead is not excessive. The model is wrong at the low end and leaves out the largest per-record store, which also holds the personal data.

### Required revisions
- **TRN-REQ-LN-002 (change):** L2 must store the source natural key as a tenant-keyed HMAC (as the exception store already does, TRN-ARCH-08 L87–88), never in clear.
- **TRN-REQ-LN-010 (add, P0):** lineage, command-store and receipt rows must have a declared retention class per data class. After the retention period they must be partitioned by month and detachable. The design must state which elements survive crypto-shredding and how the hash chain still verifies afterwards.
- **TRN-REQ-PF-003 (add, P0):** the storage model must include the per-record footprint of Echelon.Execution (command, history, outbox) and of Transitus intent/receipt rows. It must be measured with `pg_total_relation_size` including all indexes, and multiplied by standby/backup factors.
- **TRN-REQ-EX-013 (add, P0):** Unbound load commands must not carry personal data in clear in `command.payload`; they must carry PII-vault references (CNV-ARC-001). This is blocked on EAR-CMD-022 and must be listed as a dependency in TRN-ARCH-11.
- Correct TRN-ARCH-12 L85 to about 5.3 GB/yr at 300 B (7–11 GB/yr at 400–600 B). Change A9 to a 300–600 B range.

---

## C9. Loading through Unbound domain APIs does not constrain throughput unacceptably

### Per-command cost (from the code)
One record loaded as one durable command makes these database calls:

| Step | Statements / commits | Source |
|---|---|---|
| Transitus load intent row | 1 commit | TRN-ARCH-05 L153 |
| Intake: `CountNonTerminal` (`count(*)` over the tenant's open commands) | 1 statement | `Intake.fs` L96, `PostgresStore.fs` L147 |
| Intake: insert `command` + history | 1 commit, 2 rows, ≥5 index entries | `PostgresStore.fs` L144, L185 |
| Claim: a CTE over **all** non-terminal commands with a correlated `NOT EXISTS` for ordering-key heads, a window rank and `SKIP LOCKED` (amortized over the batch), plus one history insert per command | ~1 commit/batch | `PostgresStore.fs` L150–179, ~L497–508 |
| Execute: lock `FOR UPDATE`, re-check authorization (CNV-PLT-010), business writes, update command, insert history, insert outbox | 1 commit | `PostgresStore.fs` ~L512–545 |
| Outbox relay: mark delivered | 1 commit per effect | `Worker.fs` L212, `PostgresStore.fs` L199 |
| Transitus receipt + L2 row | 1 commit | TRN-ARCH-05 L153 |

That is **about 5 commits and 20+ statements per record**, before any business writes. Unbound's only measurement is a bare pgbench grant-approval transaction (about 10 statements, 1 commit). It ran on a 4-vCPU host with fast local fsync, and **without** the command store or synchronous replication. It reached 3,944 tx/s, falling to **2,127 tx/s with 1 ms round-trip time** (`unbound/requirements/discovery/2026-11-23-cross-industry/18-ARCHITECTURE-BENCHMARK.md` L20–41). CNV-ARC-001 adds a synchronous standby for RPO 0, which raises the cost of each commit.

Realistic ceiling, unbenchmarked: **about 300–800 records/s with the whole cluster dedicated** to the load. A7's 1,000 records/s is an upper bound that assumes Transitus owns the entire shared cluster (all sponsors, CNV-ARC-001). Under TRN-REQ-PF-002's OLTP budget, at say 25% of the cluster, the rate is **about 100–250 records/s**. That means 10⁶ records in roughly 1–3 h, and 10⁷ in roughly 11–28 h.

**A8 (20,000 records/s batched) is not credible for domain logic.** It is 5–10× the measured ceiling for bare business transactions. Batching saves command overhead, but it does not reduce the per-record authorization re-checks and ledger writes required by CNV-PLT-010 (L312). The only fast batch in the benchmark (B2: 100k funds in 1.5 s) is a set-based fee `UPDATE`, not per-record domain commands. **UNB-TRN-012, which A8 depends on (TRN-ARCH-12 L30), is not defined anywhere in either repository**: the reference dangles.

### Further constraints the proposal does not address
- **The tenant quota is shared with live donors.** `QueuedPerTenant = 10_000` (`Intake.fs` L38). At the limit, *every* submission from that sponsor gets `Throttled` with a 30 s retry, including donors' grant recommendations (L98). UNB-AVL-006 (`availability-architecture/02-REQUIREMENTS.md` L106) requires priority for control-adjacent work over batch work, but its status is "priority classes by operation pending". Transitus can starve its own sponsor.
- **Claim cost grows with backlog.** The claim CTE scans every open command across all tenants on every worker cycle. A migration backlog therefore slows claiming for every sponsor.
- **CNV-ARC-001 requires** "batch … work … in separately scaled worker roles" with reserved pools for critical paths. The in-process load must run in such a role. TRN-ARCH-05 does not say so.

### Batch commands versus Unbound's design
- **Ordering:** UNB-AVL-005 (L84–96) requires per-fund order to equal acceptance order. A command has exactly one `ordering_key` (Schema L15). A 500-record batch spanning many funds therefore bypasses the per-fund queues of live commands, and correctness then depends only on row locks. Benchmark B1 shows what a long multi-fund transaction does: approval p99 rose to 244 ms (L49).
- **Idempotency:** there is one key and fingerprint per command. If a batch's composition changes on retry, for example after an exception is fixed, the result is `IdempotencyConflict` (`Intake.fs` L78–82). That conflicts with TRN-REQ-EX-006's per-record keys and `replayExceptions`.
- **Per-record outcomes:** `HandlerResult` and the single `outcome_detail` per command cannot carry 500 individual receipts. L2 needs a receipt per record.
- **Quarantine:** one bad record quarantines the batch's key and blocks everything behind it (UNB-AVL-007).

**Concession.** For a one-time migration *before program activation*, there is no live traffic on the sponsor's funds. Activation requires tied-out opening balances (`ENTERPRISE-GAP-REGISTER…md` L164). Ordering conflicts are moot then, and even 100–250 records/s finishes a typical migration over a weekend. The recurring feeds also do not need batching: 50k custodian rows a day take 3–8 minutes unbatched. BMF data is shared charity reference data, not sponsor ledger commands. TRN-ARCH-12 L70–73 is therefore right that load is the bottleneck, but wrong that batch ledger commands are the remedy.

A different point is missed altogether. Historical facts (paid grants, settled contributions) must not be replayed through live-workflow commands such as `grant.recommend`, which trigger diligence, holds and dispatch. They need dedicated **historical-import operations** (WFM-26 staged balances). Those operations are naturally set-based and run before activation.

### Verdict: **partially upheld**
Throughput is acceptable at Echelon's volumes, but A7 is optimistic and A8 is unsupported. Batch domain commands conflict with UNB-AVL-005/-007 and with per-record idempotency and receipts after activation. Sharing the tenant quota is a real risk to the sponsor's own live operations.

### Required revisions
- **TRN-REQ-PF-001 (change):** A7 and A8 must be benchmarked through the real Echelon.Execution PostgreSQL adapter with synchronous standby, measured per committed record. Replace A7 with a range of 300–800 records/s (dedicated) and 100–250 (shared). Delete A8 until a defined Unbound operation exists.
- **TRN-REQ-AD-011 (add, P0):** the Unbound destination must keep the open commands it submits below a configured fraction of `QueuedPerTenant` (for example ≤20%), submit at the lowest priority class, and run in a separately scaled worker role with its own connection pool (CNV-ARC-001, UNB-AVL-006).
- **TRN-REQ-AD-012 (add, P0):** migration of historical facts must use dedicated, set-based Unbound historical-import operations allowed only before program activation, with per-record receipts. Post-activation loads must use per-record commands keyed by the domain's ordering key (per fund).
- **TRN-REQ-AD-008 (change):** state that batch commands touching more than one ordering key are prohibited after activation.
- **TRN-REQ-PF-002 (change):** define the OLTP budget numerically (for example, live approval p99 rises by no more than 10 ms) and test it with a migration backlog present.
- Define or remove UNB-TRN-012 and UNB-TRN-009, which are referenced at TRN-ARCH-12 L30 and `02-use-cases.md` L31 but defined nowhere. Add a dependency on EAR-CMD-022 and on Unbound's operation priority classes to TRN-ARCH-11.

---

## Summary of factual and arithmetic errors
1. TRN-ARCH-12 L85: lineage per year is understated. The low end is at least 3.75 GB from the custodian feed alone, and the total is ≈5.3 GB at 300 B.
2. A9 takes the low end of TRN-ARCH-08's 300–400 B range and ignores the extra indexes lineage needs.
3. Echelon.Execution's per-record storage (command, history, outbox; 1.5–3 KB) and the commits it adds are left out of both the storage and the throughput models.
4. A8 (20k records/s) exceeds Unbound's own measured ceiling for bare transactions (2,127–3,944 tx/s).
5. UNB-TRN-012 and UNB-TRN-009 are referenced but not defined.
6. `daf.grant-record` is labelled "public"; it is an unendorsed Echelon draft.
7. `vendor.ren-iphi` treats iPhi and DFX as one source system.
