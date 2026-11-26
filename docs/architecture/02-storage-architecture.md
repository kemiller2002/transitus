---
id: TRN-ARCH-02
title: Storage Architecture
status: proposed
version: 0.1.0
created: 2026-11-26
updated: 2026-11-26
work_item: WI-0001
decisions: [DF-TRN-2026-0008]
---

# Storage architecture

Four logical layers. Physical realization is **PostgreSQL (the host
application's database, DDL governed by Strata) + a blob store abstraction**.
No new database engine is introduced (DF-TRN-2026-0008).

```
┌───────────┐   ┌─────────────┐   ┌──────────────┐   ┌──────────────────────┐
│ Raw store │──▶│ Staging     │──▶│ Transformed  │──▶│ Destination          │
│ immutable │   │ typed, TTL  │   │ (=staged     │   │ via domain API only  │
│ CAS blobs │   │ chunked     │   │  datasets    │   │ (not Transitus-owned)│
└───────────┘   └─────────────┘   │  w/ status)  │   └──────────────────────┘
                                  └──────────────┘
```

## 1. Raw storage

Purpose: preserve original source inputs exactly.

| Attribute | Rule |
|---|---|
| Addressing | `sha256:<hex>` of the bytes. Identical bytes stored once per tenant. |
| Metadata row (`transitus.raw_object`) | tenant, content hash, size, media type (declared + sniffed), source id, source locator (path/URL/key — metadata only, never used as a storage path), acquisition timestamp (UTC, from injected clock), source-supplied timestamps (mtime, ETag, Last-Modified), adapter id@version, acquisition execution id, classification, retention class, legal-hold flag |
| Immutability | Write-once. Corrections are new raw objects. |
| Blob backend | `IBlobStore` port with two adapters: **PostgreSQL large-object/bytea chunk table** (default; zero new infrastructure; adequate to ~low tens of GB per tenant) and **S3-compatible object storage** (opt-in for large volumes; Azure Blob via the same port). |
| Encryption | Host-provided at-rest encryption; optional per-object envelope encryption with per-execution data keys to enable crypto-shredding. |
| Retention | Retention class → TTL; legal hold overrides; purge emits evidence (hash, size, purge time, policy id). |

Raw-file preservation has **no existing Echelon owner**: Arca explicitly
must not store large binary artifacts (ARCA-REC-007). Transitus therefore
defines the `IBlobStore` port; if a portfolio-wide object-storage component
emerges, the port is re-pointed (OQ-04).

## 2. Staging storage

Isolated, temporary, typed working data.

### Options evaluated

| Approach | Strengths | Weaknesses | Use when |
|---|---|---|---|
| **In-memory streaming** (`IAsyncEnumerable` chunks) | Fastest; no I/O | No resumability mid-stage; bounded by memory | Per-record transforms within a chunk; small reference lookups |
| **Chunked file-backed** (Parquet/Arrow IPC chunks in blob store) | Columnar, compact (5–10× smaller than row tables), cheap; scales to 10⁸ rows | Set operations need an engine (sort/merge in F#); not SQL-inspectable | Large volumes (≥ ~10⁷ rows) where DB staging cost dominates |
| **Database staging — dedicated schema with per-dataset tables** | Set operations (join, dedupe, aggregate) via PostgreSQL; inspectable; transactional with execution state | Write amplification; WAL volume; vacuum; per-tenant table churn | Default for ≤ ~10⁷ rows |
| **Database staging — generic JSONB rows** in one partitioned table | No DDL per dataset | 2–4× storage; weaker typing; slower set ops | Small, heterogeneous datasets (profiling samples, exceptions) |
| **Temporary tables** (`CREATE TEMP TABLE`) | No WAL; auto-drop | Session-bound — incompatible with leased, resumable, multi-worker execution | **Rejected** for stage outputs; allowed inside one chunk handler |
| **UNLOGGED tables** | ~2–3× faster writes, no WAL | Truncated on crash; not replicated | Acceptable for staging because raw input is preserved and stages are replayable — opt-in per pipeline |

### Decision (DF-TRN-2026-0008)

- Default: **typed, partitioned staging tables in a `transitus_staging`
  schema**, one table per *schema version* (not per dataset) partitioned by
  `(tenant, dataset_id)` via list partitioning; DDL generated from the
  schema definition and applied through **Strata** (Transitus never issues
  ad hoc DDL at runtime — staging tables for a pipeline's schemas are created
  when the pipeline is *published*, through the host's Strata-governed
  migration path). Dropping a partition is the purge mechanism (cheap,
  no vacuum debt).
- Opt-in: **chunked Parquet in the blob store** for very large pipelines,
  with set operations executed by an external-sort/merge-join implementation
  in the engine (phase 4; only if the performance model's thresholds are
  demonstrated in practice — see TRN-ARCH-12).
- In-memory streaming within a chunk always.

Open issue: generating DDL at publish time requires Strata to accept
programmatically produced schema fragments from an embedded library; this is
a proposed requirement for Strata (DEP-STRATA-01), not assumed.

### Staging controls

- Every staging row carries `tenant_id`, `execution_id`, `dataset_id`,
  `chunk_no`, `ordinal`, `source_locator`.
- Row-level security keyed on tenant (consistent with CNV-ARC-001 and
  UNB-TEN-009, which extend tenant isolation to queues and object storage).
- TTL per pipeline (`retention.staging`, default P30D, maximum P180D without
  elevated approval). A staged dataset is not readable by any API other than
  Transitus inspection/preview endpoints, which enforce classification.
- Staging is **not** a system of record: it has no external consumers and is
  never a source for another tenant or application (TRN-REQ-ST-006).

## 3. Transformed storage

Transformed datasets are staged datasets with additional status:
`draft → validated → reconciled → approved → loaded → verified`.
They support:

- **Inspection** (paged preview with classification-aware masking),
- **Reconciliation** (set-level comparisons),
- **Approval** (the approved `LoadPlan` references the dataset hash),
- **Replay** (re-load the same plan after a destination outage, reusing
  idempotency keys),
- **Loading** (the load stage reads only an approved, hash-matching dataset).

A dataset is sealed by a Merkle root over chunk hashes; approval binds to that
root, so any post-approval mutation is detectable.

## 4. Destination storage

Not owned by Transitus. Destinations are reached through registered
destination adapters (TRN-ARCH-03 §4). For Unbound regulated workflows the
adapter submits domain commands (e.g. through `Echelon.Execution` intake to
Unbound domain operations); Transitus has no credentials to Unbound's
business tables (TRN-REQ-AD-008).

## 5. Execution, exception, lineage and evidence stores

| Store | Content | Retention default |
|---|---|---|
| Execution state | owned by Echelon.Execution tables + `transitus.execution` | P2Y |
| Exceptions | record-level errors with code, locator, masked value/hash | P2Y |
| Lineage | see TRN-ARCH-08 | P7Y for financial |
| Evidence packages | manifests, report hashes, approvals | P7Y (SOC 2 / financial record-keeping); configurable |

## 6. Preventing an uncontrolled secondary system of record

1. TTL on staging, enforced by a retention stage and a periodic sweeper
   command; sweeper failure alerts.
2. No reporting/query API over staging beyond bounded previews.
3. Lineage stores *identifiers and hashes*, not full copies of values,
   except for fields explicitly marked `lineageCaptureValue` (TRN-ARCH-08).
4. Quarterly evidence: staging footprint per tenant and age distribution
   (automated SOC 2 evidence, TRN-SEC-02).
