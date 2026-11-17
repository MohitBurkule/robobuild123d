"""Expandabot (Team Bits Everywhere, Adam Stanley) — parametric build123d model.

Entry points:
  expandabot.assembly.build(part="tub")   build one manufactured part in its own frame
  expandabot.assembly.made_parts()        all manufactured parts
  expandabot.assembly.cots()              catalogue parts with their world Locations
  expandabot.params.check()               rule / packaging assertions
"""
from .assembly import PARTS, build, cots, export, made_parts, mass_report  # noqa: F401
