---
id: TRN-SEC-02
title: Compliance Control Mapping
status: proposed
version: 0.1.0
created: 2026-11-26
updated: 2026-11-26
work_item: WI-0001
frameworks: ["AICPA SOC 2 Trust Services Criteria (2017, revised points of focus 2022)", "HIPAA Security Rule 45 CFR 164.312 (Helix Note context)"]
caveat: "Mapping is a design proposal. Whether a control operates effectively is determined by an auditor; Transitus can only produce evidence."
---

# Compliance control mapping

Transitus does not make a host application compliant. It **produces
evidence automatically** for the controls it participates in, so that a
SOC 2 examination of the host (e.g. Unbound, per its SOC 2
evidence-by-design directive in `requirements/AGENT-MISSION.md`) can be
supported without manual collection. Evidence exports feed the
echelon-assurance programme and, for printable packets, Folio.

## 1. SOC 2 Trust Services Criteria

| TSC | Criterion (abridged) | Transitus control | Automated evidence produced | Req |
|---|---|---|---|---|
| CC6.1 | Logical access security over protected information | Destinations registered by host and granted per tenant; secret references only; tenant-scoped keys and RLS | Destination grant inventory per tenant; secret-slot inventory (names only); RLS policy check result | SEC-009, SEC-011, SEC-013 |
| CC6.6 | Protection against threats from outside system boundaries | Egress allow-lists; parser limits; XXE/zip-bomb defences | Egress allow-list per adapter instance; limit configuration snapshot; fuzz/abuse test results per release | SEC-002, SEC-003, SEC-015 |
| CC6.7 | Restrict transmission/movement of information | Classification ≤ destination clearance check; AI exposure gating | Publish-time validation reports showing classification checks; AI prompt-exposure log (hashes, classification) | PS-008, AI-007 |
| CC7.1 | Detect configuration changes that introduce vulnerabilities | Immutable, hashed pipeline versions; authority-envelope diff | Pipeline version history with hashes, diffs and approvers | PS-004, PS-008 |
| CC7.2 | Monitor system components for anomalies | Distribution checks, OTel metrics, OutcomeUnknown alerts | Anomaly reports; alert events | VR-001, LN-007 |
| CC7.3–7.5 | Evaluate, respond to and recover from incidents | Blocked / PartiallyLoaded / OutcomeUnknown states; replay from raw | Execution state history; recovery (replay) evidence linking original and remediation executions | EX-002, EX-007 |
| CC8.1 | Change management — authorized, tested, approved | Publish requires validation + dry run on fixtures + approval; SoD for financial/PHI | Publish record: validator version, fixture results, approver ids, second approver | PS-004, AI-002 |
| CC3.2 / CC9.2 | Risk assessment; vendor/third-party risk | Dependency pinning, SBOM, vulnerability scan; AI provider approval per tenant | SBOM per release; scan results; approved AI provider list | SEC-017, AI-007 |
| A1.2 | Recovery infrastructure / backups | Raw preservation enables re-derivation | Raw object inventory with hashes and retention | ST-001 |
| PI1.1 | Processing integrity — specifications of inputs/outputs | Versioned schemas and pipeline specs | Execution manifest (all versions/hashes) | PS-001, AI-005 |
| PI1.2 | Inputs complete and accurate | Count/control-total reconciliation of inputs | Conservation table; reconciliation reports | VR-002, VR-007 |
| PI1.3 | Processing complete, accurate, timely | Stage gates; freshness checks | Validation reports; freshness results; timings | VR-004, VR-001 |
| PI1.4 | Outputs complete, accurate, distributed only to intended parties | Post-load verification; registered destinations | Verification reports; receipts summary | VR-010, SEC-013 |
| PI1.5 | Store inputs/outputs completely and accurately | Content-addressed raw; Merkle-sealed datasets; hash-chained evidence | Raw hashes; dataset roots; chain heads | ST-001, ST-005, LN-006 |
| C1.1 / C1.2 | Confidential information identified, retained and disposed | Field classification; retention classes; purge with evidence; crypto-shredding | Retention policy snapshot; purge evidence; staging age report | SEC-012, SEC-018, ST-006 |
| P4.2 / P4.3 (Privacy) | Retain and dispose personal information | Same as C1; masking/redaction in previews/exceptions | Masking configuration; log-leak test results | LN-008 |
| CC2.1 | Information quality for internal control | Evidence packages with lineage | Evidence package per execution | LN-003 |
| CC4.1 | Monitoring activities / evaluations | Quarterly automated evidence bundle | Bundle: executions, gate overrides, exceptions aged > SLA, staging footprint | SEC-019 |

### Automated evidence bundle (TRN-REQ-SEC-019)

A scheduled `transitus.evidence.periodic` command (Echelon.Execution
`ScheduledCommand`) produces, per tenant and period:

1. All executions with final state and evidence package hashes.
2. All gate overrides with justification and approvers.
3. All pipeline publications with authority-envelope changes.
4. Exceptions aged beyond SLA and OutcomeUnknown items unresolved.
5. Staging footprint and age distribution; purge evidence summary.
6. Dependency SBOM delta and vulnerability scan status for the deployed
   Transitus version.

Output: JSON (machine-verifiable, hash-chained) + Folio-rendered PDF packet.

## 2. HIPAA Security Rule (Helix Note context)

| 45 CFR | Safeguard | Transitus contribution |
|---|---|---|
| 164.312(a)(1) | Access control | Tenant/patient scoping; registered destinations |
| 164.312(b) | Audit controls | Execution history, approval events, lineage |
| 164.312(c)(1) | Integrity | Content hashes, Merkle roots, hash-chained evidence |
| 164.312(e)(1) | Transmission security | TLS/SFTP host-key pinning; egress allow-lists |
| 164.514 | Minimum necessary (Privacy Rule context) | AI metadata-only default; masking in previews/logs |

Helix Note's own compliance posture is not established; this mapping only
records where Transitus would contribute.

## 3. Financial record-keeping (Unbound context)

Transitus ships no retention durations. Retention comes from approved classification and sponsor policy references (owner resolution of OQ-10, TRN-REQ-LN-010). The binding retention schedule is an Unbound and sponsor policy decision, configured per pipeline through policy references, and is not decided by Transitus.
