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

## Owner-directed revision (WI-0002, 2026-11-26)

The owner's comment on transitus#1 resolved OQ-13 (migration in release 1) and OQ-14 (independent repository), set the phase-1 scope, and resolved OQ-01/02/04/05/08/09/10/11/15. Applied:
- **Decisions:** DF-0018..0021 accepted, superseding DF-0016, 0014, 0008 and 0006.
- **Requirements:** revision passes OWNER-2026-11-26 and TRN-REV-02.
- **Schemas:** `pipeline-phase1.schema.json`, `policy:` retention, and package `scope` and `rights` fields.
- **Examples:** three demonstration pipelines and five basic packages.
- **Validator:** `tools/validate_specs.py`.
- **Challenge:** independent review TRN-REV-02.
- **Planning:** roadmap and estimates revised; unresolved conflicts UC-1..UC-16 recorded.
- **Cross-repository:** Unbound #20, daf-landscape #89 and registry #123 updated.

## DAF Landscape Phase III revision (WI-0003, 2026-11-26)

The owner strategically approved DAF Landscape DEC-001..012 on 2026-11-26. For Transitus:

- **Decisions:** DF-TRN-2026-0022..0025 record DEC-011, DEC-007, DEC-010 and DEC-012/DEC-008. Their `status` is `accepted` with `approval_stage: strategically-approved`, because Praxis allows no other DF status. No record is superseded.
- **Requirements:** revision `DAF-P3-2026-11-26` adds 19 proposed requirements (PRF-001..003, VR-014, MIG-005..007, MP-010, MET-001..003, ASM-001..008) and refines VR-010, MP-004, MIG-001 and ARC-009. The register now holds 171 requirements.
- **Trigger TA:** gates the pre-contract assessment.
- **XRI-009..014 dispositions, capability coverage and the generic/Unbound boundary:** `docs/research/03-daf-phase3-dispositions.md`.
- **Open:** OD-TRN-P3-01, OQ-17 and UC-17..19 (`docs/open-questions.md`).
- **OD-TRN-P3-02 resolved by the owner (2026-11-26, WI-0004):** the DEC-008 kill rule does not stop Transitus (DF-TRN-2026-0026).
- **Stage I review fixes (WI-0005):**
  - S1-06: phase-1 scope-impact statement in the roadmap and DF-0025/DF-0022 annotations; ARC-009 names the gated phase-1 rows.
  - S1-07: MP-010 consumes Unbound UNB-CDD-ONB-002.
  - S1-15: DEC-005 trace in the dispositions doc §7a.
- **IP note (S1-08):** owner decision OD-P3-01 / OD-DAF-IP-001 ("EF owns all property we make"). `LICENSE` names an individual as copyright holder. **TODO for counsel**; `LICENSE` is not edited (see `docs/open-questions.md`, OQ-12 note).
- **Tooling:** `tools/render_requirements.py` now preserves the Praxis provenance block of `requirements/REQUIREMENTS.md` across re-renders. Previously, re-rendering dropped it.
- **Not authorized:** expenditure, commitments, implementation. The V-4 gate is not satisfied.

## Decisions and assumptions (phase 0, as first delivered)

- ~~Phase 1 is three pure libraries (DF-TRN-2026-0016)~~. Superseded by DF-TRN-2026-0018: a minimal declarative pipeline.
- **The engine, declarative model, packages, AI and UI** wait for triggers T2, T3 and T4.
- **Echelon.Execution** is used in place inside Unbound. Extraction happens at T2 (DF-TRN-2026-0006).
- **Licence:** MIT, per the brief. The portfolio-level decision is open (OQ-12).

## Validation run

- `./praxis validate`: passed.
- `./praxis registry check`: passed.
- `python3 -I tools/render_requirements.py --check`: passed.
- `python3 -I tools/validate_specs.py`: passed (10 examples valid; 7 negative cases rejected).
- The JSON Schemas pass the Draft 2020-12 metaschema check, and the example pipeline validates against `schemas/pipeline.schema.json`.
- Not run: no .NET SDK was available here. No F# code exists in phase 0; the requirements renderer is Python by recorded deviation (DF-TRN-2026-0017).

## Unresolved questions

The questions needing the owner are OQ-01, 02, 03, 08, 12, 13 and 14 (`docs/open-questions.md`). Two of them block the start of phase 1:

- OQ-13 and OQ-14 were **resolved by the owner** (2026-11-26).
- Still open, pending evidence: OQ-03, 06, 07, 12, 16.
- Unresolved conflicts: UC-1..UC-16.

## Risks

- **Echelon.Execution is unbenchmarked.** Load throughput is estimated at 100–800 records/s, and that figure is theoretical.
- **Single-owner maintenance capacity** (review C11). Mitigated by the three-package budget.
- **Parser libraries** are the largest attack surface (R-SEC-2).
- **Migration demand is unvalidated:** there is no design partner (OD-M-14).

## Next recommended action

1. The owner reviews the `review`-status DF records and UC-1..UC-16. Unbound records the migration decision (UC-3, UC-7) and defines the canonical shape and rehearsal cell (UNB-TRN-013/014).
2. Phase-1 work item 1: port the requirements renderer to F#.
3. Phase-1 work item 4: move the `Unbound.Replay` parsers into `Transitus.Formats`.

## Continuity

An executor session is disposable. Before handing off, commit and push the work. Then record a checkpoint with `./praxis work checkpoint --id ID --occurred-at NOW --summary ... --next-action ...` and push the `.ros/` state. A successor reads `./praxis work context ID --text` and takes over with `./praxis work continue`.
