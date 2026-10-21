"""Deliberate departures from the original RVRN 2.0 (tub-adjacent parts), all OFF by default.

User rule: first 100 % parity with the original, then improve. The default build is the dump/STEP geometry; every design
improvement is a named switch here. Override with the env var REVRON_VARIANTS="battery_pad,esc_tray" (or "all") before
import, or at run time with set_variants("battery_pad", ...) / set_variants() to reset; then regenerate the spec.

  battery_pad   foam tape pad under the pack (original: pack floats 2 mm over the base panel skin, held by bay + deck)
  esc_tray      TPU weapon-ESC tray glued to the base panel (original: wesc held by kapton alone, no tray)
  rxesc_strap   6 mm TPU strap over the Malenki (original: kapton to the deck); retained="strap"
  base_csk_fit  base panel M2 countersinks opened to seat the 4.4 mm ISO head (original RV26 seat: dk 3.2, 0.5 deep)
  top_screws    4 M2x5 thread-forming screws through the Ti top panel (original: panel bonded on the deck, no screws)
"""
import os

NAMES = ("battery_pad", "esc_tray", "rxesc_strap", "base_csk_fit", "top_screws")
VARIANTS = {n: False for n in NAMES}


def set_variants(*names):
    """Switch exactly `names` on (all others off); no arguments = the original. Unknown names raise."""
    names = NAMES if names == ("all",) else names
    bad = [n for n in names if n not in VARIANTS]
    if bad:
        raise KeyError(f"unknown variant {bad}; known: {NAMES}")
    for n in VARIANTS:
        VARIANTS[n] = n in names


def variant(name):
    return VARIANTS[name]


set_variants(*[t.strip() for t in os.environ.get("REVRON_VARIANTS", "").split(",") if t.strip()])
