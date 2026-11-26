---
id: TRN-ARCH-00
title: Architectural Principles
status: proposed
version: 0.1.0
created: 2026-11-26
updated: 2026-11-26
work_item: WI-0001
---

# Architectural principles

Each principle names the failure it prevents and the evidence behind it.
`SRC-` identifiers refer to `docs/research/source-register.md`; `ECH-`
identifiers refer to Echelon repository evidence listed in
`docs/architecture/11-echelon-dependency-analysis.md`.

| ID | Principle | Prevents | Evidence |
|---|---|---|---|
| P1 | **Pipelines are data.** A pipeline is a versioned, hashed, declarative document interpreted by the engine. No user-supplied code, SQL, script, or expression `eval`. | Unreviewable logic; injection; vendor-style "script task" sprawl. | SSIS Script Task / Informatica Java transformation complaints; Echelon SEC-DB-001 (no dynamic SQL) ECH-BND-10. |
| P2 | **One authoritative definition.** Visual editors, AI assistants and APIs all edit the same JSON document. | Visual/executable drift (PowerCenter repository XML vs. exported mappings). | ECH-FORMA-ADR-0006 (Forma portable workflow standard). |
| P3 | **Preserve before you parse.** Raw bytes are content-addressed and retained before any interpretation. | Irreproducible results; disputes without the original. | Unbound UNB-EXT-017..029, UNB-KNOW-023, CNV-FIN-013. |
| P4 | **Determinism is a contract.** Same raw input hash + pipeline hash + package hashes + reference-data versions + parameters + engine version ⇒ equivalent output. No ambient culture, clock or randomness. | Silent behavioural drift; un-auditable migrations. | — (design requirement TRN-REQ-AI-005) |
| P5 | **Nothing is silently lost.** Every record is accounted for: loaded, rejected, quarantined, or deduplicated — with counts that reconcile by construction. No silent truncation, rounding, defaulting or discarding. | Financial misstatement. | CNV-FIN-004 ("no silent write-offs"); RR-REQ-X-061-r1. |
| P6 | **Load through the front door.** Systems of record are written only through domain APIs / approved domain interfaces, never by direct table writes. | Bypassing business invariants and authorization. | UNB-API-002; echelon-registry "Integration boundary" invariant. |
| P7 | **Effectively-once, never "exactly-once" claims.** Idempotency keys, durable state, verification and reconciliation; ambiguity is an explicit state. | False assurance; duplicate payments. | Echelon.Execution OutcomeUnknown (EAR-CMD-014). |
| P8 | **Gates before effects.** Validation, reconciliation and authorization are blocking stages ahead of any system-of-record load. | Loading then discovering errors. | RR-REQ-X-061-r1 MigrationRun states; UNB-RCN-WF-020. |
| P9 | **AI proposes; deterministic gates dispose.** AI output is a diff to a pipeline definition, subject to the same validation and approval as a human change; AI never executes, approves or loads. | Prompt-injection-driven authority changes; nondeterministic transforms. | TRN-SEC-01 T09. |
| P10 | **Consume, don't duplicate.** Durable execution comes from Echelon.Execution; schema DDL from Strata; workflow visualization from Forma; fault handling from Aegis; printable reports from Folio; UI boundary from Limen. | Parallel half-implementations across the portfolio. | Praxis SHARED-APPLICATION-FOUNDATIONS §1; echelon-registry duplication analysis. |
| P11 | **Embedded library, not a platform.** Transitus ships as F# libraries hosted inside a consuming application (component monolith). No separately deployed service, broker, cluster, or Spark runtime. | Operational overhead that dominates the integration market's TCO. | ADR-EVA-001 / CNV-ARC-001 (no broker at release 1); competitor TCO evidence (TRN-RES-01). |
| P12 | **Smallest sufficient adapter set.** Build adapters only for demonstrated consumer scenarios; contracts let others be added without changing the core. | Connector-catalogue maintenance burden. | Airbyte/Singer connector quality complaints (TRN-RES-01). |
| P13 | **Generic core, domain rules outside.** Reconciliation *primitives* live in Transitus; accounting rules (e.g. what balances must tie, NAV tolerances) live in Unbound mapping/validation profiles. | Transitus becoming an Unbound-specific accounting engine. | Charter §2. |
| P14 | **Staging is temporary and governed.** TTL, tenant scoping, encryption and purge evidence; never queryable as a business system. | Shadow system of record. | Charter §5. |
| P15 | **Explain everything in machine-readable form.** Every operation, field and error code has AI-readable semantics documentation. | AI hallucinating semantics; onboarding cost. | Charter §6. |
