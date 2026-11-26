---
id: TRN-ARCH-07
title: AI-Assisted Configuration Model
status: proposed
version: 0.1.0
created: 2026-11-26
updated: 2026-11-26
work_item: WI-0001
decisions: [DF-TRN-2026-0012]
---

# AI-assisted configuration model

## 1. Position

AI is a **configuration author and explainer**, not a runtime component.
The runtime path (parse → transform → validate → load) contains no model
calls. This keeps results deterministic (P4) and removes model latency and
cost from per-record processing.

```
 untrusted inputs                AI assistant                 deterministic gates             runtime
 (samples, headers,   ───────▶  proposes a PipelineDiff ───▶ schema+type+policy validator ──▶ (no AI)
  docs, vendor specs)            + rationale + confidence     dry run on fixtures
                                                              authority-envelope diff
                                                              human approval
```

## 2. Capabilities and their guardrails

| Capability | Input given to the model | Output | Deterministic check |
|---|---|---|---|
| Interpret unfamiliar schemas | inferred schema, profile statistics, masked/synthetic samples, column headers | field descriptions, type suggestions | type inference re-run; profile must agree with suggested types |
| Suggest field mappings | source schema + destination schema + package catalogue | `PipelineDiff` adding `map` operations, each with rationale + confidence | type check; dry run on fixtures; reconciliation passes |
| Identify semantic mismatches | mapping + profiles | warnings (e.g. "amount appears to be in cents") | profile-based heuristics confirm (e.g. all values integers, magnitude ×100) |
| Explain source anomalies | profile + exceptions | narrative | none needed (explanatory) — labelled as AI-generated |
| Propose validation rules | profile | rule diff | rules must pass on known-good fixtures and fail on mutated fixtures |
| Generate synthetic test data | schema + constraints + profile (no real values) | fixture generator *parameters* (not raw data) | generator is deterministic given seed |
| Identify likely schema changes | previous vs new inferred schema | change classification (rename / type change / new / removed) | structural diff is computed deterministically; AI only labels likely renames |
| Explain reconciliation failures | reconciliation report | narrative + suggested causes | none (explanatory) |
| Suggest remediation | exceptions grouped by code | diff (mapping/reference data) | same as mapping |
| Produce documentation | pipeline + package | Markdown | links verified |
| Compare pipeline versions | two definitions | narrative over a deterministic diff | diff computed deterministically |
| Identify reusable mapping packages | mapping + package catalogue | candidate package + overrides | package compatibility check |

## 3. Determinism and reproducibility

- AI output becomes authoritative **only** when committed as a pipeline
  version; from then on, execution is deterministic regardless of model.
- Every AI proposal records model id, provider, prompt template version,
  input artifact hashes, and output hash, attached to the pipeline version's
  provenance (`created_by: agent`), consistent with Praxis provenance
  practice.
- Re-asking the model may produce a different proposal; that is acceptable
  because proposals are not executions.

## 4. Prompt-injection resistance

| Control | Detail |
|---|---|
| Data/instruction separation | Untrusted content is passed in delimited, typed fields (JSON with `untrusted: true` provenance tags); system prompt states that content inside them is data. |
| No tools with authority | The assistant's tool surface is read-only (read schema, read profile, read catalogue, propose diff). It cannot publish, approve, run, load, change secrets or egress. |
| Authority-envelope check | The validator rejects (or escalates to elevated approval) any diff that adds sources, destinations, egress hosts, secret slots, lowers gates, raises tolerances, adds `acknowledgeLoss`, or changes classification — regardless of who proposed it. |
| Minimized exposure | Default inputs are schema metadata and **synthetic or masked samples**. Real samples require tenant policy permitting it and a classification below `phi`/`restricted-financial` unless the tenant has approved a provider for that class. |
| Output schema | Model output must parse as `PipelineDiff` JSON; anything else is discarded. |
| Adversarial corpus | Prompt-injection fixtures (malicious headers/values) run in CI against the assistant integration; pass criterion: no authority-widening diff accepted. |

## 5. Reliability expectations

> **Revised after TRN-REV-01 C6.**
> - The evaluation (TRN-REQ-AI-008) is a **P0 gate**: AI suggestions stay disabled for a pipeline class until measured precision meets recorded thresholds (AI-009).
> - The validator also flags *semantic-critical* changes that do not widen authority: idempotency-key fields, `autoApprove` conditions, code mappings on financial fields, swapped money or date fields, and reference-data versions (PS-008).
> - Profile statistics inherit their field's classification and are masked (AI-007).
> - Non-semantic annotations are excluded from AI context (AI-003).
> - AI is a phase-3 capability gated by trigger T3.

AI mapping suggestions are treated as **drafts with measured precision**.
Phase 3 includes an evaluation harness: for each mapping package with a
human-authored ground truth, measure top-1 mapping precision/recall and
the rate at which dry-run catches wrong suggestions. Until measured,
claims about AI accuracy are not made (see adversarial review C6).

## 6. Integration point

The assistant runs in the host application, uses the host's approved model
provider (Helix Note currently calls the OpenAI API directly, `helix-note-application/api/HelixNote.AI.OpenAI.fs:110`), and is optional:
every capability above has a non-AI path (manual mapping in the editor or
API). The Forma contextual AI assistance interaction patterns
(`forma/docs/requirements/contextual-ai-assistance-interaction-patterns-2026-11-23.md`)
govern the UI.
