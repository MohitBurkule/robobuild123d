"""`robot mcp` stdio server (B5): the verifier as MCP tools for an LLM client.

JSON-RPC 2.0 over stdio (one JSON object per line). Tools:
  schema()                      design.json JSON Schema + buildable summary
  catalog(kind?, query?)        catalogue entries with props
  validate(design)              validate a design.json, errors in the one envelope
  explain(id)                   what a finding id means
  diff(a, b)                    two report dicts -> regression diff
  guide(section?)               the GUIDE.md text (optionally one ## section)

Responses are capped (default 16 kB) - oversize results are truncated with a
note, and catalog/validate page long output. `handle(msg)` is the testable core;
`main()` runs the stdin loop.
"""

from __future__ import annotations

import json
import sys

MAX_BYTES = 16_000
PROTOCOL_VERSION = "2024-11-05"


def _tool(name, description, props=None, required=None):
    return {"name": name, "description": description,
            "inputSchema": {"type": "object", "properties": props or {}, "required": required or []}}


TOOLS = [
    _tool("schema", "JSON Schema of design.json plus what the generator can build today"),
    _tool("catalog", "Catalogue entries; kind filters (motor, battery, esc, wheel...), query is a substring",
          {"kind": {"type": "string"}, "query": {"type": "string"}}),
    _tool("validate", "Validate a design.json; returns the hypothesis or errors in the one envelope",
          {"design": {"type": "object"}}, ["design"]),
    _tool("explain", "What a finding id means and how to act on it", {"id": {"type": "string"}}, ["id"]),
    _tool("diff", "Diff two report dicts; regressed=true when findings got worse",
          {"a": {"type": "object"}, "b": {"type": "object"}}, ["a", "b"]),
    _tool("guide", "The verifier guide (optionally one '## Section')", {"section": {"type": "string"}}),
]


def _cap(text, limit=MAX_BYTES):
    if len(text) <= limit:
        return text, False
    return text[:limit] + "\n...[truncated]", True


def _result(payload):
    return {"content": [{"type": "text", "text": payload if isinstance(payload, str) else json.dumps(payload)}]}


def _call_tool(name, args):
    from . import catalog as catalog_mod
    from .checks.explain import explain
    from .design_io import schema as schema_fn, validate
    from .diffcmd import diff_reports

    if name == "schema":
        return _result(schema_fn())
    if name == "catalog":
        rows = []
        for e in catalog_mod.catalog():
            if args.get("kind") and e.kind != args["kind"]:
                continue
            if args.get("query") and args["query"].lower() not in e.id.lower() and args["query"].lower() not in e.name.lower():
                continue
            rows.append({"id": e.id, "kind": e.kind, "name": e.name, "mass_g": e.mass_g, "props": e.props})
        text, _trunc = _cap(json.dumps(rows[:60], indent=1))
        return _result({"count": len(rows), "shown": min(len(rows), 60), "entries": json.loads(text) if not text.endswith("[truncated]") else text})
    if name == "validate":
        h, user, errors = validate(args.get("design") or {})
        return _result({"ok": not errors, "hypothesis": h.to_dict() if h is not None else None,
                        "user": user, "errors": errors})
    if name == "explain":
        return _result(explain(args.get("id", "")))
    if name == "diff":
        return _result(diff_reports(args.get("a") or {}, args.get("b") or {}))
    if name == "guide":
        from pathlib import Path

        g = Path(__file__).parent / "GUIDE.md"
        text = g.read_text()
        sec = args.get("section")
        if sec:
            parts = text.split("\n## ")
            hit = next((p for p in parts if p.lstrip("# ").lower().startswith(sec.lower())), None)
            text = hit if hit else f"no section matching {sec!r}; sections: " + ", ".join(
                p.split("\n", 1)[0].lstrip("# ") for p in parts)
        text, _trunc = _cap(text)
        return _result(text)
    return {"content": [{"type": "text", "text": f"unknown tool {name!r}"}], "isError": True}


def handle(msg: dict) -> dict | None:
    """One JSON-RPC message in, response dict out (None for notifications)."""
    method = msg.get("method", "")
    mid = msg.get("id")
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": mid, "result": {"protocolVersion": PROTOCOL_VERSION,
                "serverInfo": {"name": "robot-antweight", "version": "1.0"},
                "capabilities": {"tools": {}}}}
    if method == "notifications/initialized" or mid is None:
        return None
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": TOOLS}}
    if method == "tools/call":
        params = msg.get("params") or {}
        try:
            return {"jsonrpc": "2.0", "id": mid, "result": _call_tool(params.get("name", ""), params.get("arguments") or {})}
        except Exception as e:
            return {"jsonrpc": "2.0", "id": mid, "result": {"content": [{"type": "text", "text": f"{type(e).__name__}: {e}"}],
                    "isError": True}}
    return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"unknown method {method!r}"}}


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except ValueError:
            msg = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "parse error"}}
            sys.stdout.write(json.dumps(msg) + "\n")
            sys.stdout.flush()
            continue
        resp = handle(msg)
        if resp is not None:
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()


def add_cli(sub):
    p = sub.add_parser("mcp", help="run the MCP stdio server (JSON-RPC over stdin/stdout)")
    p.set_defaults(func=lambda a: (main(), 0)[1])
