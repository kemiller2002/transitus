# Transitus current state

## Repository status (2026-11-26)

Phase 0 is complete pending owner review. This covers research, architecture, requirements and adversarial review. No production code exists.

## Observed facts

- No existing Echelon component provides typed ingestion with raw preservation, control totals and evidence. Adjacent capabilities have owners (TRN-ARCH-11).
- Echelon.Execution, incubating in `unbound/execution`, already provides durable execution.
- Unbound already parses the IRS and OFAC files in its replay tooling.
- Vigila is a follow-up tracker, not an observability platform. Runtime monitoring has no owner (registry GAP-05).
- At Echelon volumes the generic integration tools are cheap. The case for Transitus therefore rests on domain-API loading, gates, evidence and a single runtime (TRN-ARCH-12 §5).
- Four independent adversarial reviews converged on a three-library phase 1 (TRN-REV-01).

## Assumptions

- All performance figures are theoretical (TRN-ARCH-12). The PF-001 benchmarks replace them in phase 1.

## Active work

WI-0001 (research initiative). Next: the owner answers OQ-13 and OQ-14, and reviews the DF-TRN records. Phase 1 then starts as described in `docs/roadmap.md`.
