---
id: TRN-ARCH-06
title: Validation and Reconciliation Model
status: proposed
version: 0.1.0
created: 2026-11-26
updated: 2026-11-26
work_item: WI-0001
decisions: [DF-TRN-2026-0011]
---

# Validation and reconciliation model

## 1. Separation of concerns

| Layer | Owner | Examples |
|---|---|---|
| **Primitives** (generic, parameterized, deterministic) | Transitus | count equals, sum equals within tolerance, uniqueness, referential integrity, sequence continuity, opening + movements = closing |
| **Profiles** (compositions of primitives with parameters) | Mapping packages (domain-owned) | "Custodian daily positions profile", "NACHA file control profile" |
| **Accounting rules** (what must tie to what, tolerance policies, posting consequences) | Consuming application (Unbound) | NAV tolerance, contribution recognition, variance-power evidence, CNV-FIN-004 ProvisionalCalibration |

Transitus never posts balancing entries, write-offs or suspense entries
(TRN-REQ-VR-009). A discrepancy is a report and an exception, never a
correction.

## 2. Validation primitives (record and dataset level)

| Primitive | Level | Parameters | Result |
|---|---|---|---|
| `v.required@1` | record | fields | per-record error |
| `v.type@1` | record | (implicit from schema) | per-record error |
| `v.range@1` | record | min/max (typed) | per-record error |
| `v.pattern@1` | record | linear-time regex | per-record error |
| `v.codeSet@1` | record | code set@v | per-record error |
| `v.checkDigit@1` | record | algorithm (ABA, Luhn, mod-97, EIN prefix table) | per-record error |
| `v.crossField@1` | record | TEL predicate | per-record error |
| `v.unique@1` | dataset | key fields, scope (file / execution / destination via read-back) | duplicate groups |
| `v.referential@1` | dataset | foreign key → staged dataset / reference set / destination lookup | orphans |
| `v.completeness@1` | dataset | expected key set (from control file, previous snapshot, or calendar) | missing keys |
| `v.sequence@1` | dataset | sequence field, gap/duplicate/out-of-order policy | breaks |
| `v.freshness@1` | dataset | as-of field, max age | stale flag |
| `v.distribution@1` | dataset | metric, previous-run baseline, max change % | anomaly (non-blocking by default) |

## 3. Reconciliation primitives

| Primitive | Compares | Typical use |
|---|---|---|
| `r.count@1` | record counts: source declared (trailer/control) vs parsed vs staged vs loaded vs read-back | every pipeline |
| `r.controlTotal@1` | sum of a money/decimal field vs control value (file trailer, separate control file, bank statement) | NACHA batch/file control (entry hash, total debit/credit), custodian files |
| `r.hashTotal@1` | sum/modular hash of identifiers vs declared | NACHA entry hash (sum of routing numbers, mod 10¹⁰) |
| `r.balance@1` | opening + Σ movements = closing (per account, per currency) | custodian positions/transactions, migrations of fund balances |
| `r.matchSets@1` | keyed set A vs keyed set B → matched / A-only / B-only / matched-with-differences | migration source vs destination read-back; bank activity vs expected settlements |
| `r.crossFile@1` | dataset from file X vs dataset from file Y (same execution or prior) | positions vs transactions consistency |
| `r.crossSystem@1` | staged dataset vs destination read-back or domain report API | post-load verification |
| `r.timing@1` | matched items with date differences classified as timing vs break, given a window | settlement T+1/T+2, ACH returns within 2 banking days |

Each primitive returns a typed report:

```fsharp
// Illustrative only — not production code.
type Difference =
    | Missing of side: Side * key: NaturalKey
    | ValueMismatch of key: NaturalKey * field: FieldPath * left: Value * right: Value
    | TotalMismatch of measure: string * expected: decimal * actual: decimal * currency: string option
    | TimingDifference of key: NaturalKey * days: int
    | SequenceBreak of expected: int64 * actual: int64

type ReconciliationOutcome =
    | Balanced
    | BalancedWithinTolerance of Tolerance * Difference list     // tolerance must be declared; financial default is zero
    | Unbalanced of Difference list
```

Tolerance defaults to **zero** for money. A non-zero tolerance must be
declared in the (domain-owned) profile with a justification and is shown
in evidence.

## 4. Gates

- A `validate` or `reconcile` stage marked `gate: blocking` halts the
  execution in `Blocked` if its outcome is not acceptable; nothing downstream
  runs.
- `gate: advisory` records results and continues.
- Pipelines whose destination is classified `system-of-record` with any field
  classified `restricted-financial` must have at least one blocking count
  reconciliation and one blocking control-total or balance reconciliation
  (validator rule PV-12).
- **Phase 1: no overrides** (TRN-REQ-VR-005, revised). A failed gate stops the execution. Remediation is a corrected mapping, reference data or source, followed by a new execution. Later phases may allow the following only by decision record:
- Overriding a blocking gate is an **authorization** with elevated approval;
  the override, its justification and the unresolved differences become part
  of evidence. Overrides never change the data.

## 5. Accounting for every record (conservation law)

For every stage:

```
in = out + rejected + quarantined + deduplicated + filteredWithCount
```

The engine computes and asserts this invariant per stage per chunk; a
violation is an engine defect and fails the execution (TRN-REQ-VR-007).
The evidence package includes the full conservation table from raw record
count to verified destination count.

## 6. Exception queues

Exceptions are typed (`code`, `stage`, `rule`, `locator`, `severity`,
`classification-aware value`), grouped by code for bulk resolution, and
resolvable by:

1. **Fix mapping** → new pipeline version → re-run (preferred; benefits all
   future runs).
2. **Supply reference data** (e.g. add an enum mapping) → re-run.
3. **Correct source** → new raw input.
4. **Accept as excluded** — requires a reason and, for financial records,
   approval; appears in reconciliation as an explained difference.

Never: editing staged values by hand. (A "manual override" value, if ever
needed, is modelled as a versioned reference-data entry so it is auditable
and replayable.)

Human follow-up for exception resolution may be raised in **Vigila** as
follow-up items (`followup.create`) when Vigila is present (optional
capability; absent-safe).
