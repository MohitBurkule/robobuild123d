"""Entry point: `robot doctor` must run even when trimesh etc. are missing (cli.py imports them at module level)."""

import sys


def main(argv=None):
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] == "doctor":
        import argparse

        from . import doctor

        ap = argparse.ArgumentParser(prog="robot")
        sub = ap.add_subparsers(dest="cmd")
        doctor.add_cli(sub)
        a = ap.parse_args(args)
        return a.func(a)
    from .cli import main as cli_main

    return cli_main(argv)
