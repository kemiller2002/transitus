# Transitus current state

## Repository status (2026-11-26)

Phase 0 has been revised per owner direction (transitus#1 comment 7200249612). It covers research, architecture, requirements and two adversarial reviews (TRN-REV-01, TRN-REV-02). No production code exists. Implementation and merge are not authorized.

## Observed facts

- **Phase-1 scope (owner, DF-TRN-2026-0018):**
  - a minimal declarative typed linear pipeline;
  - basic reusable mapping packages;
  - checkpoints, replay, idempotency, dry runs and migration rehearsal.
- **Demonstrations:** three theoretical pipelines covering IRS, bank/custodian and canonical migration. They validate against `schemas/pipeline-phase1.schema.json`, and the validator rejects seven classes of violation.
- **Requirements:** 152 in total, 121 of them in phase 1.
- **Decision records:** DF-TRN-2026-0001..0021. 4 are accepted (owner), 4 superseded, 13 in review.
- **Critical path:** it runs outside Transitus — Unbound domain operations, the canonical shape, the rehearsal cell, Echelon.Execution prerequisites, partner specifications and rights (`docs/open-questions.md`).

## Assumptions

- All performance and effort figures are theoretical.

## Active work

WI-0002 (owner-directed revision). Next: owner review of the `review`-status records and the unresolved conflicts UC-1..UC-16.
