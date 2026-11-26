---
id: TRN-ARCH-08
title: Data Lineage and Evidence Model
status: proposed
version: 0.1.0
created: 2026-11-26
updated: 2026-11-26
work_item: WI-0001
decisions: [DF-TRN-2026-0013]
---

# Data lineage and evidence model

## 1. Lineage granularities

| Level | What is recorded | Cost (per 10⁶ records, theoretical) | Default |
|---|---|---|---|
| L0 Execution | execution manifest: raw input hashes, pipeline/package/reference/engine versions, parameters, reports, approvals | O(1): a few KB | always |
| L1 Dataset/chunk | chunk hashes, counts, Merkle roots, stage→stage edges | ~100 chunks × ~200 B ≈ 20 KB | always |
| L2 Record | for each destination record: source raw hash + record locator (row/byte offset/JSON pointer) + source natural key + destination id + idempotency key + receipt id | ~150–250 B/record of data; with PostgreSQL row overhead and the 2–3 indexes needed to query by destination id, source hash and execution ≈ 400–600 B/record ⇒ 400–600 MB (revised after TRN-REV-01 C8). Natural keys of personal records are stored as tenant-keyed HMACs (TRN-REQ-LN-002) | system-of-record destinations |
| L3 Field | for each destination field: contributing source fields + operation chain | Stored as **mapping-level static lineage** (field→field graph per pipeline version, a few KB) + record-level L2. Per-record field values are *not* stored. | static always; dynamic only for fields marked `lineageCaptureValue` |

Key insight: field-level lineage is almost entirely **static** — it is a
property of the pipeline version, not of each record. Combining static field
lineage (L3-static) with record lineage (L2) answers "where did this
destination field value come from?" exactly, by re-deriving through the
deterministic pipeline from the preserved raw input, without storing per-field
values (DF-TRN-2026-0013).

Dynamic field capture (`lineageCaptureValue`) is reserved for fields where
the branch taken depends on data (e.g. `coalesce` chose source B) and the
domain requires the explanation without replay; the engine stores the
branch/selection code (1–2 bytes), not the value.

## 2. Traceability of a destination record

Required linkage (TRN-REQ-LN-001):

| Element | Source |
|---|---|
| Original source | `raw_object.source_id`, locator |
| Source record identifier | natural key + locator |
| Source version | raw content hash; source-supplied version/ETag |
| Pipeline version | pipeline content hash + semver |
| Mapping version | package id@version + hash |
| Transformation operations | static lineage graph of the pipeline version |
| Reference data versions | execution manifest |
| Validation results | report ids (and per-record exceptions, if any) |
| Authorization decisions | approval event id |
| Execution identifier | execution id (+ Echelon.Execution command ids) |
| Destination response | receipt (destination id, status, response hash) |

## 3. Evidence package

Produced by the `evidence` stage. Structure:

```
EvidencePackage
 ├─ manifest.json        (execution manifest; hashes of everything below)
 ├─ conservation.json    (record accounting per stage)
 ├─ validation/*.json
 ├─ reconciliation/*.json
 ├─ approvals/*.json     (signed approval events)
 ├─ receipts-summary.json
 ├─ exceptions-summary.json (codes, counts; values masked per classification)
 └─ chain.json           (hash chain: each entry = H(prev ‖ entry))
```

- Hash-chained per execution and anchored by a running per-tenant chain head
  (append-only table) so deletion or reordering is detectable (T21).
- **Folio** renders human-readable/printable evidence reports from the package
  (Folio is the proposed presenter for auditor export, registry GAP-06).
- **Vigila** receives follow-ups for unresolved exceptions and
  `OutcomeUnknown` obligations when present. Note: Vigila is a follow-up
  tracker, *not* an operational observability platform; runtime monitoring is
  currently unowned in the portfolio (GAP-05). Transitus emits OpenTelemetry
  metrics/traces through the host and does not create its own monitoring
  stack (see TRN-ARCH-11 DEP-VIGILA-01, OQ-03).
- OpenLineage event export is an optional adapter (phase 4) for customers who
  run Marquez/DataHub; the internal model is mapped to OpenLineage RunEvent
  facets (TRN-RES-01 §patterns).

## 4. Sensitive data minimization

- Logs and telemetry carry execution ids, record locators and hashes; never
  values of fields classified above `internal` (T22).
- Exception store keeps values only when classification permits; otherwise a
  keyed hash (HMAC, tenant key) to support grouping without disclosure.
- Evidence packages contain no raw values above `internal`; they reference
  the raw object hash, which is itself subject to retention.
- When raw input is purged under retention, L2 lineage remains (hash and
  locator), and evidence records that the raw object was purged (purge
  evidence id), so lineage degrades gracefully to "proved at the time,
  original no longer retained".
