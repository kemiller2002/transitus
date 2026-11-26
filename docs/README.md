# Transitus documentation index

Phase 0 (research, architecture and requirements), revised per owner direction on transitus#1 (2026-11-26). No production code; implementation and merge are not authorized.

| Deliverable (brief §20) | Document |
|---|---|
| Project charter | [`../PROJECT-CHARTER.md`](../PROJECT-CHARTER.md) |
| Competitive research | [`research/01-competitive-research.md`](research/01-competitive-research.md) |
| Source register | [`research/source-register.md`](research/source-register.md) · [JSON](research/source-register.json) |
| Cross-industry use cases | [`research/02-use-cases.md`](research/02-use-cases.md) |
| DAF Landscape Phase III dispositions (XRI-009..014, pre-contract assessment, boundary) | [`research/03-daf-phase3-dispositions.md`](research/03-daf-phase3-dispositions.md) |
| Architectural principles | [`architecture/00-principles.md`](architecture/00-principles.md) |
| Pipeline specification proposal | [`architecture/01-lifecycle-and-pipeline-specification.md`](architecture/01-lifecycle-and-pipeline-specification.md) · [`../schemas/pipeline.schema.json`](../schemas/pipeline.schema.json) · phase-1 profile [`../schemas/pipeline-phase1.schema.json`](../schemas/pipeline-phase1.schema.json) · [demonstration pipelines](../examples/pipelines/) |
| Storage architecture | [`architecture/02-storage-architecture.md`](architecture/02-storage-architecture.md) |
| Adapter architecture | [`architecture/03-adapter-architecture.md`](architecture/03-adapter-architecture.md) · [`../schemas/adapter-descriptor.schema.json`](../schemas/adapter-descriptor.schema.json) |
| Transformation library specification | [`architecture/04-transformation-library.md`](architecture/04-transformation-library.md) |
| Execution model | [`architecture/05-execution-model.md`](architecture/05-execution-model.md) |
| Validation and reconciliation model | [`architecture/06-validation-and-reconciliation.md`](architecture/06-validation-and-reconciliation.md) |
| AI-assisted configuration model | [`architecture/07-ai-assisted-configuration.md`](architecture/07-ai-assisted-configuration.md) |
| Data lineage model | [`architecture/08-lineage-and-evidence.md`](architecture/08-lineage-and-evidence.md) |
| Reusable mapping packages | [`architecture/09-mapping-packages.md`](architecture/09-mapping-packages.md) · [`../schemas/mapping-package.schema.json`](../schemas/mapping-package.schema.json) · [basic packages](../examples/packages/) |
| Visual administration requirements | [`architecture/10-visual-administration.md`](architecture/10-visual-administration.md) |
| Echelon dependency analysis | [`architecture/11-echelon-dependency-analysis.md`](architecture/11-echelon-dependency-analysis.md) |
| Performance and economic models | [`architecture/12-performance-and-economics.md`](architecture/12-performance-and-economics.md) |
| Security threat model | [`security/threat-model.md`](security/threat-model.md) |
| Compliance control mapping | [`security/compliance-control-mapping.md`](security/compliance-control-mapping.md) |
| Adversarial review | [`reviews/adversarial-review.md`](reviews/adversarial-review.md) (TRN-REV-01; independent challenge of the owner-revised scope TRN-REV-02: [`adv-E`](reviews/agent-reviews/adv-E.md)) |
| Requirements register | [`../requirements/REQUIREMENTS.md`](../requirements/REQUIREMENTS.md) · [JSON](../requirements/requirements.json) |
| Requirements traceability | [`../requirements/TRACEABILITY.md`](../requirements/TRACEABILITY.md) |
| Architectural decision register | [`decisions/README.md`](decisions/README.md) |
| Open questions, owner resolutions, unresolved conflicts | [`open-questions.md`](open-questions.md) |
| Phased implementation roadmap | [`roadmap.md`](roadmap.md) |

Regenerate the requirements views with `python3 -I tools/render_requirements.py` (check mode: `--check`). Validate schemas, examples and the negative cases with `python3 -I tools/validate_specs.py`.
