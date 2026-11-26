---
id: TRN-ARCH-10
title: Visual Administration Requirements (Forma-based, future)
status: proposed
version: 0.1.0
created: 2026-11-26
updated: 2026-11-26
work_item: WI-0001
decisions: [DF-TRN-2026-0010]
---

# Visual administration requirements

## 1. Position

The administration UI is **phase 4** and optional. Everything it does must be
possible through documented APIs first (TRN-REQ-UI-010). It is built from:

- **Forma** design system components, and Forma's **portable workflow**
  capability (`forma/docs/decisions/ADR-0006-portable-workflow-capability.md`,
  `forma/src/workflow/Forma.Workflow/`, `<forma-workflow>` element) for the
  pipeline graph (view, inspect, edit, pick, runtime-visualization modes);
- **Limen** as the browser/application authority boundary (WASM-first, no
  application JavaScript outside Limen, SEC-UI-002);
- **Iter** for typed routing; URL-addressable state per Praxis SAF-URL rules;
- **Folio** for printable evidence and reconciliation reports.

Transitus does not build its own graph editor. If Forma's workflow model
cannot represent a Transitus construct (e.g. `route` partitions with a
mandatory `otherwise`), the gap is raised as a Forma requirement
(DEP-FORMA-01) rather than forked.

## 2. Single authoritative definition

The graph is a projection of the pipeline JSON. Rules:

1. The editor loads the pipeline JSON, renders via a pure projection
   `Pipeline -> WorkflowDocument`, and converts edits back via
   `WorkflowEdit -> PipelineDiff`.
2. Round-trip property (tested): `project >> edit(identity) >> unproject = id`.
3. Layout coordinates are stored as **non-semantic annotations** (excluded
   from the content hash), so moving a box never creates a new pipeline
   version.
4. There is no "export to executable" step; saving the editor *is* saving the
   JSON draft.

## 3. Required views

| View | Key requirements |
|---|---|
| Pipeline graph | stages, dependencies, branches; status overlay from executions; keyboard navigable |
| Source schema inspection | inferred schema, profile stats, detected format/version |
| Destination schema inspection | from destination `Describe` |
| Field mapping | two-column mapping table (not only drag lines), type compatibility indicators, loss warnings, AI suggestions with accept/reject per field |
| Transformation configuration | form generated from operation parameter schema + semantics docs inline |
| Data preview | paged, classification-aware masking, before/after per stage |
| Profiling | histograms, null rates, pattern summaries |
| Validation configuration | rule list with test-against-fixture |
| Reconciliation results | balanced/unbalanced, differences drill-down |
| Exception queues | grouped by code, bulk actions (fix mapping, add reference entry, accept-excluded with approval) |
| Execution history | timeline, state, counts, evidence links |
| Pipeline comparison | deterministic semantic diff of two versions, authority-envelope changes highlighted |
| Approval workflow | what is being approved (plan hash, counts, totals, differences), approve/reject with reason |
| Lineage inspection | destination record → source raw locator, pipeline version, operations |
| Resource monitoring | per execution: bytes, records/s, memory budget usage, queue lag |
| AI-assisted configuration | proposals as reviewable diffs, never auto-applied |

## 4. Accessibility and mobile

- WCAG 2.2 AA.
- **Every drag-and-drop interaction has a non-drag alternative** (WCAG 2.2
  SC 2.5.7 Dragging Movements): mapping via select lists / table rows,
  graph edits via forms ("add stage after…", "connect to…").
- Mobile: read-only graph + approvals + exception triage are first-class on
  small screens; full mapping editing is supported but optimized for
  table-based layout rather than canvas.
- Screen-reader representation of the graph is the ordered stage list with
  dependencies, which is the same structure as the JSON.

## 5. APIs

All configuration, preview, execution, approval, exception and lineage
operations are exposed through documented, versioned HTTP APIs (OpenAPI) of
the host application; the UI uses only those APIs.
