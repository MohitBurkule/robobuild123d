"""`python3 -m robot eval answers_dir`: score LLM-written design.json files against robot/evals/prompts.jsonl.
UNTESTED. answers_dir/<id>.json = the LLM's design.json for prompt <id>. Scoring (validation only, no CAD build unless
--build): valid (validator agrees with expect_ok), field match (fraction of expected leaf fields equal), refusal
(for unbuildable prompts, any expected error code or a {"refuse": reason} answer)."""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).parent


def cases(path=HERE / "prompts.jsonl"):
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]


def leaves(d, pre=""):
    for k, v in (d or {}).items():
        if isinstance(v, dict):
            yield from leaves(v, f"{pre}{k}.")
        else:
            yield f"{pre}{k}", v


def get(d, dotted):
    for k in dotted.split("."):
        if not isinstance(d, dict) or k not in d:
            return None
        d = d[k]
    return d


def score_case(case, answer) -> dict:
    from .. import design_io
    if answer is None:
        return {"id": case["id"], "score": 0.0, "why": "no answer"}
    if not case["expect_ok"]:
        if isinstance(answer, dict) and "refuse" in answer:
            return {"id": case["id"], "score": 1.0, "why": "refused"}
        _, _, errs = design_io.validate(answer)
        hit = any(e["code"] in case.get("expect_error_codes", ()) for e in errs)
        return {"id": case["id"], "score": 1.0 if hit else 0.0, "why": "validator rejected" if hit else "accepted unbuildable"}
    _, _, errs = design_io.validate(answer)
    exp = dict(leaves(case["expected"]))
    match = sum(get(answer, k) == v for k, v in exp.items()) / max(1, len(exp))
    valid = not errs
    return {"id": case["id"], "score": round(0.5 * valid + 0.5 * match, 3), "valid": valid, "field_match": round(match, 3),
            "errors": [e["code"] + ":" + str(e.get("field")) for e in errs]}


def score_dir(answers_dir, build=False, out="robots/_eval") -> dict:
    rows = []
    for c in cases():
        p = Path(answers_dir) / f"{c['id']}.json"
        try:
            ans = json.loads(p.read_text()) if p.exists() else None
        except ValueError:
            ans = None
        r = score_case(c, ans)
        if build and ans is not None and c["expect_ok"] and r.get("valid"):
            from .. import build_cmd
            br = build_cmd.run(p, out, export=False)
            r["build_ok"] = br["ok"]
            r["score"] = round(r["score"] * (1.0 if br["ok"] else 0.5), 3)
        rows.append(r)
    total = sum(r["score"] for r in rows) / max(1, len(rows))
    return {"score": round(total, 3), "n": len(rows), "cases": rows}


def cli(a):
    res = score_dir(a.answers, build=a.build)
    print(json.dumps(res, indent=1) if a.json else f"eval score {res['score']:.3f} over {res['n']} prompts")
    if not a.json:
        for r in res["cases"]:
            if r["score"] < 1:
                print(f"  {r['id']}: {r['score']} {r.get('why') or r.get('errors')}")
    return 0


def add_cli(sub):
    p = sub.add_parser("eval", help="score LLM design.json answers against robot/evals/prompts.jsonl")
    p.add_argument("answers")
    p.add_argument("--build", action="store_true", help="also generate+verify each valid answer (slow)")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cli)
