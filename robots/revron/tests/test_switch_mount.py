"""Every catalog power switch says how it is held: its mount holes, or [] for one made to be bonded. Missing data must
not read as "no holes" (a screwed switch would be declared glued and skip the fastener checks)."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from robot import catalog  # noqa: E402


def test_every_catalog_switch_lists_its_mount_holes():
    sw = [e for e in catalog.catalog() if e.kind == "switch"]
    assert sw and all("mount_holes_mm" in (e.props or {}) for e in sw), [e.id for e in sw if "mount_holes_mm" not in (e.props or {})]


def test_switch_without_hole_data_is_refused(monkeypatch):
    import dataclasses

    import pytest
    from revron import hw

    real = catalog.find
    monkeypatch.setattr(catalog, "find", lambda cid: dataclasses.replace(real(cid), props={}) if cid == "switch_slide_12x4" else real(cid))
    hw.switch_mount.cache_clear()
    with pytest.raises(ValueError, match="mount_holes_mm"):
        hw.switch_mount("switch_slide_12x4")
    hw.switch_mount.cache_clear()
