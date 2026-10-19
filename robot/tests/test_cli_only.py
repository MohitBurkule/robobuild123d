from robot import checks, cli


def test_list_groups(capsys):
    assert cli.main(["verify", "--list-groups"]) == 0
    out = capsys.readouterr().out.split()
    assert out == [n for n, _ in checks.GROUPS]


def test_only_sets_options_and_rejects_unknown(capsys):
    a = type("A", (), {"quick": False, "fast": True, "only": "mfg, interference"})()
    assert cli.opts_from(a).only == ["mfg", "interference"]
    assert cli.main(["verify", "x.json", "--only", "nosuchgroup"]) == 1
    assert "unknown check group" in capsys.readouterr().err
