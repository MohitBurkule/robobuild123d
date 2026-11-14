"""waiver_audit: one inventory of EVERY opt-out a spec carries, and rules that keep the pile small, dated and honest.

A waiver is cheap to add and never removed: each check validates its own opt-out, nothing looks at them together.
`collect(spec)` returns every opt-out as a record {kind, owner, key, reason, expires, path}:

  fastener_waive      fasteners[i].waive {"<check id>": reason}                    (checks/waiver.py)
  practice_ok / geom_ok / dfm_ok   parts[i].<key> {"<check suffix>": reason}        (checks/practice.py, ...)
  sharp_corners_ok    parts[i].sharp_corners_ok "reason"                           (checks/sharp_corner.py)
  sharp_ok            sharp_ok[i] {part, near, r_mm, reason}                       (checks/sharp_corner.py)
  visual_ok           reference_cad.parts[i].visual_ok {"<check>": reason}         (checks/visual.py)
  param_exempt        param_exempt[i] {func, reason}                               (checks/param_lint.py)
  allow_overlap       allow_overlap[i] {a, b, max_depth_mm, reason}                (checks/interference.py)
  loose_ok / assembly_ok / no_contact_ok / rub_gap_ok   parts[i].<key> {..., reason}
  retained_reason     parts[i].retained + retained_reason (a hold taken on trust)  (checks/retention.py)
  thin_wall_deviation / cover_fasteners_deviation / solid_reason   parts[i].<key> "reason"
  rotor_ok / exposed_reason   wires[i].<key> "reason"                              (checks/wire_review.py)
  render_ok           render_ok[i] {file, reason}                                  (checks/wire_review.py)
  group_disabled      review.<group>.enabled: false (and root `integrity: false` / {"enabled": false})
  threshold_override  review.<group>.<threshold> (and the root `sharp_corner` / `visual` / `integrity` sections)

NOT collected (reported as an assumption): reference_cad `deviations` (blob waivers, audited by reference_cad itself)
and intent `exempt` / `gap_ok` entries.

Expiry. A record is dated by an ISO date in either form:
  * object form  {"reason": "...", "expires": "2026-12-31"}  (dict-shaped waivers such as `loose_ok` just add `expires`);
  * a trailing tag inside a plain reason string:  "... RV14 has the same play [expires 2026-12-31]"
    (works for every string-valued waiver today, with no schema change).

  waiver.no_expiry         WARNING  a record without a parsable `expires`
  waiver.expired           BLOCKER  expires < today (`review.waiver_audit.today` when set, else date.today())
  waiver.budget            WARNING  more than `review.waiver_audit.max` (25) records, or more than `max_per_part` (4)
                                    on one owner
  waiver.blanket           BLOCKER  `enabled: false` for a whole group without a reason >= 20 chars;
                           WARNING  such a switch with a reason, or a waive / *_ok key that is a bare group prefix
                                    ("joint", "fastener", "practice", "*") instead of one check id
  waiver.duplicate_reason  WARNING  the same reason text on >= 4 records
  waiver.inventory         note     counts per kind (`total=N; kind=n; ...`), metric `waiver.count`

Never passes on missing input: a section that cannot be parsed goes to ctx.not_checked and suppresses every `ok`.
Zero waivers is a judged fact and is reported as ok(`waiver.inventory`, "total=0").
"""

from __future__ import annotations

import re
from collections import Counter
from datetime import date

from ..finding import BLOCKER, WARNING, fail, note, ok

G = "waiver_audit"
MIN_REASON = 20
DEFAULT_MAX = 25
DEFAULT_MAX_PER_PART = 4
DUP_MIN = 4
EXPIRES_TAG = re.compile(r"\[\s*expires\b\s*:?\s*([^\]]*?)\s*\]", re.I)

# Part keys holding {"<check suffix>": reason}; the group each one opts out of is the key without `_ok`.
PART_CHECK_DICTS = ("practice_ok", "geom_ok", "dfm_ok")
# Part keys holding ONE waiver as an object with a `reason`.
PART_REASON_DICTS = ("loose_ok", "assembly_ok", "no_contact_ok", "rub_gap_ok")
# Part keys holding ONE waiver as a plain reason string.
PART_REASON_STRINGS = ("sharp_corners_ok", "thin_wall_deviation", "cover_fasteners_deviation", "solid_reason")
WIRE_REASON_STRINGS = ("rotor_ok", "exposed_reason")
# review sections that are not waivers at all (this group's own settings; where the reference index lives)
REVIEW_NOT_WAIVERS = ("waiver_audit", "reference_index")
# review sections whose non-`enabled` keys are run settings (time budget, workers), not thresholds of a check
REVIEW_CONFIG_ONLY = ("robust",)
# root-level sections that work like review.<group> (read with _review.resolve or their own params())
ROOT_SECTIONS = ("sharp_corner", "visual", "integrity")
SECTION_META = ("enabled", "reason", "expires")
BLANKET_KEYS = ("", "*", "all", "any")


# ------------------------------------------------------------------------------------------------ parsing
def parse_date(v):
    """datetime.date of an ISO `YYYY-MM-DD` value, else None."""
    if isinstance(v, date):
        return v
    if not isinstance(v, str):
        return None
    try:
        return date.fromisoformat(v.strip())
    except ValueError:
        return None


def split_reason(v):
    """(reason text without the expires tag, raw expires string or None) of a waiver value: a plain string, or an
    object {"reason": ..., "expires": ...}. A `[expires YYYY-MM-DD]` tag inside the reason counts when the object has no
    `expires` of its own."""
    exp = None
    if isinstance(v, dict):
        exp = v.get("expires")
        v = v.get("reason")
    text = v if isinstance(v, str) else ("" if v is None or isinstance(v, bool) else str(v))
    m = EXPIRES_TAG.search(text)
    if m:
        if exp is None:
            exp = m.group(1)
        text = text[:m.start()] + text[m.end():]
    return text.strip(), (None if exp is None else str(exp).strip())


def norm_reason(text):
    """Reason text folded for comparison (case, spacing, trailing punctuation)."""
    return re.sub(r"\s+", " ", str(text or "")).strip().strip(".!;, ").lower()


def _rec(kind, owner, key, value, path):
    reason, exp = split_reason(value)
    return {"kind": kind, "owner": str(owner or ""), "key": str(key), "reason": reason, "expires": exp, "path": path}


# ------------------------------------------------------------------------------------------------ collect
def collect(spec, problems=None):
    """Every opt-out of `spec` as records {kind, owner, key, reason, expires, path} (see the module docstring).
    `problems` (optional list) receives one string per section that could not be parsed; nothing is raised."""
    problems = problems if problems is not None else []
    raw = getattr(spec, "raw", None) or {}
    out = []

    def rows(key):
        v = raw.get(key)
        if v is None:
            return []
        if not isinstance(v, list):
            problems.append(f"`{key}` is not a list")
            return []
        return list(enumerate(v))

    for i, p in rows("parts"):
        base = f"parts[{i}]"
        if not isinstance(p, dict):
            problems.append(f"`{base}` is not an object")
            continue
        pid = p.get("id") or base
        for k in PART_CHECK_DICTS:
            v = p.get(k)
            if v is None:
                continue
            if not isinstance(v, dict):
                problems.append(f"`{base}.{k}` is not an object {{check: reason}}")
                continue
            for ck, why in v.items():
                out.append(_rec(k, pid, ck, why, f"{base}.{k}.{ck}"))
        for k in PART_REASON_DICTS:
            v = p.get(k)
            if v is None:
                continue
            if not isinstance(v, dict):
                problems.append(f"`{base}.{k}` is not an object with a `reason`")
                continue
            out.append(_rec(k, pid, k, v, f"{base}.{k}.reason"))
        for k in PART_REASON_STRINGS:
            if p.get(k) is not None:
                out.append(_rec(k, pid, k, p[k], f"{base}.{k}"))
        if p.get("retained") is not None and "retained_reason" in p:
            out.append(_rec("retained_reason", pid, str(p.get("retained")), p.get("retained_reason"), f"{base}.retained_reason"))

    for i, f in rows("fasteners"):
        base = f"fasteners[{i}]"
        if not isinstance(f, dict):
            problems.append(f"`{base}` is not an object")
            continue
        v = f.get("waive")
        if v is None:
            continue
        if not isinstance(v, dict):
            problems.append(f"`{base}.waive` is not an object {{check id: reason}}")
            continue
        for ck, why in v.items():
            out.append(_rec("fastener_waive", f.get("id") or base, ck, why, f"{base}.waive.{ck}"))

    for i, w in rows("wires"):
        base = f"wires[{i}]"
        if not isinstance(w, dict):
            problems.append(f"`{base}` is not an object")
            continue
        for k in WIRE_REASON_STRINGS:
            if w.get(k) is not None:
                out.append(_rec(k, w.get("id") or base, k, w[k], f"{base}.{k}"))

    for i, e in rows("sharp_ok"):
        if not isinstance(e, dict):
            problems.append(f"`sharp_ok[{i}]` is not an object")
            continue
        out.append(_rec("sharp_ok", e.get("part") or f"sharp_ok[{i}]", f"near={e.get('near')}", e, f"sharp_ok[{i}].reason"))

    for i, e in rows("param_exempt"):
        e = e if isinstance(e, dict) else {"func": str(e)}   # param_lint.exemptions reads a bare string the same way
        out.append(_rec("param_exempt", e.get("func") or f"param_exempt[{i}]", str(e.get("func") or ""), e,
                        f"param_exempt[{i}].reason"))

    for i, e in rows("allow_overlap"):
        if not isinstance(e, dict):
            problems.append(f"`allow_overlap[{i}]` is not an object")
            continue
        out.append(_rec("allow_overlap", e.get("a") or f"allow_overlap[{i}]", f"{e.get('a')}|{e.get('b')}", e,
                        f"allow_overlap[{i}].reason"))

    for i, e in rows("render_ok"):
        if not isinstance(e, dict):
            problems.append(f"`render_ok[{i}]` is not an object")
            continue
        out.append(_rec("render_ok", e.get("file") or f"render_ok[{i}]", str(e.get("file") or ""), e, f"render_ok[{i}].reason"))

    rc = raw.get("reference_cad")
    rparts = rc.get("parts") if isinstance(rc, dict) else rc   # reference_cad._cfg: a bare list is the parts list
    if rparts is not None and not isinstance(rparts, list):
        problems.append("`reference_cad.parts` is not a list")
        rparts = None
    for i, e in enumerate(rparts or []):
        if not isinstance(e, dict) or e.get("visual_ok") is None:
            continue
        base = f"reference_cad.parts[{i}].visual_ok"
        if not isinstance(e["visual_ok"], dict):
            problems.append(f"`{base}` is not an object {{check: reason}}")
            continue
        for ck, why in e["visual_ok"].items():
            out.append(_rec("visual_ok", e.get("part") or base, ck, why, f"{base}.{ck}"))

    def section(group, sec, path, config_only=False):
        if sec is False:   # `integrity: false`
            out.append(_rec("group_disabled", group, "enabled", None, path))
            return
        if not isinstance(sec, dict):
            problems.append(f"`{path}` is not an object")
            return
        dated = {"reason": sec.get("reason"), "expires": sec.get("expires")}
        if "enabled" in sec and not sec["enabled"]:
            out.append(_rec("group_disabled", group, "enabled", dated, f"{path}.enabled"))
        keys = sorted(str(k) for k in sec if k not in SECTION_META)
        if keys and not config_only:
            out.append(_rec("threshold_override", group, ",".join(keys), dated, path))

    review = raw.get("review")
    if review is not None and not isinstance(review, dict):
        problems.append("`review` is not an object")
        review = None
    for g, sec in (review or {}).items():
        if g in REVIEW_NOT_WAIVERS or sec is None:
            continue
        section(str(g), sec, f"review.{g}", config_only=g in REVIEW_CONFIG_ONLY)
    for g in ROOT_SECTIONS:
        if raw.get(g) is not None:
            section(g, raw[g], g)
    return out


# ------------------------------------------------------------------------------------------------ settings
def config(spec, problems=None):
    """({"max", "max_per_part", "today"}, {"budget": usable, "today": usable}) from `review.waiver_audit`."""
    problems = problems if problems is not None else []
    cfg = {"max": DEFAULT_MAX, "max_per_part": DEFAULT_MAX_PER_PART, "today": None}
    can = {"budget": True, "today": True}
    review = (getattr(spec, "raw", None) or {}).get("review")
    sec = review.get("waiver_audit") if isinstance(review, dict) else None
    if sec is None:
        return cfg, can
    if not isinstance(sec, dict):
        problems.append("`review.waiver_audit` is not an object")
        return cfg, {"budget": False, "today": False}
    for k in ("max", "max_per_part"):
        v = sec.get(k)
        if v is None:
            continue
        if isinstance(v, bool) or not isinstance(v, (int, float)) or v != v or v < 0:
            problems.append(f"`review.waiver_audit.{k}` = {v!r} is not a count >= 0")
            can["budget"] = False
        else:
            cfg[k] = int(v)
    if sec.get("today") is not None:
        d = parse_date(sec["today"])
        if d is None:
            problems.append(f"`review.waiver_audit.today` = {sec['today']!r} is not an ISO date (YYYY-MM-DD)")
            can["today"] = False
        else:
            cfg["today"] = d
    return cfg, can


def is_blanket_key(rec) -> bool:
    """True when a record's key names a whole group instead of one check id."""
    k = rec["key"].strip()
    if rec["kind"] == "fastener_waive":   # waiver._matches: a key matches its id and everything under `key.`
        return "*" in k or "." not in k.rstrip(".")
    if rec["kind"] in PART_CHECK_DICTS or rec["kind"] == "visual_ok":
        return "*" in k or k.lower() in BLANKET_KEYS or k.lower().rstrip(".") == rec["kind"][:-3]
    return False


def _where(rec):
    return f"path={rec['path']} kind={rec['kind']} owner={rec['owner']} key={rec['key']}"


def _on(rec):
    return rec["owner"] or rec["path"]


# ------------------------------------------------------------------------------------------------ audit
def audit(spec, today=None):
    """(findings, metrics, not_checked) for one spec. Pure: reads only `spec.raw` (and the clock when no `today` is
    given here or in `review.waiver_audit.today`)."""
    problems = []
    recs = collect(spec, problems)
    cfg, can = config(spec, problems)
    today = today or cfg["today"] or (date.today() if can["today"] else None)
    clean = not problems
    not_checked = [f"waiver_audit: {p}; the waivers there were not audited" for p in problems]
    by_kind = Counter(r["kind"] for r in recs)
    inv = f"total={len(recs)}" + "".join(f"; {k}={n}" for k, n in sorted(by_kind.items()))
    metrics = {"waiver.count": len(recs), "waiver.by_kind": dict(sorted(by_kind.items()))} if clean else {}
    out = []
    if not recs:
        if clean:
            out.append(ok("waiver.inventory", G, "No waivers in the spec", inv + " (every opt-out key was read; none is set)"))
        return out, metrics, not_checked
    out.append(note("waiver.inventory", G, "Waiver inventory",
                    inv + (f"; unparsed_sections={len(problems)}" if problems else "")))

    def passed(fid, title, msg, n_before):
        if clean and not any(not f.passed and f.id == fid for f in out[n_before:]):
            out.append(ok(fid, G, title, msg))

    # ---- waiver.no_expiry
    n0 = len(out)
    dated = []
    for r in recs:
        d = parse_date(r["expires"])
        if d is not None:
            dated.append((r, d))
            continue
        why = "expires=missing" if r["expires"] is None else f"expires={r['expires']!r} (not an ISO date YYYY-MM-DD)"
        out.append(fail("waiver.no_expiry", G, WARNING, "Waiver has no expiry date", f"{_where(r)} {why}")
                   .on(_on(r)).expect("expires=YYYY-MM-DD", r["expires"])
                   .fix(f"At `{r['path']}` end the reason string with ` [expires YYYY-MM-DD]` (or, where the value is an "
                        'object, add "expires": "YYYY-MM-DD"), a date by which the waiver is re-argued or removed.'))
    passed("waiver.no_expiry", "Every waiver has an expiry date", f"dated={len(dated)} of total={len(recs)}", n0)

    # ---- waiver.expired
    if today is not None:
        n0 = len(out)
        for r, d in dated:
            if d < today:
                out.append(fail("waiver.expired", G, BLOCKER, "Waiver has expired",
                                f"{_where(r)} expires={d.isoformat()} today={today.isoformat()} overdue_days={(today - d).days}")
                           .on(_on(r)).expect(f">= {today.isoformat()}", d.isoformat())
                           .fix(f"Fix what `{r['path']}` waives and delete it, or re-argue the reason and set a new "
                                "`expires` date."))
        if dated:   # with no dated record nothing was judged here (waiver.no_expiry reports them)
            passed("waiver.expired", "No waiver has expired", f"dated={len(dated)} today={today.isoformat()}", n0)

    # ---- waiver.budget
    if can["budget"]:
        n0 = len(out)
        per_owner = Counter(_on(r) for r in recs)
        if len(recs) > cfg["max"]:
            top = [o for o, _ in per_owner.most_common(5)]
            out.append(fail("waiver.budget", G, WARNING, "Too many waivers",
                            f"path=review.waiver_audit.max {inv}; max={cfg['max']}; top_owners="
                            + ",".join(f"{o}:{per_owner[o]}" for o in top))
                       .on(*top).expect(f"<= {cfg['max']}", len(recs))
                       .fix("Fix the designs the oldest waivers cover and delete them; raise `review.waiver_audit.max` "
                            "only with a written reason."))
        for owner, n in sorted(per_owner.items()):
            if n > cfg["max_per_part"]:
                mine = [r for r in recs if _on(r) == owner]
                kinds = Counter(r["kind"] for r in mine)
                out.append(fail("waiver.budget", G, WARNING, "Too many waivers on one owner",
                                f"owner={owner} count={n}; max_per_part={cfg['max_per_part']}; "
                                + "; ".join(f"{k}={c}" for k, c in sorted(kinds.items()))
                                + "; paths=" + ",".join(r["path"] for r in mine[:8]))
                           .on(owner).expect(f"<= {cfg['max_per_part']}", n)
                           .fix(f"`{owner}` is waived {n} times: redesign it so the checks pass, and delete the waivers "
                                "that no longer apply."))
        passed("waiver.budget", "Waiver count within budget",
               f"{inv}; max={cfg['max']}; max_per_part={cfg['max_per_part']}", n0)

    # ---- waiver.blanket
    n0 = len(out)
    for r in recs:
        if r["kind"] == "group_disabled":
            short = len(r["reason"]) < MIN_REASON
            out.append(fail("waiver.blanket", G, BLOCKER if short else WARNING, "Whole check group switched off",
                            f"{_where(r)} reason_chars={len(r['reason'])} min_reason_chars={MIN_REASON}: every check of "
                            f"group `{r['owner']}` is skipped")
                       .on(_on(r)).expect(f">= {MIN_REASON} chars", len(r["reason"]))
                       .fix(f"Delete `{r['path']}` and waive the ONE failing check id where it fails; if the whole group "
                            f"really cannot apply, say why in `reason` (>= {MIN_REASON} chars) next to it."))
        elif is_blanket_key(r):
            out.append(fail("waiver.blanket", G, WARNING, "Waiver names a whole group, not one check",
                            f"{_where(r)}: the key is a bare group prefix, so it waives every check under it")
                       .on(_on(r))
                       .fix(f"At `{r['path']}` replace the key `{r['key']}` with the full id of the one check being "
                            "waived (e.g. `fastener.hole_record.length`)."))
    passed("waiver.blanket", "Every waiver names one check", f"total={len(recs)}", n0)

    # ---- waiver.duplicate_reason
    n0 = len(out)
    same = {}
    for r in recs:
        t = norm_reason(r["reason"])
        if t:
            same.setdefault(t, []).append(r)
    for t, rs in sorted(same.items()):
        if len(rs) >= DUP_MIN:
            out.append(fail("waiver.duplicate_reason", G, WARNING, "Same reason pasted on many waivers",
                            f"count={len(rs)} min={DUP_MIN} reason={t[:80]!r}; paths=" + ",".join(r["path"] for r in rs[:12]))
                       .on(*sorted({_on(r) for r in rs})).expect(f"< {DUP_MIN}", len(rs))
                       .fix("Write for each waiver why THAT place is acceptable (what was measured, which reference "
                            "part shows it), or fix the shared cause once and delete them."))
    passed("waiver.duplicate_reason", "Waiver reasons are individual", f"distinct_reasons={len(same)}", n0)
    return out, metrics, not_checked


def run(ctx):
    out, metrics, not_checked = audit(ctx.r.spec)
    ctx.metrics.update(metrics)
    ctx.not_checked.extend(not_checked)
    return out
