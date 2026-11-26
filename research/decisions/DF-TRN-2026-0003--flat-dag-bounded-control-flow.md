---
id: DF-TRN-2026-0003
title: "Pipeline control flow is a flat DAG with total partitioning routes, merges, runIf over execution facts, error and retry policies — no sub-pipelines, loops or recursion"
status: review
decision_type: architecture
created: 2026-11-26
updated: 2026-11-26
created_by_agent: claude
confidence: high
supersedes: []
superseded_by: []
evidence: ["TRN-ARCH-01 §3", "TRN-REV-01 C3", "TRN-REV-01 C4"]
tags: [transitus]
work_item: WI-0001
provenance:
  contributions:
    EXE-20261126T151721856Z-671cd5b7:
      operations: [created]
      at: 2026-11-26T15:41:59.980Z
      actor:
        kind: agent
        id: anthropic/claude-code
        provider: anthropic
        model: unknown
        runtime: claude-code
      reason: "Transitus phase-0 decision record after adversarial review TRN-REV-01"
      evidence: [docs/reviews/adversarial-review.md]
---

# Decision Record

## Decision

Reuse happens through stage templates and packages, not nested pipelines. Routes must be total (mandatory otherwise) so record counts reconcile by construction.

## Rationale and evidence

Simplicity and analysability (P1); review C3 confirmed complexity risk; C4 showed set-level needs are met by bounded operators (DF-0004) rather than general iteration.

## Alternatives considered

Sub-pipelines/includes (deferred); general workflow engine (rejected: duplicates orchestration, ADR-EVA-001 no workflow engine).

## Status

Proposed by the authoring agent after adversarial review (TRN-REV-01); acceptance is an owner decision. Reversible: yes, through a superseding Decision Record.
