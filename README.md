# Transitus

Transitus is a proposed embeddable, AI-native data-integration engine for Echelon Foundry, written in F#. Its job is to make ingestion, transformation, migration and recurring integrations predictable, reproducible, secure and inexpensive. Unbound is the first reference application, but the design is not tied to it.

**Status: phase 0 (research, architecture and requirements).** No production code exists yet.

## What Transitus is

Transitus is a set of F# libraries hosted inside the application that uses them. It is not a separate service. Phase 1, as directed by the owner (DF-TRN-2026-0018), is a **minimal declarative typed linear pipeline** built from these stages:
- ingest;
- immutable raw evidence;
- isolated temporary staging;
- deterministic mapping;
- validation and reconciliation;
- authorization;
- domain-API load;
- post-load verification.

The engine provides checkpoints, replay, idempotency, dry runs and migration rehearsal. It ships with basic reusable mapping packages, and is built on its Formats, Checks and Evidence libraries. Durable execution is reached through host ports backed by Echelon.Execution.

Complex DAGs, advanced AI and visual editing are later phases, each gated by a recorded trigger. See [`docs/roadmap.md`](docs/roadmap.md).

## What Transitus is not

- A job queue (Echelon.Execution provides one).
- Schema governance (Strata provides it).
- A workflow designer (Forma provides one).
- An observability platform.
- A CDC or sync engine.
- A home for domain business rules.
- A separately deployed service.

## Start here

1. Read the [project charter](PROJECT-CHARTER.md).
2. Read the [documentation index](docs/README.md). It maps every deliverable in the initiating brief to the document that answers it.
3. Read the [adversarial review](docs/reviews/adversarial-review.md). It explains why phase 1 is deliberately small.
4. Read the [open questions](docs/open-questions.md). They list the decisions that need the owner.

## Machine-readable specifications

- [`schemas/pipeline.schema.json`](schemas/pipeline.schema.json) and the phase-1 profile [`schemas/pipeline-phase1.schema.json`](schemas/pipeline-phase1.schema.json). There are three demonstration pipelines in [`examples/pipelines/`](examples/pipelines/) and five basic packages in [`examples/packages/`](examples/packages/).
- [`schemas/adapter-descriptor.schema.json`](schemas/adapter-descriptor.schema.json)
- [`schemas/mapping-package.schema.json`](schemas/mapping-package.schema.json)
- [`requirements/requirements.json`](requirements/requirements.json): 152 proposed requirements.
- [`docs/research/source-register.json`](docs/research/source-register.json)

## Validation

```bash
./praxis registry check
./praxis validate
python3 -I tools/render_requirements.py --check
python3 -I tools/validate_specs.py
```

## Licence

MIT (see [LICENSE](LICENSE)), as the initiating brief directs. Per owner direction, this is to be resolved against the authoritative portfolio licensing policy before any release (OQ-12).
