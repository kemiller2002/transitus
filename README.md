# Transitus

Transitus is a proposed embeddable, AI-native data-integration engine for Echelon Foundry, written in F#. Its job is to make ingestion, transformation, migration and recurring integrations predictable, reproducible, secure and inexpensive. Unbound is the first reference application, but the design is not tied to it.

**Status: phase 0 (research, architecture and requirements).** No production code exists yet.

## What Transitus is

Transitus is a small set of F# libraries hosted inside the application that uses them:

- **Formats** parse files strictly, within resource limits.
- **Checks** validate and reconcile the data.
- **Evidence** preserves raw input, records lineage, derives idempotency keys and assembles an evidence package.

It loads data only through the consuming application's domain operations, using the durable command path provided by Echelon.Execution.

Later phases are each gated by a recorded trigger. They add a declarative pipeline model and engine, mapping packages, AI-assisted configuration, and a Forma-based administration UI. See [`docs/roadmap.md`](docs/roadmap.md).

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

- [`schemas/pipeline.schema.json`](schemas/pipeline.schema.json): the phase-2 pipeline definition. [Example](examples/pipelines/irs-eo-bmf-ingest.pipeline.json).
- [`schemas/adapter-descriptor.schema.json`](schemas/adapter-descriptor.schema.json)
- [`schemas/mapping-package.schema.json`](schemas/mapping-package.schema.json)
- [`requirements/requirements.json`](requirements/requirements.json): 136 proposed requirements.
- [`docs/research/source-register.json`](docs/research/source-register.json)

## Validation

```bash
./praxis registry check
./praxis validate
python3 -I tools/render_requirements.py --check
```

## Licence

MIT (see [LICENSE](LICENSE)), as the initiating brief directs for public repository content. The portfolio-level licence decision is open (OQ-12).
