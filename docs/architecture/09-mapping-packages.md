---
id: TRN-ARCH-09
title: Reusable Mapping Packages
status: proposed
version: 0.1.0
created: 2026-11-26
updated: 2026-11-26
work_item: WI-0001
schema: schemas/mapping-package.schema.json
decisions: [DF-TRN-2026-0014]
---

# Reusable mapping packages

## 1. What a package is

A **mapping package** is a versioned, content-hashed bundle of *configuration
only* — never data, never code:

```
irs.eo-bmf/2.1.0/
  package.json            id, version, publisher, licence, compatibility, hashes
  schemas/                source schemas (with version ranges they accept)
  templates/              stage templates (parse dialects, transforms)
  mappings/               source schema → target schema mappings
  reference/              code sets (e.g. NTEE codes, IRS subsection codes, ACH return codes)
  validation-profiles/    rule sets
  reconciliation-profiles/
  fixtures/               synthetic inputs + expected outputs (+ generator params)
  docs/                   AI-readable semantics, provenance of the format knowledge
  CHANGELOG.md
```

Packages are referenced by pipelines with a semver range and pinned hash at
publish time. A customer's pipeline = base package + **overlay** (customer
configuration: column renames, extra code mappings, stricter rules). Overlays
are declarative patches (JSON Merge Patch restricted to allowed paths) —
never forks (TRN-REQ-MP-003).

## 2. Provenance of format knowledge (no invented vendor schemas)

Each package states the basis of its schema knowledge:

| Basis | Allowed content |
|---|---|
| `public-specification` | Published standards/specs (IRS EO BMF layout, NACHA Operating Rules record formats, FHIR R4, ISO 20022) |
| `public-api-documentation` | Vendor's publicly documented API/export (e.g. Daffy public API docs, Chariot grant API) |
| `customer-authorized-sample` | Derived from a sample a customer authorized for this purpose; the package contains the **schema** and **synthetic** fixtures only, never the sample |
| `synthetic-representation` | Explicitly fictional layout for testing; marked so it can never be mistaken for a vendor schema |

Packages for proprietary systems with no public documentation (Ren/iPhi
DFX, TIFIN Give, GiftingNetwork, DAFtech, Blackbaud FIMS/DonorCentral,
Foundant) start as **`synthetic-representation` skeletons** describing the
*target-side* canonical shape (Unbound fund/contribution/grant/advisor model,
plus the public DAF grant record standard in
`daf-landscape/standards/daf-grant-record/schema-v0.1.json`) and become real
only when a customer-authorized export sample exists. daf-landscape research
confirms no public export schemas for these vendors.

## 3. Unbound package catalogue (proposed)

| Package | Basis available today | Status |
|---|---|---|
| `irs.eo-bmf` | public-specification (IRS EO BMF extract) | buildable now; Unbound.Replay/Sources.fs parser is prior art |
| `irs.pub78` | public-specification | buildable now |
| `irs.auto-revocation` | public-specification | buildable now |
| `irs.990-efile` (Schedule D / I subsets) | public-specification (IRS e-file XML schemas) | buildable now |
| `nacha.ach` (entries, returns R01–R85, NOC C01–C13) | public-specification (NACHA Operating Rules — licence terms of the rules text to be checked; layouts widely published) | buildable now; returns/NOC are CNV-PAY-005 |
| `bank.bai2` / `iso20022.camt053` | public-specification | phase 2 (bank activity, CNV-PAY-007) |
| `custodian.generic-positions-transactions` | synthetic-representation + customer samples | skeleton |
| `payroll.generic-contributions` | synthetic-representation | skeleton (payroll not in R1, OD-M-02) |
| `daf.grant-record` | public (daf-landscape standard v0.1) | buildable now |
| `spreadsheet.admin` (generic fund/donor/grant workbook) | synthetic-representation | skeleton; primary path for small sponsors |
| `vendor.ren-iphi`, `vendor.tifin-give`, `vendor.giftingnetwork`, `vendor.daftech`, `vendor.cf-fims`, `vendor.foundant` | none public | placeholder only until a customer-authorized sample |
| `bank.custom` | per-customer overlay on `spreadsheet.admin`/fixed-width | overlay pattern |

## 4. Compatibility and upgrades

- Source schemas declare `accepts: ["2024.*"]`-style version ranges and
  **detectors** (header signature, column set) so a new vendor export version
  is detected as `compatible`, `compatible-with-warnings` (new optional
  columns), or `incompatible`.
- Package semver: patch = docs/fixtures; minor = additive mappings/codes;
  major = changed semantics. Pipelines pin major.
- Upgrade path: `transitus package upgrade --dry-run` re-runs the pipeline's
  fixtures and the last N executions' raw inputs (replay, staging-only sink)
  against the new version and produces a deterministic diff of outputs before
  any switch.

## 5. Learning across migrations without leaking customer data

Improvements flow back as **configuration**, not data:

1. A migration engineer resolves exceptions for customer A by adding a code
   mapping or a detector rule in the customer overlay.
2. A promotion review asks: is this rule general (true of the vendor format)
   or customer-specific (customer's own codes)? Only general rules are
   promoted to the base package.
3. Promotion carries **no values** from customer data: fixtures are
   regenerated synthetically; code sets are promoted only if they are
   vendor-defined (e.g. a vendor's status enumeration) not customer-defined.
4. The promotion is a pull request against the package repository with
   provenance `derived-from: customer-overlay@hash` (no content), reviewed
   by a second person for disclosure risk.
5. Aggregate metrics (exception codes per package version, auto-match rate)
   are tracked to show packages improving over time.
