"""Assembly instructions (D7): a build sheet from the verifier's disassembly order.

The assembly group records the greedy take-apart order (Report.assembly:
AssemblyStep(order, id, dir, travel_mm)); the build sheet is that order reversed,
with prep steps (heat-set inserts, printed parts) and a pre-flight checklist.
`steps(report_dict)` -> list of step dicts; `write(report_dict, out_dir)` -> build.md.
"""

from __future__ import annotations

DIR_NAMES = {"+x": "slide it in the +x direction", "-x": "slide it in the -x direction",
             "+y": "slide it in from the front", "-y": "slide it in from the back",
             "+z": "drop it in from the top", "-z": "push it up from below"}


def _dir_text(d):
    if not d:
        return "place it in its pocket"
    axis = max(range(3), key=lambda i: abs(d[i]))
    sign = "+" if d[axis] >= 0 else "-"
    key = f"{sign}{'xyz'[axis]}"
    return DIR_NAMES.get(key, "place it in its pocket")


def steps(report: dict, max_steps: int = 14) -> list:
    """Build steps from a report dict: prep, then the reversed disassembly order, capped at max_steps."""
    asm = sorted(report.get("assembly") or [], key=lambda s: -int(s.get("order", 0)))
    out = [{"n": 1, "title": "Print and prep the parts",
            "body": "Print the STLs (see plates.json for orientation), press any heat-set inserts with the soldering "
                    "iron, and cut the wires to the reported lengths with both ends stripped 3 mm.",
            "parts": []}]
    taken = set()
    for s in asm:
        pid = s.get("id")
        if pid in taken or len(out) >= max_steps:
            continue
        taken.add(pid)
        out.append({"n": len(out) + 1, "title": f"Fit {pid}", "body": _dir_text(s.get("dir")),
                    "parts": [pid]})
    out.append({"n": len(out) + 1, "title": "Close up and check",
                "body": "Before the first flight: all screws tight, weapon spins free by hand, pack voltage "
                        "checked with a meter, radio failsafe tested at 1 m.",
                "parts": []})
    return out


def write(report: dict, out_dir) -> dict:
    from pathlib import Path

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    st = steps(report)
    lines = ["# Build sheet", ""]
    for s in st:
        lines.append(f"{s['n']}. **{s['title']}** - {s['body']}")
    lines += ["", "## Pre-flight checklist", "",
              "- [ ] every screw present and tight",
              "- [ ] weapon spins free by hand, no rub",
              "- [ ] pack at fighting voltage, connector seated",
              "- [ ] radio failsafe stops the weapon at 1 m",
              "- [ ] mass on the scale at or under 150 g"]
    (out / "build.md").write_text("\n".join(lines) + "\n")
    return {"steps": st, "file": str(out / "build.md")}
