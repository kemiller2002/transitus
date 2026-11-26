---
id: TRN-ARCH-05
title: Execution Model
status: proposed
version: 0.1.0
created: 2026-11-26
updated: 2026-11-26
work_item: WI-0001
decisions: [DF-TRN-2026-0006, DF-TRN-2026-0007]
depends_on: ["Echelon.Execution (incubating at kemiller2002/unbound/execution, INIT-012 RM-07)"]
---

# Execution model

## 1. Decision summary

Transitus **does not implement its own job queue, scheduler loop, lease
manager, or outbox**. It is the second consumer of `Echelon.Execution`, the
durable command execution module incubating in Unbound
(`unbound/execution/README.md`; INIT-012 RM-07; ADR-EAR-004), which states it
"can be extracted to a shared repository when a second transactional
application needs it". Transitus becoming that consumer triggers the
extraction decision; it is recorded as a cross-repository dependency
(DF-TRN-2026-0006, OQ-01) rather than performed here.

What Transitus adds on top is the **pipeline execution state machine**: how a
pipeline execution decomposes into durable commands, how chunks are
checkpointed, and how load effects are made effectively-once.

## 2. Mapping onto Echelon.Execution

| Transitus concept | Echelon.Execution construct | Request class |
|---|---|---|
| Start a pipeline execution | `Command` operation `transitus.execution.start` | `LongRunningOperation` (manual) / `ScheduledCommand` (scheduled) / `ExternalIntegrationOperation` (event-triggered) |
| Advance one stage for one chunk | `Command` operation `transitus.stage.<kind>`; `OrderingKey = executionId/stageId` for ordered stages, `executionId/stageId/chunkN` for parallel chunks | `LongRunningOperation` |
| Await approval | `AwaitingApproval approvalRef` state | `HumanApprovalWorkflow` |
| Load a batch into a destination | `Command` operation `transitus.load` with `IdempotencyKey` derived from records | `ExternalIntegrationOperation` |
| Destination returned no definitive answer | `OutcomeUnknown obligation` (never retried; resolved by verify/reconcile) | — |
| Transient failure | `RetryScheduled` with the module's backoff | — |
| Poison chunk | `Quarantined` (only that ordering key) | — |
| Cancel | `Cancelled` | — |
| Pause tenant / pipeline | `PauseScope.Tenant` / `PauseScope.Operation` | — |
| Stage completion → next stage | Outbox message → next command intake, in the same transaction as the stage's state write | — |

Port boundary (TRN-REQ-ARC-011, TRN-REV-02). The engine depends only on two ports implemented by the host:
- `IDurableCommands`: submit, await, receipts, OutcomeUnknown;
- a domain-destination port.

It neither references nor copies the Echelon.Execution assembly. A stable port contract is the precondition for extracting Echelon.Execution (owner resolution of OQ-01). Checkpoints in phase 1 are stage-granular, plus per-item intent and receipt in load (EX-005). Chunk parallelism is phase 2.

Review constraints (TRN-REV-01 C8, C9):

- Command payloads carry dataset/record references and hashes only, never personal values (TRN-REQ-EX-013), consistent with CNV-ARC-001 vault references.
- Bulk loads use a bounded share of the sponsor's queue quota at lower priority, through a separate worker role, so imports cannot throttle live donor operations (TRN-REQ-AD-011). The module's per-sponsor queue limit of 10,000 commands would otherwise let a migration starve interactive work.
- In phase 1, Echelon.Execution is used **in place** inside Unbound; extraction waits for trigger T2.

Consequences:

- Every stage transition is committed atomically with its output ledger
  rows and the outbox message that enqueues the next stage (EAR-CMD-001/-006).
- Crash anywhere ⇒ lease expiry ⇒ reclaim ⇒ the stage command re-runs; stage
  handlers are idempotent per chunk (they upsert by `(execution, stage, chunk)`).
- Per-tenant fairness and queue limits come from the module (EAR-API-009).

### Gaps in Echelon.Execution that Transitus needs (to be raised in that repository, not patched here)

| Gap | Module status (README) | Transitus need |
|---|---|---|
| G1 Lease renewal for long handlers | Not implemented | Parsing a 2 GB file chunk can exceed a fixed lease; mitigated by bounding chunk size so handler time ≪ lease. |
| G2 Automatic dependency resume (EAR-CMD-010) | Partial | Fan-in after parallel chunks. Mitigated by outbox-driven "last chunk completes the stage" counter check. |
| G3 Payload protection & retention purge (EAR-CMD-022) | Not implemented | Command payloads must carry **references** (dataset ids), never record values. |
| G4 Metrics (EAR-OBS-002) | Not implemented | Throughput/lag metrics. |

## 3. Pipeline execution state machine

```fsharp
// Illustrative only — not production code.
type ExecutionState =
    | Planned                                  // manifest bound, nothing run
    | Running of currentStages: StageId list
    | AwaitingApproval of ApprovalRequestId
    | Loading of progress: LoadProgress
    | Verifying
    | Succeeded of EvidencePackageId
    | SucceededWithExceptions of EvidencePackageId * exceptionCount: int64
    | Blocked of GateFailure                   // validation/reconciliation gate failed; nothing loaded
    | Failed of Fault                          // infrastructure/permanent error before load
    | PartiallyLoaded of LoadProgress * Fault  // load started and stopped; requires reconciliation
    | OutcomeUnknown of UnresolvedEffects      // destination ambiguity; requires resolution
    | Cancelled of reason: string
```

Legal transitions are an exhaustive pure function (following Ordo's
state-directed method and the pattern of `Echelon.Execution.Lifecycle`);
illegal transitions are unrepresentable or return `Error`.

`PartiallyLoaded` and `OutcomeUnknown` are explicit, terminal-until-resolved
states. They never become `Succeeded` without a verification/reconciliation
step that proves the destination state.

## 4. Execution modes

| Mode | Behaviour |
|---|---|
| **Manual** | Operator or API starts execution with parameters. |
| **Scheduled** | `ScheduledCommand` with `notBefore`; schedule definitions live in the pipeline (`schedule.cron`, explicit IANA zone, misfire policy `skip\|runOnce`). A tiny schedule materializer enqueues the next occurrence after each run — no separate scheduler service. |
| **Event-triggered** | A host application event (e.g. "SFTP file arrived", "domain event X") calls the Transitus API; Transitus does not poll unless the source adapter declares `discover` polling. |
| **Dry run** | Runs stages 1–9 against real or fixture input; `load` is replaced with a *plan* (`LoadPlan`) and destination adapters run in `validateOnly` mode where supported. Never writes to a system of record. Evidence is marked `dry-run`. |
| **Replay** | Re-executes a past manifest (same pipeline hash, package hashes, reference versions, raw input hash). Must produce byte-identical staged outputs (determinism check) and, if loading, identical idempotency keys. |
| **Batch / incremental** | Incremental uses adapter cursors (`Checkpoint` values: high-water mark, page token, CDC LSN, file set seen). Cursor advances **only** after the stage that consumed the data has committed. |

## 5. Chunking, checkpointing, backpressure, parallelism

- Parsers emit records in **chunks** (default 10,000 records or 16 MiB,
  whichever first). The chunk is the unit of checkpoint, retry, and
  parallelism.
- Checkpoint = (raw object hash, byte offset, record ordinal, parser state
  hash). Resuming re-opens the raw object at the offset. Formats that cannot
  seek (some XLSX, gzip streams) re-parse from the start and skip committed
  chunks by ordinal — correct but slower (documented per adapter).
- Backpressure: a stage enqueues at most `parallelism × 2` outstanding chunk
  commands; downstream lag above threshold pauses upstream intake via the
  module's pause scope.
- Resource throttling: per-pipeline `memoryBudget`, `parallelism`,
  per-destination `maxRequestsPerSecond` (token bucket in the destination
  adapter), per-tenant queue limit (module).
- Dependency ordering: stage DAG topological order; chunk parallelism only
  where the stage is declared `chunkParallel` (pure transforms, validation
  rules that are per-record); set-level stages (dedupe, aggregate, join,
  reconcile) run after a fan-in barrier.

## 6. Delivery semantics

Transitus **does not claim exactly-once delivery** to external systems.
It provides **effectively-once business outcomes** where the destination
co-operates:

1. **Deterministic idempotency keys.** For each destination record:
   `key = base32(SHA-256(tenant ‖ pipelineId ‖ destinationId ‖ naturalKey ‖ businessEffectiveDate ‖ rawInputHash?))`.
   The pipeline declares which fields form `naturalKey`; including
   `rawInputHash` is optional and decided per pipeline (a corrected re-send of
   the same business fact should usually *not* produce a new key).
2. **Destination contract.** Destination adapters declare their guarantee:

   | Guarantee | Meaning | Transitus behaviour |
   |---|---|---|
   | `idempotent-key` | Destination dedupes on supplied key (Unbound domain APIs via `Echelon.Execution` intake: EAR-API-005) | Retry freely. |
   | `natural-upsert` | Destination upserts on natural key; replays converge | Retry freely; verify by read-back. |
   | `query-before-write` | No idempotency; can check existence | Read-before-write within the ordering key; race window documented. |
   | `none` | Cannot dedupe or query (e.g. outbound file drop to a bank) | Single attempt; ambiguity ⇒ `OutcomeUnknown`; human resolution; generated files carry unique, deterministic file IDs and batch numbers so the receiver can reject duplicates. |
3. **Outbox.** Load intent is committed before the external call; the
   receipt is committed after. A crash between them yields `OutcomeUnknown`
   for that item, resolved by `verify` read-back.
4. **Reconciliation closes the loop** (TRN-ARCH-06): counts and control
   totals loaded vs. planned vs. read back.

## 7. Transaction boundaries

| Boundary | Atomic unit |
|---|---|
| Preserve | raw blob write (content-addressed, idempotent) then metadata row; orphan blobs garbage-collected |
| Stage / transform chunk | chunk rows + chunk ledger entry + exception rows + outbox(next) in one DB transaction |
| Validation / reconciliation report | report + gate result + outbox(next) |
| Approval | approval event + state transition |
| Load item | intent row (pre-call) → external call → receipt row (post-call); never one transaction across the network |
| Evidence | evidence manifest + hash-chain head |

## 8. Partial failure and exception isolation

- Record-level errors go to the **exception store** with stable code, stage,
  locator, and (classification-permitting) the offending value or its hash.
- Exception thresholds (`maxErrors`, `maxErrorRate`) are evaluated per stage;
  exceeding them fails the stage (not the process).
- Load failures for individual records do not roll back successful ones
  (external systems cannot be rolled back). The execution enters
  `SucceededWithExceptions` or `PartiallyLoaded`; remediation is a new
  execution over the exception subset (`replayExceptions`) with its own
  evidence, linked to the original.
- **Financial pipelines** default to `loadMode: all-or-nothing-plan`:
  nothing loads unless *all* validation and reconciliation gates pass for
  the whole plan. Partial loads still occur if the destination fails
  mid-way; that case is surfaced, never hidden.
- Compensation (reversing a loaded financial record) is **never automatic**;
  it is a domain action in the destination (e.g. an Unbound reversal) that
  an operator initiates.

## 9. Cancellation

Cancellation is cooperative: queued commands move to `Cancelled`; an
in-flight chunk finishes or is abandoned at lease expiry; in-flight load
items finish (their receipts are recorded) — cancellation never leaves an
unrecorded external effect.
