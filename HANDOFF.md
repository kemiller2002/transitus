# Transitus handoff

## Objective

Phase 0 of Transitus covers research, architecture and requirements only (WI-0001). The goal is to establish Transitus as a reusable, embeddable data-integration engine for Echelon Foundry, with Unbound as the first reference application.

## Work completed

- **Competitive research.** 20 products, 128 sources, plus 23 Echelon evidence sources. See `docs/research/`.
- **Architecture.** TRN-ARCH-00..12: principles, lifecycle and pipeline specification, storage, adapters, transformation library, execution, validation and reconciliation, AI, lineage, mapping packages, administration UI, Echelon dependency analysis, and performance and economics.
- **Security.** Threat model and compliance control mapping (`docs/security/`).
- **Requirements.** 136 proposed requirements with traceability (`requirements/`), rendered from `tools/requirements_source.py`.
- **Machine-readable artifacts.** JSON Schemas and an example pipeline (`schemas/`, `examples/`).
- **Adversarial review.** Four independent reviewers covered twelve challenges, with dispositions applied (`docs/reviews/`).
- **Decisions.** DF-TRN-2026-0001..0017, all with status `review` (`research/decisions/`). Index: `docs/decisions/README.md`.
- **Planning.** Open questions (`docs/open-questions.md`) and the phased roadmap with triggers and kill criteria (`docs/roadmap.md`).
- **Cross-repository pull requests:**
  - echelon-registry: Transitus inventory entry;
  - unbound: UNB-TRN discovery requirements;
  - daf-landscape: migration-tooling findings.

## Decisions and assumptions

- **Phase 1** is three pure libraries (Formats, Checks, Evidence) that serve the Unbound release-1 feeds (DF-TRN-2026-0016).
- **The engine, declarative model, packages, AI and UI** wait for triggers T2, T3 and T4.
- **Echelon.Execution** is used in place inside Unbound. Extraction happens at T2 (DF-TRN-2026-0006).
- **Licence:** MIT, per the brief. The portfolio-level decision is open (OQ-12).

## Validation run

- `./praxis validate`: passed.
- `./praxis registry check`: passed.
- `python3 -I tools/render_requirements.py --check`: passed.
- The JSON Schemas pass the Draft 2020-12 metaschema check, and the example pipeline validates against `schemas/pipeline.schema.json`.
- Not run: no .NET SDK was available here. No F# code exists in phase 0; the requirements renderer is Python by recorded deviation (DF-TRN-2026-0017).

## Unresolved questions

The questions needing the owner are OQ-01, 02, 03, 08, 12, 13 and 14 (`docs/open-questions.md`). Two of them block the start of phase 1:

- **OQ-13:** is migration in Unbound release 1?
- **OQ-14:** should Transitus live in this repository or inside Unbound?

## Risks

- **Echelon.Execution is unbenchmarked.** Load throughput is estimated at 100–800 records/s, and that figure is theoretical.
- **Single-owner maintenance capacity** (review C11). Mitigated by the three-package budget.
- **Parser libraries** are the largest attack surface (R-SEC-2).
- **Migration demand is unvalidated:** there is no design partner (OD-M-14).

## Next recommended action

1. The owner answers OQ-13 and OQ-14 and reviews the DF-TRN records.
2. Phase-1 work item 1: port the requirements renderer to F#.
3. Phase-1 work item 4: move the `Unbound.Replay` parsers into `Transitus.Formats`.

## Continuity

An executor session is disposable. Before handing off, commit and push the work. Then record a checkpoint with `./praxis work checkpoint --id ID --occurred-at NOW --summary ... --next-action ...` and push the `.ros/` state. A successor reads `./praxis work context ID --text` and takes over with `./praxis work continue`.
