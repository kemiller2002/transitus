"""Validate JSON Schemas and examples (deterministic). Usage: python3 -I tools/validate_specs.py"""
import glob, json, os, sys
import jsonschema
from referencing import Registry, Resource

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda p: json.load(open(os.path.join(ROOT, p), encoding="utf-8"))
base, phase1, package, adapter = (load(f"schemas/{n}.schema.json") for n in ("pipeline", "pipeline-phase1", "mapping-package", "adapter-descriptor"))
registry = Registry().with_resources([("https://echelon-foundry.dev/transitus/pipeline/1.0/pipeline.schema.json", Resource.from_contents(base)), (base["$id"], Resource.from_contents(base))])
[jsonschema.Draft202012Validator.check_schema(s) for s in (base, phase1, package, adapter)]
checks = [(f, jsonschema.Draft202012Validator(phase1, registry=registry)) for f in sorted(glob.glob(os.path.join(ROOT, "examples/pipelines/*.json")))] + \
         [(f, jsonschema.Draft202012Validator(package)) for f in sorted(glob.glob(os.path.join(ROOT, "examples/packages/*.json")))]
results = [(os.path.relpath(f, ROOT), [e.message for e in v.iter_errors(json.load(open(f, encoding="utf-8")))]) for f, v in checks]
print("\n".join(f"{'ok  ' if not errs else 'FAIL'} {f}" + "".join(f"\n     {m[:160]}" for m in errs) for f, errs in results))

# Negative cases: the phase-1 profile must reject each mutation of a valid pipeline (DF-TRN-2026-0018).
import copy
seed = json.load(open(os.path.join(ROOT, "examples/pipelines/bank-camt053-ingest.pipeline.json"), encoding="utf-8"))
def mutate(f):
    d = copy.deepcopy(seed); f(d); return d
must_reject = {
    "route stage (complex DAG, phase 2)": mutate(lambda d: d["stages"].insert(5, {"id": "split", "kind": "route", "dependsOn": ["map"], "routes": [{"name": "a", "when": "x"}], "otherwise": "b"})),
    "stage with two dependencies": mutate(lambda d: d["stages"][4].__setitem__("dependsOn", ["stage", "parse"])),
    "advisory gate": mutate(lambda d: d["stages"][6].__setitem__("gate", "advisory")),
    "invented retention duration": mutate(lambda d: d["retention"].__setitem__("raw", "P7Y")),
    "missing allowedModes": mutate(lambda d: d.pop("allowedModes")),
    "inline secret value": mutate(lambda d: d["sources"]["bank"]["secrets"].__setitem__("key", "not-a-reference")),
    "load without idempotency key": mutate(lambda d: d["stages"][8].pop("idempotencyKey")),
}
v1 = jsonschema.Draft202012Validator(phase1, registry=registry)
neg = [(name, any(True for _ in v1.iter_errors(doc))) for name, doc in must_reject.items()]
print("\n".join(f"{'ok  ' if rejected else 'FAIL'} rejects: {name}" for name, rejected in neg))
sys.exit(1 if any(errs for _, errs in results) or not all(r for _, r in neg) else 0)
