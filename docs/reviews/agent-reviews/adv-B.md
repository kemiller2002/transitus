# Adversarial review B: Transitus claims C4, C5, C6

Reviewer stance: try to refute each claim with evidence, and concede where the evidence supports the proposal. In this review, "upheld" means **the challenge is upheld**, so the proposal's claim fails as written. Line references are to files under `transitus` unless another path is given.

---

## C4. Declarative transformations are expressive enough

### Concessions
The model fits the high-volume, well-specified feeds. U2 (BMF), U3 (revocations), U7/U8 (NACHA) and U4 (custodian) are mostly parse-then-map-then-reconcile. Their structural difficulty sits in compiled **format adapters/templates** (`nacha.ach/parse-returns@1`, `docs/research/02-use-cases.md:41-49`), which are code by design. The money, null, culture and loss rules (`docs/architecture/04-transformation-library.md:50-76`) are better than what most surveyed tools offer. No code in pipelines is a defensible control.

### Strongest case against
The catalogue (`04 §3`) and TEL (`01-lifecycle…md:133-155`) contain only value-level operations plus equi-key set operations. The scenarios the proposal itself puts in scope need several things that neither provides:

1. **Order-dependent scans (window, fill-down, running total).** Institutional migration exports (U1, `02-use-cases.md:22`) are often report-shaped XLSX. A group header row ("Fund: Smith Family") is followed by detail rows, then subtotal rows, and merged cells leave the key columns blank. Rebuilding them needs a forward fill keyed on the previous row. Checking that a reconstructed fund never went negative needs a cumulative sum ordered by date. The catalogue has no `lag`, fill-down, running-sum or row-number-within-group operation. `aggregate first-by(order)` collapses rows; it does not scan them.
2. **As-of (range) joins against effective-dated reference data.** `join@1` and `lookup@1` are equi-key only (`04:160-161`). U10 resolves a historical grant's charity EIN against the BMF (`02-use-cases.md:31`), but the correct question is the charity's status *on the grant date*. U5 needs the last price on or before the valuation date, and any FX handling needs the rate as of a date. None of these can be expressed.
3. **Date arithmetic and date parts.** §3.3 has parse, zone and business-day operations but no add-days, date difference, year/month extraction or fiscal-period derivation. TEL `Arith` works on decimals only (`01:147`). U10's reconciliation, "grants paid totals per fund per year" (`02-use-cases.md:31`), cannot be grouped by a sponsor's July–June fiscal year. U8 cannot compute the NACHA timeliness of "2 banking days" versus "60 calendar days", because `date.businessDay@1` only moves to the next or previous business day, not by n days.
4. **Generating rows from rules.** Legacy exports often store a recurring grant as a schedule ("$500 quarterly, 2019-01 to 2023-12"). Unbound treats installments as distinct obligations (`unbound/requirements/ENTERPRISE-GAP-REGISTER…md` UNB-GAP-006) and requires that legitimate installments are not deduplicated (`unbound/requirements/grants/GRANT-EVENT-CATALOG…md:181`, GEX-T14). Expanding a schedule into its instances is a bounded loop. TRN-REQ-PS-005 forbids loops outright.
5. **Transitive clustering.** For U9, `match@1` emits pairwise candidates (`04:165`). Donor deduplication needs clusters (A~B and B~C gives {A,B,C}), which is connected components, an iterative computation. Without it, reviewers adjudicate inconsistent pairs, and approving A=B, B=C but rejecting A=C is possible.
6. **Wide-to-long reshaping.** Vendor columns such as `Successor1Name/Pct … SuccessorNName/Pct` or `Grants2019…Grants2025` need an unpivot. `record.unnest` handles nested lists, not repeated columns.
7. **Nested-list predicates (FHIR, H1/H2).** `Observation.code.coding.where(system='http://loinc.org').code`, `value[x]` choice types and recursive `Observation.hasMember` panels all need list filtering, a variant type and bounded recursion. TEL has no list operators, and the value model (`04:78-93`) has no sum type. FHIRPath is the industry-standard language for exactly this. Helix Note's own feasibility work rates FHIR import as **XL** (`helix-note-application/research/2026-market-investigation/10-technical-feasibility/technical-feasibility.md:71`).
8. **Capture-group extraction.** Lab values such as `"<0.5 mg/dL"`, `"5.0-7.0"` or `"Positive"` (H2), and tribute text in donor memos, need regex extraction. `text.replace` only substitutes.

### Is the escape hatch adequate and governable?
**Not as specified.**
- **It covers values only.** An extension implements `Transform = Value -> Result<Value,…>` (`04:47, 191-196`). Gaps 1, 2, 4, 5 and 6 are **set-level or stateful**, and set operations run in PostgreSQL (`12` A6). There is no specified extension contract for set operators, and writing one would mean generating SQL, which DF-TRN-2026-0005 forbids. So the escape hatch cannot reach the counter-examples that matter most. The fallback is bespoke format adapters per vendor, which puts migration logic into parsers.
- **There is no sandbox.** In-process .NET (Core) has no code-access security, and `AssemblyLoadContext` is not a security boundary. A "pure" extension can read the clock, the culture, the file system, the network or the host's Unbound credentials. The conformance suite (`04:198-206`) is property testing, which cannot prove the absence of I/O or of a branch triggered by a rare value.
- **The economics break.** U1 is bespoke for every predecessor vendor. If each quirk needs a signed, reviewed, compiled release, then engineering is on the critical path of every migration. Mapping packages are code-free (TRN-REQ-MP-001), so vendor-specific code needs a separate, separately governed artifact.
- **The pattern is universal.** Every surveyed product ships a code escape: SSIS C# script components, Talend Java, NiFi Java processors, ADF Spark/Power Query, Bloblang (`docs/research/01-competitive-research.md:133, 249, 280, 815-817, 802`). The question is how the escape is governed, not whether it exists.

### Factual errors (C4)
- `number.parse@1`, `money.parse@1` and `date.parse@1` are classified **R (reversible)** (`04:118-119, 130`). Parsing `"1,234.50"`, `"+5"`, `"005"` or `"1/2/2026"` loses the original formatting, so the inverse property in conformance test 4 (`04:204`) fails for the proposal's own catalogue. These should be `I` with "loss: no material loss", or the reversibility definition should be redefined as value-level.

### Verdict: **upheld (claim fails as stated), with mitigation available**
"Sufficiently expressive" is false for U1, U9, U10, H1 and H2 without code. The design is recoverable with bounded, declarative set operators.

### Required revisions
- **New TRN-REQ-TX-011.** Add bounded declarative operators:
  - `window@1`: partitioned and ordered; lag, lead, fill-down, running sum, row number; requires a declared partition key and a maximum partition size.
  - `join.asOf@1`: effective-dated reference sets.
  - `date.add/diff/part/fiscalPeriod@1` and `date.businessDay` with an n offset.
  - `text.extract@1`: RE2 capture groups.
  - `reshape.unpivot@1`: with a declared column set.
  - `expand.schedule@1`: with a declared maximum number of instances.
  - `cluster.connected@1`: over match candidates, with a maximum cluster size; clusters, not pairs, go to review.
  - A FHIRPath-subset list predicate (`where/exists/first`, bounded recursion depth) inside TEL.
- **Amend TRN-REQ-PS-005.** Replace "loops … MUST NOT be expressible" with "unbounded iteration MUST NOT be expressible; bounded operators with declared cardinality limits enforced at runtime are permitted".
- **Amend TRN-REQ-PS-006 and add TRN-REQ-EXT-001..004:**
  - an extension contract for set-level operators and parse templates;
  - static IL banned-API analysis covering I/O, clock, culture, reflection-emit, P/Invoke, environment and threading;
  - extensions authored and signed by the platform owner only, never by tenants;
  - two-person review;
  - the extension assembly hash and its dependency closure in the execution manifest (TRN-REQ-AI-005);
  - an explicit risk acceptance that extensions run at full host trust.
- **Amend TRN-REQ-PS-010.** Make the acceptance criterion an **expressiveness corpus**: a complete pipeline fixture for each of U1–U12 and H1–H5 before phase 1 exits. Report the share of real-migration columns that needed an extension as a tracked metric.
- **Amend TRN-REQ-TX-004.** Fix the reversibility classifications for the parse operations.

---

## C5. PostgreSQL staging will not cause unacceptable bottlenecks

### Arithmetic check of `docs/architecture/12-performance-and-economics.md`
The volume table (`12:38-42`) is internally consistent with A1–A11. Core time = N/400k + 3N/50k + N/30k, so 10⁶ gives 95.8 s (≈1.6 min). Load at 10⁷ is 10⁴ s (≈2.8 h). WAL = 1.5 × 3 × N × 600 B. The 47 MB/s figure (`12:50`) is 45 GB / 960 s. **The errors are in what the model leaves out:**

1. **The lineage cost is understated** (`12:84`). Custodian alone is 50k × 250 × 300 B = **3.75 GB/yr**. BMF diffs at 5% are 2M × 0.05 × 52 × 300 B = 1.56 GB. The migration adds 5M × 300 B = 1.5 GB. That totals **≈6.8 GB/yr**, not "1.5–5 GB/yr", and **≈48 GB per sponsor** over the P7Y retention. Taken literally, the formula as printed gives 35 GB/yr.
2. **Raw retention exceeds the default backend.** ≈5 GB/yr compressed × 7 years = 35 GB per tenant for BMF alone. That exceeds the PostgreSQL blob default, which is rated "adequate to ~low tens of GB per tenant" (`02:36`). Because content addressing works "once per tenant" (`02:33`), every sponsor stores and stages the same public BMF again. §4 models "a sponsor running BMF weekly", so on a shared cluster with 100 sponsors that is roughly 200M staged rows per week. **The model works per execution and never per cluster.**
3. **The load-path writes are missing.** A7 is "command + history + outbox + business writes", but none of that appears in the storage or WAL figures. `Echelon.Execution.Postgres/PostgresStore.fs:144-199` shows one command INSERT, repeated UPDATEs of the command row (lease, status; each creates a dead tuple), one history INSERT per transition, and an outbox INSERT plus UPDATE. Each unbatched record therefore produces about 8–10 WAL-logged row versions. At 10⁷ records that is tens of millions of command and history rows, retained for P2Y (`02:120`).
4. **"1 set pass"** is unrealistic for U1, U9 and U10. Dedupe, match, join, balance and matchSets add up to at least four passes, or about 22 extra minutes at 10⁷. Validation, lineage and exception writes are also excluded from "core processing".
5. **The memory model uses 1 KB per record** (`12:48`) while A1 and A2 say 300 B and 600 B. A .NET record with about 30 boxed string fields probably exceeds 1 KB. The number is inconsistent, though it is not decisive.
6. **The recovery claim is wrong under UNLOGGED** (`12:53` versus `12:61`, `02:58`). After a PostgreSQL crash, UNLOGGED tables are truncated, and after an HA failover they are empty. Recovery is then a full replay (16 min of core time at 10⁷), not "lease + seconds". An approved, Merkle-sealed dataset (TRN-REQ-ST-005) that is waiting days for approval is lost and must be rebuilt bit-identically.

### Structural contradictions (more serious than the arithmetic)
- **The "no runtime DDL" rule contradicts per-dataset partitions.** DF-TRN-2026-0008 partitions by `(tenant, dataset_id)` and purges by dropping the partition (`02:62-69`). Dataset IDs are created per execution, so each execution needs `CREATE TABLE … PARTITION OF`, which is runtime DDL. TRN-REQ-ST-003 forbids that ("Execution role lacks DDL privilege"). It also takes heavy locks on the parent table, and partition churn bloats the catalogue.
- **LIST partitioning accepts only one key column.** "List partitioning by `(tenant, dataset_id)`" is not valid PostgreSQL; it would have to be multi-level partitioning.
- **COPY conflicts with RLS.** PostgreSQL documents that `COPY FROM` is not supported on tables with row-level security unless the role bypasses RLS. A5 (binary COPY at 50k rows/s) and the RLS control (`02:84`) cannot both hold. Either the execution role bypasses RLS, which defeats the control, or ingestion falls back to INSERT and A5 is invalid.
- **Chunk idempotency conflicts with COPY.** Handlers "upsert by (execution, stage, chunk)" (`05-execution-model.md:50`). COPY has no ON CONFLICT, so a retry needs delete-then-COPY, which creates dead tuples.
- **The tenancy model is incompatible.** CNV-ARC-001 requires a "schema and database role per sponsor tenant, row-level security on every tenant table" (`unbound/requirements/PLATFORM-UX-API-AND-ASSURANCE-STANDARDS.md:257`). Unbound's persistence design supports profiles A, B and C: separate schema, separate database and dedicated infrastructure (`unbound/architecture/TENANT-AWARE-PERSISTENCE-DESIGN.md:21`; UNB-TEC-STRATA-002). A single shared `transitus_staging` schema holding donor data from all sponsors fits none of them, and §2 cites CNV-ARC-001 as support while contradicting it.
- **Synchronous standby, replicas and connection pools.** CNV-ARC-001 sets RPO 0 through a **synchronous standby**. Every logged staging byte (27 GB of WAL at 10⁷) therefore competes with OLTP commit latency. The same clause requires batch and AI work to "read from replicas or snapshots under statement timeouts", with reserved pools for critical paths. Transitus set operations run on the primary, and UNLOGGED staging cannot be read on a replica at all.
- **"No vacuum debt" is false.** PostgreSQL 13+ autovacuums insert-only tables, and the first read after COPY sets hint bits. With data checksums on, as is typical on managed services, that produces full-page-image WAL. At Unbound's modelled burst rate of 200 tx/s, 200M XIDs are used in about 11.6 days, which is inside the P30D staging TTL. Anti-wraparound freeze of large staging partitions before they are dropped is therefore plausible. This is a burst-rate bound and must be measured.
- **Data persists past the TTL.** Logged staging rows survive in WAL archives, PITR backups and standbys long after the TTL purge. The purge evidence (`02:38`, TRN-REQ-SEC-012) therefore overstates erasure. Envelope encryption is optional and covers raw objects only.
- **The headroom is small.** The only measured capacity is 2,100–3,900 tx/s on fast local disk with 60 s runs, "autovacuum, bloat and checkpoint behaviour … not observed", and no concurrent batch (`unbound/requirements/discovery/2026-11-23-cross-industry/18-ARCHITECTURE-BENCHMARK.md` §1, §5). A7's 1,000 durable commands/s is 25–50% of that ceiling, versus the platform's own ~200 tx/s need. That benchmark also found that long batch transactions holding hot rows were the real risk (B1, p99 244 ms).

### Concession
At ≤10⁶ rows per execution with one tenant active, the absolute volumes are small (≤2 GB). The proposal is honest that every figure is theoretical (`12:13-16`, TRN-REQ-PF-001).

### Verdict: **partially upheld**
The numbers are mostly computed correctly, but the default physical design does not work as written: runtime DDL, the LIST key, COPY with RLS, and the tenancy profile all conflict. The model also leaves out the cluster-wide, load-path, lineage and synchronous-replication costs. "Will not create unacceptable bottlenecks" has not been shown on a shared synchronous-standby OLTP cluster.

### Required revisions
- **Amend DF-TRN-2026-0008 and TRN-REQ-ST-003.**
  - Use pre-created, publish-time slot or time-bucket partitions per tenant schema, purged by TRUNCATE (with the privilege granted), and fix the partition key.
  - Or default to blob-backed chunk staging for tenants on shared clusters, and amend TRN-REQ-ST-008 so the threshold is measured rather than ~10⁷.
- **New TRN-REQ-ST-009.** Staging MUST follow the host's isolation profile (A/B/C): schema and role per sponsor, never a cross-tenant shared schema.
- **New TRN-REQ-ST-010.** The ingest path MUST work with RLS enforced and without BYPASSRLS. Re-baseline A5 accordingly.
- **New TRN-REQ-ST-011.** UNLOGGED staging MUST NOT hold approved datasets awaiting load unless rematerialisation and Merkle re-verification are tested. Correct the recovery-time claim.
- **Amend TRN-REQ-SEC-012/018.** Envelope-encrypt classified staging columns with per-execution keys, so crypto-shredding covers WAL, backups and replicas.
- **Raise TRN-REQ-PF-002 to P0.** Run it on the chosen managed PostgreSQL with a synchronous standby and the Unbound S5–S7 mix running concurrently, for at least 4 hours, so checkpoints, autovacuum and freeze are observed. Run N tenants concurrently. The budget is Unbound's approval SLO.
- **New TRN-REQ-PF-003.** Adaptive throttling: on WAL rate and standby replay lag, a dedicated pool separate from the CNV-ARC-001 reserved pools, statement timeouts, and a maximum chunk lock footprint.
- **New TRN-REQ-PF-004.** Add to the model: Execution command, history and outbox rows; lineage WAL; multiple set passes; and cluster-wide aggregates. Correct §4's lineage figures.
- **New TRN-REQ-ST-012.** Public reference pipelines (BMF, revocations) run once per platform and are shared under licence (TENANT-AWARE design, "Shared charity reference data"), not once per tenant.

---

## C6. AI-assisted mapping is reliable and safe

### Concessions
The containment architecture is sound and better than most vendors':
- no model calls on the runtime path (`07:15-18`, TRN-REQ-AI-005);
- proposals only, with a read-only tool surface (`07:61`);
- an authority-envelope validator that applies "regardless of who proposed it" (`07:62`);
- output that must be schema-typed;
- a CI injection corpus;
- an explicit refusal to claim accuracy before measurement (`07:69-73`).

### Strongest case against
1. **The authority envelope does not cover semantic harm.** TRN-REQ-PS-008 covers sources, destinations, egress, secrets, gates, tolerances, acknowledgeLoss and classification. It does not cover changes that are equally dangerous and pass type checks:
   - mapping `received_date` to `deposit_date` (moves contributions across tax years, with donor-receipt consequences);
   - swapping same-typed Money columns (`cost_basis` and `fair_market_value` on stock gifts);
   - editing `enum.map` entries (a return-reason code mapped to "settled");
   - changing **idempotency-key fields** (collapses distinct records, or duplicates loads);
   - lowering `match@1` auto-link thresholds;
   - changing `filter` predicates, routes, `runIf` and **`autoApproveIf`** (`01:113`);
   - changing `maxErrorRate`;
   - changing reference data, which "suggest remediation" explicitly proposes (`07:40`).

   Only fixtures and reconciliations stand between these changes and a load. Fixtures are synthetic, and control totals do not cover dates or roles.
2. **The deterministic "confirmation" heuristics are weak.** "Amount appears to be in cents … all values integers, magnitude ×100" (`07:34`) misfires on DAF data, where whole-dollar grants are the norm.
3. **Data exposure gaps.**
   - Profile statistics are a default model input (`07:32`), but TRN-REQ-AI-007 limits defaults to "schema metadata and synthetic or masked samples". Top-k values, min/max and distinct examples of a donor-name or diagnosis column are real PII or PHI.
   - Column headers in pivoted exports can be donor or patient names.
   - Masked samples of small populations can be re-identified.
   - Nothing requires a provider contract with zero retention, or a BAA for PHI (H5).
4. **Factual error.** §6 states "Azure OpenAI is already used by Helix Note" (`07:78`). Helix Note actually calls `https://api.openai.com/v1/chat/completions` (`helix-note-application/api/HelixNote.AI.OpenAI.fs:110`) at temperature 0.3–0.7. Helix's own privacy research marks the HIPAA eligibility of Azure OpenAI as "Not verified" (`…/07-privacy-and-regulation/privacy-and-regulatory-landscape.md:331`).
5. **Second-order injection.** Pipeline `description` is "AI-readable" (`schemas/pipeline.schema.json:16`). `annotations` are excluded from the content hash (`:105`), so they can change without a new version or an authority diff. Package semantics docs are fed back into prompts. These are persistent injection carriers that TRN-REQ-AI-003 does not class as untrusted.
6. **Determinism and audit.** TRN-REQ-AI-006 records model, prompt-template version and hashes. It does not record sampling parameters, the provider deployment or snapshot version, the tool schema, or the retained prompt text, which an injection investigation needs.
7. **Reliability is unmeasured and ungated.** TRN-REQ-AI-008 is **P2, verified by "review"**, and blocks only *claims*, not *enablement*. The competitive research shows vendors ship AI features but cites no accuracy evidence (`01-competitive-research.md:47-51`). No requirement addresses reviewer automation bias, even though human approval is the main safety argument. Unbound's own UNB-GAP-033 requires evaluation and safe operation without AI.

### Verdict: **partially upheld**
The *safety architecture* is credible; prompt injection cannot directly widen authority. *Reliability* is unevidenced. The envelope misses semantic and approval-predicate changes, and the data-exposure defaults leak through profiles.

### Required revisions
- **Raise TRN-REQ-AI-008 to P0 with a phase-3 gate.** Before enablement, require per-field-class precision thresholds on held-out, customer-authorized vendor exports, a measured dry-run catch rate, and a reviewer study. Disable per tenant if precision falls below the threshold.
- **Extend TRN-REQ-PS-008.** Add idempotency-key fields, match thresholds, `autoApproveIf`/`runIf`/route/filter predicates, enum and reference-data edits, and `maxErrorRate` to the elevated-review envelope.
- **New TRN-REQ-AI-009.** AI-proposed mappings that touch Money, tax-date or role fields need a second approver and mutation fixtures: swapping any two same-typed mapped fields MUST fail the dry run.
- **Extend TRN-REQ-AI-007.** Classify profile statistics and headers, apply small-cell suppression, and require provider zero-retention terms, or a BAA for PHI.
- **Extend TRN-REQ-AI-003.** Treat descriptions, annotations and package docs as untrusted. Include `annotations` in the authority diff, or exclude them from prompts.
- **Extend TRN-REQ-AI-006.** Record sampling parameters, the deployment or snapshot version and the tool schema, and retain the encrypted prompt.
- **Correct the Helix Note provider statement** in `07 §6`.
