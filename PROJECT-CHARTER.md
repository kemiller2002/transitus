---
id: PROJECT-CHARTER-transitus
title: Transitus Project Charter
status: proposed
version: 0.2.0
created: 2026-11-26
updated: 2026-11-26
work_item: WI-0001
---

# Transitus project charter

## Mission

Establish Transitus as a reusable, embeddable, AI-native data integration
engine for Echelon Foundry. It should make data ingestion, transformation,
migration and recurring integrations predictable, reproducible, secure and
inexpensive. Unbound is the first reference application, and the
architecture remains domain-independent.

## Business purpose

Every Echelon application that handles regulated data has to bring data in
from outside sources:

- Unbound: IRS charity files, custodian and bank files, predecessor-platform history;
- Helix Note: patient-authorized records;
- Summa: opening balances and bank feeds.

Without a shared engine, each application hand-builds parsers, reconciliation
and evidence, and these diverge in quality and auditability.

Transitus supplies the parts that are generic:
- typed parsing;
- deterministic transformation;
- validation and reconciliation primitives;
- raw-input preservation;
- lineage and evidence;
- effectively-once loading through domain APIs.

Domain rules stay in the domains.

The case for Transitus is **not** licence savings. Generic tools are cheap at
Echelon volumes (TRN-ARCH-12 §5). The case rests on four things:

1. loading through business invariants, with blocking financial gates and evidence;
2. no second runtime, and no third-party processor of regulated data;
3. reuse across applications;
4. migration as a repeatable, assurable capability.

The adversarial review (TRN-REV-01) tests that case, and the phased roadmap
includes kill criteria.

## Initiating brief

The initiating brief (2026-11-26) has 22 sections, referenced as §1–§22
throughout `requirements/TRACEABILITY.md`.

| § | Topic | Primary response |
|---|---|---|
| 1 | Mission | this charter |
| 2 | Repository context, Echelon overlap, registry | TRN-ARCH-11; echelon-registry PR |
| 3 | Competitive research | TRN-RES-01, TRN-RES-03 |
| 4 | Lifecycle | TRN-ARCH-01 §2–3 |
| 5 | Storage | TRN-ARCH-02 |
| 6 | Declarative pipelines | TRN-ARCH-01, `schemas/pipeline.schema.json` |
| 7 | Transformation library | TRN-ARCH-04 |
| 8 | Adapters | TRN-ARCH-03, `schemas/adapter-descriptor.schema.json` |
| 9 | AI-native configuration | TRN-ARCH-07 |
| 10 | Mapping packages | TRN-ARCH-09, `schemas/mapping-package.schema.json` |
| 11 | Execution | TRN-ARCH-05 |
| 12 | Validation and reconciliation | TRN-ARCH-06 |
| 13 | Lineage and evidence | TRN-ARCH-08 |
| 14 | Security | TRN-SEC-01, TRN-SEC-02 |
| 15 | Visual administration | TRN-ARCH-10 |
| 16 | Echelon architecture | TRN-ARCH-00, TRN-ARCH-11 §2 |
| 17 | Reference use cases | TRN-RES-02 |
| 18 | Performance and economics | TRN-ARCH-12 |
| 19 | Adversarial review | TRN-REV-01 |
| 20 | Deliverables | `docs/README.md` index |
| 21 | Cross-repository updates | Unbound, daf-landscape, registry PRs |
| 22 | Completion criteria | `HANDOFF.md` |

## Intended users

- **Engineers** embedding Transitus in Echelon applications. Unbound comes first.
- **Data stewards and operations staff**, who approve loads and resolve exceptions.
- **Migration engineers**, who onboard sponsors from predecessor platforms.
- **Auditors**, who consume the evidence packages.
- **AI agents**, which author pipeline proposals against the machine-readable specification.

## Scope

**Included**
- Declarative pipeline model and validator.
- Transformation and check libraries.
- Adapter contracts and a minimal standard adapter set.
- Raw, staging, lineage and evidence storage.
- Pipeline execution on Echelon.Execution.
- Mapping packages.
- AI proposal protocol.
- Later: a Forma-based administration UI.

**Excluded**
- A general workflow orchestrator.
- A job queue (Echelon.Execution provides one).
- Schema governance (Strata provides it).
- CDC platforms, event-stream processing and bidirectional sync / MDM.
- Domain accounting rules.
- A monitoring platform.
- Document OCR / NLP extraction.
- Independently deployed services.
- Any production code during phase 0, this research phase.

## Success criteria (initiative completion, §22)

1. The business purpose is clear (above).
2. Competitive alternatives have been evaluated (TRN-RES-01).
3. Architectural boundaries are explicit (TRN-ARCH-11).
4. Core requirements are traceable (`requirements/TRACEABILITY.md`).
5. Security and failure behaviour are defined (TRN-SEC-01, TRN-ARCH-05).
6. Unbound reference scenarios are covered (TRN-RES-02).
7. Existing Echelon capabilities are not duplicated (TRN-ARCH-11).
8. Material decisions have had adversarial review (TRN-REV-01).
9. Open questions are documented (`docs/open-questions.md`).
10. A minimal viable implementation scope is established (`docs/roadmap.md`).

## Constraints

- F#, written in a functional style.
- An embeddable component monolith.
- WASM-first administration UI on Forma and Limen.
- Persistence: PostgreSQL with DDL governed by Strata.
- Fault handling through Aegis.
- Reports through Folio.
- Praxis governance.
- Unit tests are required.
- Infrastructure dependencies are kept to a minimum.
- No microservices without explicit approval.

**Licence.** The brief says MIT for public repository content, while the portfolio components use PolyForm Noncommercial; see OQ-12. This repository's documentation is MIT-licensed per the brief.

## Owners and decision authority

- **Repository owner:** kemiller2002. Material decisions are escalated to the owner (`docs/open-questions.md`).
- **Routine decisions:** recorded as DF-TRN records in `docs/decisions/`.
