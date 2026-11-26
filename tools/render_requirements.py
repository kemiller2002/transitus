"""Render the requirements register (deterministic). Usage: python3 -I tools/render_requirements.py [--check]"""
import json, sys, os, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from requirements_source import R  # noqa: E402

def _existing_provenance(rel):
    """Return the Praxis provenance block of an already-rendered file (preserved across re-renders), or ''."""
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path): return ""
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---\n"): return ""
    front = text[4:text.find("\n---\n", 4) + 1]
    i = front.find("provenance:\n")
    return front[i:] if i >= 0 else ""

def _with_provenance(head, rel):
    block = _existing_provenance(rel)
    return head.replace("(do not hand-edit)\n---\n", "(do not hand-edit)\n" + block + "---\n", 1) if block else head

def render():
    ids = [r["id"] for r in R]
    dup = [i for i, c in collections.Counter(ids).items() if c > 1]
    if dup: raise SystemExit(f"duplicate ids: {dup}")
    data = {"schema": "transitus.requirements/v1", "status": "proposed", "count": len(R), "requirements": R}
    js = json.dumps(data, indent=1, ensure_ascii=False) + "\n"
    head = "---\nid: TRN-REQ-REGISTER\ntitle: Transitus Requirements Register\nstatus: proposed\nversion: 0.1.0\ncreated: 2026-11-26\nupdated: 2026-11-26\ngenerated_by: tools/render_requirements.py (do not hand-edit)\n---\n\n"
    md = [_with_provenance(head, "requirements/REQUIREMENTS.md") + f"# Requirements register\n\n{len(R)} proposed requirements (revisions TRN-REV-01, OWNER-2026-11-26, TRN-REV-02 and DAF-P3-2026-11-26; rows carry `revision` in JSON). Phases (owner-directed revision, DF-TRN-2026-0018): 1 = minimal declarative typed linear pipeline, basic mapping packages, checkpoints/replay/idempotency, dry runs; 2 = complex DAGs and set operators (T2); 3 = advanced AI and vendor-specific packages (T3); 4 = visual editing (T4); trigger TA gates the pre-contract assessment (ASM, PRF-003) — see `docs/roadmap.md`. Priority: P0 = required for first production use, P1 = required for the phase, P2 = conditional/deferred. Machine-readable: `requirements/requirements.json`.\n"]
    for cat in dict.fromkeys(r["category"] for r in R):
        md.append(f"\n## {cat}\n\n| ID | P | Phase | Requirement | Acceptance | Verify |\n|---|---|---|---|---|---|")
        md += [f"| {r['id']} | {r['priority']} | {r['phase']} | {r['statement']} | {r['acceptance']} | {r['verify']} |" for r in R if r["category"] == cat]
    tr = [head.replace("TRN-REQ-REGISTER", "TRN-REQ-TRACE").replace("Requirements Register", "Requirements Traceability") +
          "# Requirements traceability\n\nCharter section → requirement → design → decision → verification. Charter sections refer to the initiating brief (§1–§22) captured in `PROJECT-CHARTER.md`.\n\n| Requirement | Charter | Design | Decisions | Verification |\n|---|---|---|---|---|"]
    tr += [f"| {r['id']} | {r['charter']} | {'; '.join(r['design'])} | {', '.join(r['decisions']) or '—'} | {r['verify']}: {r['acceptance']} |" for r in R]
    cov = collections.defaultdict(list)
    for r in R:
        for s in r["charter"].replace("§", "").split(","):
            cov[s.strip()].append(r["id"])
    tr.append("\n## Charter coverage\n\n| Charter § | Requirements |\n|---|---|")
    tr += [f"| §{k} | {len(v)}: {', '.join(v)} |" for k, v in sorted(cov.items(), key=lambda kv: int(kv[0]))]
    return {"requirements/requirements.json": js, "requirements/REQUIREMENTS.md": "\n".join(md) + "\n", "requirements/TRACEABILITY.md": "\n".join(tr) + "\n"}

out = render()
if "--check" in sys.argv:
    bad = [p for p, c in out.items() if not os.path.exists(os.path.join(ROOT, p)) or open(os.path.join(ROOT, p), encoding="utf-8").read() != c]
    if bad: raise SystemExit(f"stale generated files: {bad}")
    print("requirements register up to date")
else:
    for p, c in out.items():
        open(os.path.join(ROOT, p), "w", encoding="utf-8").write(c)
    print(f"rendered {len(R)} requirements")
