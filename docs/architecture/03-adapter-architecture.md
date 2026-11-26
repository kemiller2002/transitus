---
id: TRN-ARCH-03
title: Adapter Architecture
status: proposed
version: 0.1.0
created: 2026-11-26
updated: 2026-11-26
work_item: WI-0001
schema: schemas/adapter-descriptor.schema.json
decisions: [DF-TRN-2026-0009]
---

# Adapter architecture

Adapters are split into three independent roles, following the strongest
pattern in the market — Singer/Airbyte's separation of *transport* from
*records* and *state* (TRN-RES-01 §Airbyte, §Singer) — but implemented as
in-process F# modules instead of containers exchanging JSON over stdout.

| Role | Responsibility | Examples |
|---|---|---|
| **Transport (source)** | Discover and acquire bytes or pages; manage cursors; no parsing | local upload, SFTP, HTTPS download, REST API pager, S3/Azure Blob, database export read, event stream |
| **Format (parser)** | Bytes → typed record chunks; dialect; no I/O | CSV/TSV, fixed-width, JSON, NDJSON, XML, XLSX, Parquet, NACHA, IRS EO BMF CSV, IRS e-file 990 XML |
| **Destination** | Typed `LoadPlan` items → effects with receipts | Unbound domain API, generic REST, file drop (SFTP), staging-only sink, Summa domain API (future) |

Separating transport from format means "IRS BMF over HTTPS" and "custodian
CSV over SFTP" reuse the same CSV parser, and fixtures for parsers need no
network.

## 1. Common contract

```fsharp
// Illustrative only — not production code.
type AdapterDescriptor =
    { Id: AdapterId                         // "sftp@1"
      Role: AdapterRole                     // Transport | Format | Destination
      Version: SemVer
      ConfigSchema: JsonSchemaRef           // validated at publish
      Capabilities: Capability Set          // see §2
      Secrets: SecretSlot list              // named slots; values never in config
      Egress: EgressRequirement             // hosts/ports derived from config
      ErrorTaxonomy: ErrorClassification list
      Semantics: DocRef }

type ErrorClass =
    | Transient            // retry with backoff (timeouts, 429, 503, connection reset)
    | RateLimited of retryAfter: TimeSpan option
    | AuthFailure          // not retried; alert; credential rotation
    | PermanentInput       // bad request / unparseable — record or object level exception
    | PermanentConfig      // misconfiguration — stop the stage
    | Ambiguous            // effect may or may not have happened — OutcomeUnknown (destinations only)
```

Contracts are F# records of functions (as in `Echelon.Execution.Store`), so
adapters are pure-core/impure-shell and can be replaced by in-memory fakes
in tests.

```fsharp
type TransportAdapter =
    { Test:     Config -> Secrets -> Async<Result<ConnectionReport, AdapterError>>
      Discover: Config -> Secrets -> Checkpoint option -> Async<Result<SourceManifest, AdapterError>>
      Acquire:  Config -> Secrets -> ManifestEntry -> Async<Result<ByteSource, AdapterError>>
      Advance:  SourceManifest -> Checkpoint }                     // pure: next cursor

type FormatAdapter =
    { Sniff:    ReadOnlyMemory<byte> -> FormatGuess                // pure; used by AI/profiling
      Infer:    ByteSource -> Limits -> Async<InferredSchema>      // schema discovery
      Parse:    Dialect -> Schema -> Limits -> ByteSource -> AsyncSeq<Chunk<ParsedRecord>> }

type DestinationAdapter =
    { Describe: Config -> Async<Result<DestinationSchema, AdapterError>>   // schema discovery
      Validate: LoadItem list -> Async<ValidationResult list>               // dry-run where supported
      Load:     LoadItem list -> Async<LoadReceipt list>                    // idempotency keys inside items
      ReadBack: NaturalKey list -> Async<Result<DestinationRecord list, AdapterError>>
      Guarantee: DeliveryGuarantee }                                        // idempotent-key | natural-upsert | query-before-write | none
```

## 2. Capability discovery

Capabilities are declared (not probed at runtime) and drive validation and
UI:

`schema-discovery`, `incremental-cursor`, `cdc`, `pagination:{offset|cursor|link-header|token}`,
`rate-limit:{fixed|header-driven}`, `seekable` (resume mid-file),
`checksum-from-source`, `server-side-filter`, `dry-run`, `read-back`,
`idempotency-key`, `batch-load:{maxItems}`, `synthetic-fixture`.

A pipeline using a feature the adapter does not declare fails publish-time
validation.

## 3. Standardized behaviours

| Concern | Standard |
|---|---|
| Authentication | Secret slots resolved from the host secret provider (`ISecretProvider` port: Azure Key Vault / AWS Secrets Manager / environment for dev). OAuth2 client credentials, API key header, mTLS, SSH key with **pinned host key**, basic auth (TLS only). |
| Pagination | Adapter-owned; pages become manifest entries so each page is a checkpointable unit. |
| Rate limiting | Token bucket per adapter instance; honour `Retry-After`; per-destination `maxRequestsPerSecond`. |
| Checkpointing | `Checkpoint` is an opaque, adapter-versioned JSON value persisted with the stage commit; advanced only after downstream commit. |
| Error classification | Every adapter maps protocol errors to `ErrorClass`; unknown errors default to `Transient` for reads and **`Ambiguous` for writes**. |
| Retry | Engine-owned (Echelon.Execution backoff); adapters never loop internally. |
| Provenance | Every acquisition returns source locator, source timestamps, size, checksum (computed by Transitus; source checksum compared when supplied). |
| Connection testing | `Test` performs a non-mutating call (list, HEAD, `SELECT 1`-equivalent API, schema describe). |
| Synthetic testing | Every adapter ships a fixture generator or recorded fixtures and runs in the conformance suite against an in-memory/fake endpoint (SFTP server container only in integration tests). |

## 4. Adapter catalogue and phasing

Phasing is driven by demonstrated consumer scenarios (TRN-RES-02), not market
breadth (P12).

| Adapter | Role | Phase | Driving scenario | Library candidates (to be confirmed by ADR) |
|---|---|---|---|---|
| Local upload / host-provided stream | Transport | 1 | migrations, bulk import | none |
| HTTPS download | Transport | 1 | IRS EO BMF, Pub 78, revocation list | `System.Net.Http` |
| CSV / TSV | Format | 1 | almost all | own RFC 4180 strict parser (Unbound.Replay/Sources.fs parsing logic is prior art) or Sylvan.Data.Csv (MIT) |
| Fixed-width | Format | 1 | NACHA, legacy bank files | own (layout = schema) |
| XLSX | Format | 1 | spreadsheet administration, migrations | ExcelDataReader (MIT) or Open XML SDK (MIT) — read-only, no formula evaluation |
| JSON / NDJSON | Format | 1 | API payloads, exports | `System.Text.Json` (`MaxDepth` set) |
| Unbound domain API | Destination | 1 | all Unbound loads | via Unbound API contracts / Echelon.Execution intake |
| Staging-only sink | Destination | 1 | reference data, previews | built-in |
| NACHA | Format | 2 | ACH settlement/returns/NOC | own (NACHA rules are public; record layouts fixed-width) |
| SFTP | Transport | 2 | custodian, bank, payroll files | SSH.NET (MIT) |
| XML | Format | 2 | IRS 990 e-file, some custodians | `System.Xml` with secure settings |
| REST API pager | Transport | 2 | vendor APIs (e.g. Daffy/Endaoment-style public APIs), FHIR | `System.Net.Http` |
| S3 / Azure Blob | Transport + blob store | 3 | large files | AWS SDK / Azure SDK (only if adopted) |
| Parquet | Format | 3 | large exports | Parquet.Net (MIT) |
| Relational DB export read (PostgreSQL, SQL Server) | Transport | 3 | legacy system extracts where customer grants read access | Npgsql / Microsoft.Data.SqlClient; **read-only, parameterized, customer-granted** |
| FHIR R4 Bundle/NDJSON | Format | 3 (Helix Note) | patient-authorized imports | `System.Text.Json` + profile validation |
| Event stream (Kafka/Event Hubs) | Transport | not planned | — | deferred until a consumer demonstrates need (OQ-09) |
| CDC (Debezium-style) | Transport | not planned | — | deferred; no Echelon scenario requires log-based CDC from external systems |

Library choices are proposals; each new dependency needs an ADR per Echelon
convention, MIT/Apache-2.0 licence check and supply-chain review.

## 5. Independent connector development

Adapters are separate NuGet packages implementing the contracts in
`Transitus.Adapters.Abstractions`. The core engine depends only on the
abstractions. A connector author:

1. Implements one role.
2. Provides `AdapterDescriptor` + config JSON Schema + semantics doc.
3. Passes `Transitus.Adapters.Conformance` (error taxonomy coverage,
   checkpoint round-trip, limits enforcement, no secret leakage, determinism
   of `Parse`).
4. Is added to the host's adapter allow-list (hosts register adapters; pipelines
   cannot load arbitrary assemblies).

This satisfies "connectors developed without modifying the core" while
avoiding the Airbyte/Singer cost of a container per connector.

## 6. Initial, incremental and bidirectional integration

| Mode | Support |
|---|---|
| Initial (full) load | All adapters. |
| Incremental | Cursor-capable transports (file-set watermark, modified-since, page token). For files: "files not yet seen" by content hash + name. |
| Snapshot diff | For full-file feeds (IRS BMF monthly): Transitus computes adds/changes/removals against the previous staged snapshot by natural key — a set operation, not CDC. |
| Bidirectional | **Out of scope as a sync engine.** Outbound flows (e.g. NACHA file generation, positive-pay issue files) are separate one-directional pipelines whose source is a domain export API. No conflict-resolution/merge engine (avoids MDM scope). |
