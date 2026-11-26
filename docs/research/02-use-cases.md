---
id: TRN-RES-02
title: Reference Use Cases
status: proposed
version: 0.1.0
created: 2026-11-26
updated: 2026-11-26
work_item: WI-0001
---

# Reference use cases

Each scenario is theoretical. It lists source/format, stages, domain
boundary, the Transitus capabilities exercised, and the existing consumer
requirement it serves. These scenarios are the test of genericity: a feature
is in Transitus scope only if at least two scenarios (ideally across two
applications) need it.

## A. Unbound

| # | Scenario | Source → format | Key stages / primitives | Domain boundary (stays in Unbound) | Serves |
|---|---|---|---|---|---|
| U1 | **Institutional migration** (sponsor moving from a predecessor platform) | upload / SFTP / DB export → XLSX, CSV, vendor export | preserve; parse; map with vendor package + customer overlay; `r.balance` per fund (opening balance = predecessor statement); `r.matchSets` source vs read-back; blocking gates; approval; load as `imported_unverified` | MigrationRun state machine, fencing of legacy writer, cutover, single writer, variance-power evidence (RR-REQ-X-061-r1, UNB-RCN-WF-020, RR-UNB-ACC-033-r1) | REQ-X-061, CNV-EXP-002, UNB-REM-008 |
| U2 | **IRS EO BMF ingestion** | HTTPS → CSV (4 regional files) | snapshot diff by EIN; `id.normalize(ein)`; code sets (subsection, foundation, deductibility); `r.count` vs previous ±2%; auto-approve if balanced | eligibility decisions; ObservedClaim → VerifiedFact | UNB-EXT-001, UNB-EXT-019/032/037, UNB-KNOW-023/027 |
| U3 | **Charity revocation updates** | HTTPS → auto-revocation list CSV | snapshot diff; new revocations routed to a high-priority branch; freshness check (CNV-GRT-003 fail-safe when stale) | grant hold/decline, donor notification | CNV-GRT-003, RR-REQ-X-007-r1 |
| U4 | **Custodian transaction ingestion** | SFTP → CSV/fixed-width/XML | incremental by file set; `v.sequence`; `r.controlTotal` vs trailer; `r.crossFile` positions vs transactions; idempotency key = custodian txn id + account | posting, lots, NAV | UNB-CUST-001/004/009/010/011/012, CNV-FIN-013, UNB-XIN-EVA-004/005 |
| U5 | **Investment valuation updates** | SFTP/API → CSV/JSON price files | `v.distribution` (day-over-day change > threshold → review); `v.freshness`; pricing hierarchy is reference data | pricing hierarchy decision, unitization (UNB-NAV-013) | UNB-NAV-013, UNB-INV-032 |
| U6 | **Payroll contributions** | upload/SFTP → employer CSV | `r.controlTotal` vs employer remittance; per-employee matching; rejected rows queue | contribution recognition, matching gifts (deferred OD-M-05, payroll not R1 OD-M-02) | REQ-X-070 |
| U7 | **ACH settlement** | bank SFTP → NACHA / BAI2 / camt.053 | `r.hashTotal` (NACHA entry hash), `r.controlTotal`, `r.timing` (settlement windows), `r.matchSets` vs expected settlements | settlement posting | CNV-PAY-007, UNB-XIN-BNK-003 |
| U8 | **ACH returns / NOC** | bank SFTP → NACHA returns | match on original trace + reason + return trace; NOC on trace + change code; fallback → exception queue | contribution reversal (CNV-FIN-003), NOC correction | CNV-PAY-005, CNV-PAY-002 |
| U9 | **Bulk donor import** | upload → XLSX/CSV | `dedupe`, `match@1` candidates → review (never auto-merge); address/name normalization as suggestions; dry run with preview | identity resolution policy, KYC | ADM-032, INT-014 (no dedicated requirement — gap noted, see Unbound proposal UNB-TRN-009) |
| U10 | **Historical grant migration** | vendor export → CSV/JSON; target canonical: DAF grant record v0.1 | map to `daf.grant-record`; `r.balance` (grants paid totals per fund per year); charity EIN resolution via BMF reference | historical grant facts as imported history, acknowledgments | CNV-EXP-002, UNB-XIN-EVA-009, CNV-ECO-003 (12-month shadow replay) |
| U11 | **Financial reconciliation** (month-end) | domain report API + bank/custodian files | `r.matchSets`, `r.balance`, `r.timing`; evidence via Folio | close process, write-off policy (none silent), ProvisionalCalibration (CNV-FIN-004) | CNV-FIN-004, UNB-ACC-028 |
| U12 | **Advisor relationship updates** | SCIM/HR feed or CSV | snapshot diff; scoped to (advisor, firm); removed relationships → approval | relationship authority | UNB-XIN-CRM-007, REQ-X-062 |

| U13 | **OFAC SDN screening list ingestion** | HTTPS → CSV/XML (Treasury SDN) | snapshot diff; `v.freshness` (fail-safe when stale); normalized name/alias sets as reference data | screening decisions and matching policy | Unbound release-1 screening (added after TRN-REV-01 C12) |
| U14 | **State charity registry ingestion (e.g. California AG Registry)** | HTTPS → CSV | snapshot diff by state registration id; identifier assertions | registration-status consequences | Unbound charity knowledge model (added after TRN-REV-01 C12) |
| U15 | **Positive-pay issue file (outbound)** | domain export API → bank-specified fixed-width/CSV → SFTP | one-directional outbound pipeline; deterministic file id; `r.count` and `r.controlTotal` against issued payments; destination guarantee `none` ⇒ single attempt, OutcomeUnknown on ambiguity | payment issuance | CNV-PAY-002 (added after TRN-REV-01 C12) |

**Release-1 scope note (TRN-REV-01 C12).** Unbound's own records conflict on migration. The adopted convergence clause CNV-EXP-002 (`release_scope: initial-implementation`) requires importing each donor's full fund history from the predecessor platform. The simplification discovery (`requirements/discovery/2026-11-24-simplification-economics/01-REVERSE-REQUIREMENTS-ANALYSIS.md:571`) proposes "no migration in R1" for REQ-X-061. OD-M-14 records no design partner. **Owner resolution (2026-11-26, OQ-13):** canonical historical import and migration rehearsal are required in Unbound release 1. U1/U10 are therefore in scope through the Unbound canonical historical import package. Vendor-specific turnkey packages may follow later (T3). The demonstration pipelines are `examples/pipelines/migration-rehearsal.pipeline.json` and `migration-historical-import.pipeline.json`.

### Worked example: U8 ACH returns

1. `discover` SFTP folder `/returns/` (cursor: files seen by hash).
2. `ingest` + `preserve` (raw NACHA retained per the approved financial-records policy class).
3. `parse` with `nacha.ach/parse-returns@1` (fixed-width; file/batch/entry/addenda records; blocking-factor padding validated).
4. `reconcile` blocking: `r.count` entries vs batch control; `r.hashTotal` entry hash; `r.controlTotal` debit/credit totals.
5. `transform`: `enum.map(nacha.return-reasons@2026)`; `relationship.resolve` original trace → Unbound contribution id via domain lookup API.
6. `route`: resolved → `load`; unresolved → exception queue (fallback match candidates for review, per CNV-PAY-005).
7. `authorize`: auto-approve if all reconciliations balanced and unresolved = 0; otherwise payments operations approval.
8. `load`: domain command `contribution.recordAchReturn` with idempotency key `H(tenant, returnTrace, originalTrace, reasonCode)`.
9. `verify`: read-back sample; `evidence` → Folio report "ACH returns file 2026-11-26 #2".

Unbound decides what a return *means* (reversal, donor notification, fee);
Transitus only proves the file was complete, correct, and delivered once.

## B. Helix Note

Helix Note (ledger-first evidence system for medical/legal cases; F# +
PostgreSQL/Strata + Limen/Forma; it calls the OpenAI API directly) has file extraction already
(`HelixNote.Data.FileExtraction.fs`) and explicitly keeps lab values exactly
as written with no silent unit conversion (HN-REQ-104).

| # | Scenario | Fit |
|---|---|---|
| H1 | Medical record ingestion (SMART Health Links, FHIR R4 Bundles: Condition, AllergyIntolerance, Immunization) | Good: FHIR NDJSON/Bundle format adapter + mapping package; preserve original bundle; per-resource lineage. FHIR Provenance lacks page/excerpt slots — Transitus locator (JSON pointer) fills that. |
| H2 | Laboratory result normalization | Good *if* normalization = structural (codes, LOINC mapping as reference data, units kept as written). Transitus must not convert units unless an explicit, declared, reversible operation is used — consistent with Helix Note's rule. |
| H3 | Medication history ingestion (CMS Blue Button v3 Part D claims) | Good: REST pager + FHIR ExplanationOfBenefit mapping; incremental by `_lastUpdated`. |
| H4 | Document metadata extraction | **Mostly out of scope.** OCR/NLP extraction stays in Helix Note. Transitus may ingest the *structured metadata output* and preserve source documents. |
| H5 | Patient-authorized data imports | Good: per-patient tenant/consent scope as a pipeline parameter; classification `phi`; AI assistance restricted to metadata only (T23). |

Helix Note confirms genericity for: raw preservation, JSON/FHIR formats,
exact-value preservation, lineage locators, classification-driven controls.
It does **not** need financial reconciliation primitives — which stay
optional modules.

## C. Other Echelon applications (from repository research)

| App | Scenario | Assessment |
|---|---|---|
| **Summa** (ledger/invoicing) | Opening-balance and customer/invoice migration from a prior accounting system; bank feed matching | Summa has its own `FinancialMigration.fs` and ledger reconciliation. Transitus would supply parsing/mapping/generic reconciliation and load via Summa's domain API. Second financial consumer → validates generic reconciliation primitives. |
| **Chrona** (time recording) | Import historical timesheets from CSV/XLSX exports of other tools | Small, simple; validates that a lightweight pipeline (no approval, staging-only preview → load) is cheap to author. |
| **Signal** (survey engine) | Bulk import of respondent/template data | Weak need; manual tooling likely sufficient. Not a driver. |
| **Echelon Registry** | Ingest component release manifests | Not a fit: Git/JSON native, tiny volumes. Confirms Transitus should not be forced onto every data movement. |
| **daf-landscape** research | Periodic public-data ingestion (IRS 990 data, sponsor disclosures) | Fit for U2-style public data pipelines; research scripts are Python today. Optional. |

## D. Genericity check

| Capability | U | H | Other | In core? |
|---|---|---|---|---|
| Raw preservation + content addressing | ✓ | ✓ | Summa | core |
| CSV/XLSX/JSON | ✓ | ✓ | Summa, Chrona | core |
| FHIR | — | ✓ | — | package (Helix Note-driven) |
| NACHA / BAI2 | ✓ | — | Summa (bank feeds) | package |
| Reconciliation primitives | ✓ | — | Summa | core module (optional) |
| Approval gates | ✓ | ✓ (patient consent) | Summa | core |
| Record matching / dedupe | ✓ | ✓ (patient/provider records) | — | core |
| AI mapping assistance | ✓ | ✓ (metadata only) | — | optional module |
| Visual designer | ✓ (not in R1) | — | — | conditional on trigger T4 (fails the two-scenario rule) |
| CDC / event streams | — | — | — | not built |
| Bidirectional sync | — | — | — | not built |
