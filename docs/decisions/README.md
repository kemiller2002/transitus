# Transitus decision navigation

Canonical Decision Records live in `research/decisions/`. This directory may
contain human-oriented indexes and architectural decision views, but must not
become a second canonical decision store.

## Architectural decision register (phase 0)

All records have status `review`: the authoring agent recommends them after the adversarial review ([TRN-REV-01](../reviews/adversarial-review.md)), and acceptance is the owner's decision. Material owner decisions are listed in [`../open-questions.md`](../open-questions.md).

| Record | Type | Decision |
|---|---|---|
| [DF-TRN-2026-0001](../../research/decisions/DF-TRN-2026-0001--transitus-unique-responsibility.md) | architecture | Transitus owns only what no Echelon component provides: declarative pipeline model, transformation and check libraries, adapter contracts, raw/lineage/evidence, pipeline state machine |
| [DF-TRN-2026-0002](../../research/decisions/DF-TRN-2026-0002--canonical-json-pipeline-definition.md) | architecture | Phase-2 pipeline definitions are versioned canonical JSON (RFC 8785) interpreted against an F# discriminated-union model; published versions are immutable and identified by content hash |
| [DF-TRN-2026-0003](../../research/decisions/DF-TRN-2026-0003--flat-dag-bounded-control-flow.md) | architecture | Pipeline control flow is a flat DAG with total partitioning routes, merges, runIf over execution facts, error and retry policies — no sub-pipelines, loops or recursion |
| [DF-TRN-2026-0004](../../research/decisions/DF-TRN-2026-0004--pure-total-versioned-operations.md) | architecture | Transformations are pure, total, versioned operations with explicit culture/zone/rounding parameters, a typed total expression language, and bounded set operators |
| [DF-TRN-2026-0005](../../research/decisions/DF-TRN-2026-0005--no-user-code-governed-extensions.md) | security | No user-supplied code, SQL or script in pipelines; extension only via reviewed, signed, allow-listed compiled F# packages with capability-free signatures |
| [DF-TRN-2026-0006](../../research/decisions/DF-TRN-2026-0006--durable-execution-via-echelon-execution.md) | architecture | Durable execution uses Echelon.Execution, in place inside Unbound for phase 1; extraction to a shared component is proposed only when trigger T2 fires |
| [DF-TRN-2026-0007](../../research/decisions/DF-TRN-2026-0007--effectively-once-delivery.md) | architecture | Transitus provides effectively-once business outcomes through deterministic idempotency keys, intent/receipt recording, declared destination guarantees, OutcomeUnknown and verification — never an exactly-once claim |
| [DF-TRN-2026-0008](../../research/decisions/DF-TRN-2026-0008--storage-phasing.md) | architecture | Phase 1 owns no staging; phase-2 staging lives in the consumer's tenant schema with Strata-governed DDL, load tables, and crypto-shredding; raw blobs behind a port with a PostgreSQL default; file-backed staging only on measured need |
| [DF-TRN-2026-0009](../../research/decisions/DF-TRN-2026-0009--adapter-role-split-in-process.md) | architecture | Adapters split into transport, format and destination roles as in-process F# contracts; Singer/Airbyte protocol compatibility is not built in phase 1 |
| [DF-TRN-2026-0010](../../research/decisions/DF-TRN-2026-0010--single-authoritative-definition-ui-conditional.md) | architecture | The visual editor, if built, is a projection of the JSON definition using Forma's portable workflow capability; the administration UI is conditional on trigger T4 |
| [DF-TRN-2026-0011](../../research/decisions/DF-TRN-2026-0011--generic-reconciliation-primitives.md) | architecture | Transitus provides generic validation and reconciliation primitives with zero default monetary tolerance; accounting rules, tolerances and posting consequences stay in consumer-owned profiles |
| [DF-TRN-2026-0012](../../research/decisions/DF-TRN-2026-0012--ai-proposes-deterministic-gates-dispose.md) | architecture | AI may only propose pipeline diffs; the runtime path contains no model calls; enablement is gated on measured mapping precision |
| [DF-TRN-2026-0013](../../research/decisions/DF-TRN-2026-0013--lineage-granularity.md) | architecture | Lineage is L0 execution + L1 chunk + L2 record for system-of-record loads, with static field-level lineage per pipeline version; no per-field value storage; personal natural keys HMAC'd |
| [DF-TRN-2026-0014](../../research/decisions/DF-TRN-2026-0014--mapping-packages-configuration-only.md) | architecture | Mapping packages are configuration-only, declare their knowledge basis, require vendor licence clearance, and start as synthetic placeholders for undocumented vendors; target-side packages come first |
| [DF-TRN-2026-0015](../../research/decisions/DF-TRN-2026-0015--embedded-libraries-no-microservices-otel.md) | architecture | Transitus is distributed as F# libraries hosted by the consumer (component monolith); no microservice; operational telemetry via OpenTelemetry through the host; Vigila used only for optional follow-ups |
| [DF-TRN-2026-0016](../../research/decisions/DF-TRN-2026-0016--phase-gating-and-kill-criterion.md) | process | Phase 1 is three pure libraries (Formats, Checks, Evidence) serving Unbound release-1 feeds; later phases require recorded triggers T2-T4; a phase-1 exit review compares against hand-written per-feed modules |
| [DF-TRN-2026-0017](../../research/decisions/DF-TRN-2026-0017--phase0-tooling-python-deviation.md) | process | The phase-0 requirements renderer is a small Python standard-library script because no .NET SDK was available in the authoring environment; it is to be ported to F# in phase 1 |
