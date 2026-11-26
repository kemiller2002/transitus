---
id: TRN-ARCH-04
title: Transformation Library Specification
status: proposed
version: 0.1.0
created: 2026-11-26
updated: 2026-11-26
work_item: WI-0001
requirements: [TRN-REQ-TX-001, TRN-REQ-TX-002, TRN-REQ-TX-003, TRN-REQ-TX-004, TRN-REQ-TX-005, TRN-REQ-TX-006, TRN-REQ-TX-007, TRN-REQ-TX-008]
decisions: [DF-TRN-2026-0004, DF-TRN-2026-0005]
---

# Transformation library specification

Transitus transformations are **pure, total, deterministic functions** from a
typed input value (plus explicitly versioned reference data and execution
parameters) to a typed `Result`. They never perform I/O, never read the clock,
never read ambient culture, and never throw for data-dependent reasons. Every
failure is a value (`TransformError`) carrying a stable error code.

This document is a specification for phase 2. No production code exists.

## 1. Contract shared by every operation

```fsharp
// Illustrative only — not production code.
type Reversibility =
    | Reversible            // an inverse exists and is documented (e.g. trim is NOT; base64 is)
    | ReversibleWithKey     // inverse requires a governed key (tokenization, encryption)
    | Irreversible          // information is destroyed (hashing, masking, redaction, rounding)

type Determinism =
    | Pure                  // depends only on input + declared parameters
    | ReferenceBound of ReferenceSetId   // also depends on a pinned reference-data version

type OperationDescriptor =
    { Id: OperationId                    // e.g. "text.trim@1"
      InputType: FieldType
      OutputType: FieldType
      Parameters: ParameterSchema list
      Reversibility: Reversibility
      Determinism: Determinism
      MayLoseInformation: bool           // true => requires explicit `acknowledgeLoss` in the pipeline
      Errors: ErrorCode list             // exhaustive list of codes it may return
      Semantics: DocRef }                // link to normative documentation (AI-readable)

type Transform = Value -> Result<Value, TransformError>
```

Rules (normative):

1. **Versioned identity.** Every operation is addressed as `name@major`.
   Behavioural change requires a new major; a pipeline pins the major it was
   validated against (TRN-REQ-TX-001).
2. **Totality.** An operation returns `Ok` or `Error`; it never throws,
   never returns `null`, and never partially writes (TRN-REQ-TX-002).
3. **No ambient state.** Culture, locale, time zone, rounding mode, and
   Unicode normalization form are explicit parameters with no defaults taken
   from the host (TRN-REQ-TX-003).
4. **Loss is declared.** Any operation whose `MayLoseInformation = true`
   (truncate, round, mask, redact, hash, lossy cast) is rejected by the
   pipeline validator unless the step carries `acknowledgeLoss` with a reason
   and, for fields classified `financial`, an approval reference
   (TRN-REQ-TX-004, TRN-REQ-VR-009).
5. **Financial values are never silently altered.** `decimal` → `decimal`
   conversions that change scale fail with `PRECISION_LOSS` unless an explicit
   rounding operation with a declared mode is used; floating point types are
   forbidden for fields typed `Money` or `Decimal` (TRN-REQ-TX-005).
6. **Null is explicit.** Inputs are `Present v | Missing | ExplicitNull`.
   Operations declare per-case behaviour; nothing coalesces silently
   (TRN-REQ-TX-006).
7. **Reference data is pinned.** Lookups use `ReferenceSetId@version`, hashed
   into the execution manifest so a replay is reproducible (TRN-REQ-TX-007).
8. **Composition.** Operations compose only through the pipeline expression
   language (`TRN-ARCH-01 §5`); there is no user-supplied code path
   (TRN-REQ-PS-006).

## 2. Value model

| Type | Representation | Notes |
|---|---|---|
| `Text` | UTF-8 string, validated scalar values | Normalization form recorded in schema; ill-formed UTF-8 is a parse error, never replaced silently. |
| `Integer` | 64-bit signed; `BigInteger` opt-in | Overflow is `OVERFLOW`, never wraps. |
| `Decimal(p,s)` | `System.Decimal` (28-29 significant digits) | Precision/scale declared in schema; values exceeding p fail. |
| `Money(currency, scale)` | `Decimal` + ISO 4217 code | Scale defaults to ISO 4217 minor units for that currency, overridable only by declaration. No implicit currency conversion. |
| `Date` | `DateOnly` (proleptic Gregorian) | No time zone. |
| `LocalDateTime` | `DateTime` with `Kind=Unspecified` | Must be paired with a zone before becoming an instant. |
| `Instant` | `DateTimeOffset` normalized to UTC | Original offset retained in lineage when source supplied one. |
| `Boolean` | true/false | Parsing vocabulary is a declared parameter. |
| `Enum(setId@v)` | code from a versioned code set | Unknown code is an error unless `onUnknown` is declared. |
| `Identifier(kind)` | normalized string | e.g. `ein`, `routing-number`, `iban`, `npi`, `uuid`. |
| `Binary` | bytes + media type | Only produced by parsers; not transformable except hash/tokenize. |
| `Record` / `List` | nested | For JSON/XML hierarchies; flattened through explicit `unnest`. |

## 3. Standard operation catalogue (v1 proposal)

`R` = reversible, `K` = reversible with key, `I` = irreversible. "Loss" means
`MayLoseInformation`.

### 3.1 Text and Unicode

| Operation | Rev | Loss | Semantics |
|---|---|---|---|
| `text.trim@1` (`mode: both\|start\|end`, `chars: unicode-whitespace\|ascii-whitespace\|explicit`) | I | no* | Removes characters in the declared class. *Whitespace removal is treated as non-material by default; a schema may mark a field `whitespaceSignificant` to force acknowledgement. |
| `text.collapseWhitespace@1` | I | no* | Replaces runs of the declared class with one U+0020. |
| `text.normalizeUnicode@1` (`form: NFC\|NFD\|NFKC\|NFKD`) | I | NFKC/NFKD yes | NFKC/NFKD are compatibility decompositions and can change meaning (e.g. `ﬁ` → `fi`, superscripts) — therefore declared loss. |
| `text.case@1` (`to: upper\|lower\|title`, `culture: invariant\|<bcp47>`) | I | yes | Culture explicit (Turkish dotless i). Title-casing is never applied to identifiers. |
| `text.replace@1` (`literal` or `pattern` with RE2-subset, bounded) | I | yes | Regex engine must be linear-time (non-backtracking `RegexOptions.NonBacktracking`) with a match timeout. |
| `text.pad@1`, `text.substring@1` | I | substring yes | `substring` beyond bounds → `OUT_OF_RANGE`, never clamps silently. |
| `text.split@1` (`separator`, `expect: n`, `onMismatch`) | R (with `join`) | no | Count mismatch is an error unless policy says otherwise. |
| `text.concat@1` (`separator`, `nullPolicy`) | I | no | Null policy mandatory. |
| `text.length.require@1` (`max`) | — | — | Validation, never truncation. Truncation is only `text.truncate@1` with `acknowledgeLoss`. |

### 3.2 Numbers, decimals and money

| Operation | Rev | Loss | Semantics |
|---|---|---|---|
| `number.parse@1` (`culture`, `groupSeparator`, `decimalSeparator`, `allowExponent=false`, `negative: minus\|parentheses\|trailing-minus`) | R | no | Exact parse to `Decimal`; rejects ambiguous inputs like `1,234` when culture is not declared. |
| `money.parse@1` (`currency` fixed or from field, `scale`) | R | no | Rejects more fractional digits than scale (`PRECISION_LOSS`). Currency symbols are not interpreted unless a symbol→ISO map is declared. |
| `decimal.round@1` (`scale`, `mode: half-even\|half-up\|half-down\|floor\|ceiling\|truncate`) | I | yes | Only way to reduce scale. `acknowledgeLoss` mandatory; financial fields need approval reference. |
| `decimal.rescale@1` (increase only) | R | no | Adds trailing zeros. Decrease → error. |
| `math.eval@1` (expression over + − × ÷, min, max, abs, with declared result scale and rounding) | I | when rounding | Division always requires a declared scale and rounding mode; divide-by-zero → `DIVIDE_BY_ZERO`. No exponentiation, no floats. |
| `money.allocate@1` (`parts` or `weights`, `remainderPolicy: first\|last\|largest-remainder`) | R (sum preserved) | no | Splits an amount so the parts sum exactly to the total; residual pennies allocated by declared policy. |
| `money.assertCurrency@1` | — | — | Fails if currency differs. There is **no** FX conversion operation in v1 (open question OQ-11). |

### 3.3 Dates, times and zones

| Operation | Rev | Loss | Semantics |
|---|---|---|---|
| `date.parse@1` (`formats: [..]` explicit list, `culture`, `century pivot` explicit) | R | no | Ambiguous formats (e.g. `01/02/2026` with both `MM/dd` and `dd/MM` listed) → `AMBIGUOUS_DATE` unless an ordered preference is declared. |
| `datetime.parseLocal@1` | R | no | Produces `LocalDateTime`. |
| `datetime.assignZone@1` (`zone: IANA id`, `tzdbVersion`, `onGap: reject\|shift-forward`, `onOverlap: reject\|earlier\|later`) | R | no | DST gaps and overlaps are explicit; tzdb version is pinned reference data. |
| `instant.toZone@1` | R | no | Presentation conversion. |
| `date.businessDay@1` (`calendar: setId@v`, `direction`) | I | no | Calendar is reference data (e.g. Federal Reserve holiday calendar for ACH settlement dates). |
| `date.serialExcel@1` (`epoch: 1900\|1904`) | R | no | Excel serial dates; the 1900 leap-year bug handled explicitly. |

### 3.4 Codes, identifiers and addresses

| Operation | Rev | Loss | Semantics |
|---|---|---|---|
| `enum.map@1` (`codeSet@v`, `onUnknown: error\|quarantine\|default(value)`) | R if bijective | no | Many-to-one mapping flagged `I` automatically by the validator. |
| `id.normalize@1` (`kind: ein\|routing-number\|iban\|npi\|ssn-last4\|uuid\|custom(setId)`) | I | no | Removes formatting, validates check digits (ABA routing checksum, IBAN mod-97, NPI Luhn). Invalid → error, never "fixed". |
| `address.normalize@1` (`country`, `ruleset@v`) | I | yes | Structural normalization only (casing, abbreviations from a pinned ruleset such as USPS Publication 28 suffixes). Postal *validation* (CASS) is an adapter-level, optional, external service and is never implicit. |
| `name.parse@1` | I | yes | Optional; heuristic, so outputs are **suggestions** that must be approved when used for matching. |

### 3.5 Structural and null handling

| Operation | Semantics |
|---|---|
| `field.default@1` (`when: missing\|null\|missing-or-null`, `value`) | Default must be type-correct; defaults on financial fields require `acknowledgeLoss`-style justification (`acknowledgeDefault`). |
| `field.require@1` | Missing/null → error. |
| `field.coalesce@1` (ordered fields) | Records which source supplied the value in lineage. |
| `record.unnest@1` / `record.nest@1` | Explicit flattening of hierarchical inputs; cardinality expectations declared. |
| `when@1` (condition, then, else) | Conditional mapping; conditions use the expression language (§5 of TRN-ARCH-01), not code. |

### 3.6 Set operations (operate on staged datasets, not single values)

| Operation | Semantics |
|---|---|
| `lookup@1` (`referenceSet@v` or staged dataset, key, `onMiss`, `onMultiple`) | Multi-match is an error by default. |
| `join@1` (`inner\|left\|anti\|semi`, keys, `expectCardinality: 1:1\|1:n\|n:1`) | Cardinality violation is a blocking error; full outer and cross joins are excluded in v1. |
| `aggregate@1` (group keys, `sum\|count\|min\|max\|first-by(order)`) | `sum` on Money requires a single currency per group. `avg` excluded (forces division semantics; use `math.eval`). |
| `filter@1` (predicate, `rejectedTo: quarantine\|discard-with-count`) | Discards are counted and reported; `discard` without count is impossible by construction (TRN-REQ-VR-007). |
| `dedupe@1` (key, `keep: first-by(order)\|reject-all`) | Removed duplicates are written to the exception store with the surviving record's id. |
| `match@1` (deterministic rules, optional similarity with threshold) | Produces **match candidates** with scores; above an "auto" threshold they may link, between thresholds they go to review, never auto-merge financial entities (TRN-REQ-TX-008). |
| `relationship.resolve@1` (natural key → destination id via destination adapter lookup or staged map) | Unresolved references are exceptions, not nulls. |

### 3.7 Privacy operations

| Operation | Rev | Semantics |
|---|---|---|
| `privacy.mask@1` (`keepLast: n`, `char`) | I | Display-grade only. |
| `privacy.redact@1` | I | Replaces with a typed `Redacted` marker, not an empty string. |
| `privacy.hash@1` (`algorithm: sha256\|hmac-sha256`, `keyRef` for HMAC) | I | Unkeyed SHA-256 is **forbidden** for low-entropy identifiers (SSN, phone, EIN) because it is trivially reversible by enumeration; HMAC with a tenant-scoped key is required. |
| `privacy.tokenize@1` (`vault: keyRef`, `format-preserving: bool`) | K | Tokens are reversible only through the governed vault (secret store integration via Limen/host); detokenization is an authorized, audited operation. |
| `privacy.generalize@1` (date → month/year, zip → zip3) | I | For analytics/evidence exports. |

## 4. Precision, culture, locale and time-zone policy

- The pipeline header declares `defaults.culture`, `defaults.timeZone`,
  `defaults.unicodeForm`; operations may override per step. A pipeline with
  no declared default and an operation that needs one fails validation.
  The host's `CultureInfo.CurrentCulture` and local time zone are never used.
- `System.Decimal` is the only numeric type for money. Its 96-bit mantissa
  covers ±7.9×10^28; values outside the declared precision fail.
- IANA tzdb version and ISO 4217 table version are pinned reference sets
  recorded in the execution manifest.

## 5. Extension mechanism

New operations are added only as **reviewed, compiled F# modules** that
implement `OperationDescriptor` + `Transform`, ship in a signed/hashed
assembly in an approved package, and pass the conformance suite
(determinism property tests, totality fuzzing, documentation completeness).
Pipelines reference them by `package/name@major`. There is no runtime
script, SQL, or JavaScript evaluation (DF-TRN-2026-0005, TRN-REQ-PS-006).

## 6. Conformance tests required per operation (phase 2)

1. Property: same input + parameters ⇒ identical output (run twice, different
   processes, different host cultures and `TZ`).
2. Property: no exception for arbitrary input (FsCheck generators per type).
3. Golden fixtures: documented examples in the semantics page are executed.
4. Reversible operations: `inverse(op(x)) = x` property.
5. Loss declaration: a mutation test proves any scale/length reduction is
   either rejected or flagged.
