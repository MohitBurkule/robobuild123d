"""MCP stdio server (robot/mcp_server.py): protocol + tools, response caps."""

import json

from robot import mcp_server as mcp


def _rpc(method, params=None, mid=1):
    msg = {"jsonrpc": "2.0", "method": method, "id": mid}
    if params is not None:
        msg["params"] = params
    return mcp.handle(msg)


def test_initialize_and_tools_list():
    r = _rpc("initialize")
    assert r["result"]["serverInfo"]["name"] and "tools" in r["result"]["capabilities"]
    r = _rpc("tools/list")
    names = {t["name"] for t in r["result"]["tools"]}
    assert {"schema", "catalog", "validate", "explain", "diff", "guide"} <= names
    for t in r["result"]["tools"]:
        assert t["inputSchema"]["type"] == "object"


def test_notification_returns_none():
    assert mcp.handle({"jsonrpc": "2.0", "method": "notifications/initialized"}) is None


def test_validate_tool_round_trip():
    r = _rpc("tools/call", {"name": "validate", "arguments": {"design": {"weapon": {"type": "wedge"}}}})
    out = json.loads(r["result"]["content"][0]["text"])
    assert out["ok"] is True and out["hypothesis"]


def test_validate_tool_errors_are_actionable():
    r = _rpc("tools/call", {"name": "validate", "arguments": {"design": {"weapon": {"type": "wedgee"}, "nope": 1}}})
    out = json.loads(r["result"]["content"][0]["text"])
    assert out["ok"] is False and len(out["errors"]) >= 1
    assert all("code" in e and "field" in e for e in out["errors"])


def test_schema_and_explain_tools():
    r = _rpc("tools/call", {"name": "schema", "arguments": {}})
    sch = json.loads(r["result"]["content"][0]["text"])
    assert sch["required"] == ["weapon"]
    r = _rpc("tools/call", {"name": "explain", "arguments": {"id": "mass.over"}})
    assert "150 g" in r["result"]["content"][0]["text"]


def test_catalog_tool_filters():
    r = _rpc("tools/call", {"name": "catalog", "arguments": {"kind": "battery"}})
    out = json.loads(r["result"]["content"][0]["text"])
    assert out["count"] >= 1 and all(e["kind"] == "battery" for e in out["entries"])


def test_unknown_method_is_protocol_error():
    r = _rpc("no/such")
    assert r["error"]["code"] == -32601


def test_bad_tool_args_report_is_error_not_crash():
    r = _rpc("tools/call", {"name": "validate", "arguments": {"design": 42}})
    out = json.loads(r["result"]["content"][0]["text"])
    assert out["ok"] is False  # design_io treats a non-dict as bad_type, not a crash


def test_handle_garbage_json_line():
    import io

    class S(io.StringIO):
        pass

    assert mcp.handle({"jsonrpc": "2.0", "id": 7, "method": "tools/call",
                       "params": {"name": "diff", "arguments": {"a": {}, "b": {}}}})["result"]
