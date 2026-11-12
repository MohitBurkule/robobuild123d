"""Metric screw heads M1.6-M5. dk/k are max values (csk: theoretical max dk). Lengths are preferred lengths of the
standard range. Drive `s`: hex key AF, torx T-number, or phillips PH number (as float).
Values from standard tables as reproduced by Bossard / Wuerth / fasteners.eu catalogue pages (see SOURCES_screws.md)."""
from ..types import ScrewHead, Source

_L = (2, 2.5, 3, 4, 5, 6, 8, 10, 12, 14, 16, 20, 25, 30, 35, 40, 45, 50)


def _r(lo, hi):
    return tuple(x for x in _L if lo <= x <= hi)


SCREWS: list[ScrewHead] = [
    # --- socket head cap ISO 4762 ---
    *[ScrewHead("cap", "ISO 4762", d, dk, k, "hex", s, t, lengths=_r(lo, hi), b_thread=b,
                src=Source("ISO 4762:2004", note="plain head dk max; dk/k/s/t/b verified https://www.fasteners.eu/standards/ISO/4762/"))
      for d, dk, k, s, t, b, lo, hi in [
          (1.6, 3.0, 1.6, 1.5, 0.7, 15, 2.5, 16), (2.0, 3.8, 2.0, 1.5, 1.0, 16, 3, 20),
          (2.5, 4.5, 2.5, 2.0, 1.1, 17, 4, 25), (3.0, 5.5, 3.0, 2.5, 1.3, 18, 5, 30),
          (4.0, 7.0, 4.0, 3.0, 2.0, 20, 6, 40), (5.0, 8.5, 5.0, 4.0, 2.5, 22, 8, 50)]],
    # --- button ISO 7380-1 (standard starts at M3; M2/M2.5 vendor) ---
    ScrewHead("button", "ISO 7380-1", 2.0, 3.5, 1.3, "hex", 1.3, 0.7, lengths=_r(3, 12),
              src=Source("vendor (ISO 7380-1 style)", note="not in ISO 7380-1; Accu/Bossard values",
                         uncertain_fields=("dk", "k", "s", "t", "lengths"))),
    ScrewHead("button", "ISO 7380-1", 2.5, 4.7, 1.5, "hex", 1.5, 0.9, lengths=_r(4, 16),
              src=Source("vendor (ISO 7380-1 style)", note="not in ISO 7380-1; Accu/Bossard values",
                         uncertain_fields=("dk", "k", "s", "t", "lengths"))),
    *[ScrewHead("button", "ISO 7380-1", d, dk, k, "hex", s, t, lengths=_r(lo, hi),
                src=Source("ISO 7380-1:2011", note="M3 dk/k/s/t verified Westfield ScrewBolt-SHBtn-M.pdf + "
                           "fasten.it/en/norms/norm/din_en_iso_7380-1; M4/M5 not re-checked",
                           uncertain_fields=() if d == 3.0 else ("t",)))
      for d, dk, k, s, t, lo, hi in [(3.0, 5.7, 1.65, 2.0, 1.04, 6, 30), (4.0, 7.6, 2.2, 2.5, 1.3, 6, 40),
                                     (5.0, 9.5, 2.75, 3.0, 1.56, 8, 50)]],
    # --- countersunk hex socket ISO 10642 (M3+) ---
    *[ScrewHead("csk", "ISO 10642", d, dk, k, "hex", s, t, csk_angle=90, lengths=_r(lo, hi),
                src=Source("ISO 10642:2004", note="dk = theoretical max; fasteners.eu/standards/ISO/10642/ shows "
                           "DIN 7991 values (6/1.7/0.95) instead - conflict unresolved",
                           uncertain_fields=("dk", "k", "t")))
      for d, dk, k, s, t, lo, hi in [(3.0, 6.72, 1.86, 2.0, 1.1, 8, 30), (4.0, 8.96, 2.48, 2.5, 1.5, 8, 40),
                                     (5.0, 11.2, 3.1, 3.0, 1.9, 8, 50)]],
    # --- countersunk hex socket DIN 7991 ---
    *[ScrewHead("csk", "DIN 7991", d, dk, k, "hex", s, t, csk_angle=90, lengths=_r(lo, hi),
                src=Source("DIN 7991:1986", note="dk max (actual-head)", uncertain_fields=unc))
      for d, dk, k, s, t, lo, hi, unc in [
          (2.0, 4.0, 1.2, 1.3, 0.8, 4, 16, ("dk", "k", "s", "t")),
          (2.5, 5.0, 1.5, 1.5, 1.0, 5, 20, ("dk", "k", "s", "t")),
          # M3-M5 dk/k/s verified https://www.fasteners.eu/standards/DIN/7991/; that page gives t min
          # 0.95/1.5/2.05 vs our 1.2/1.8/2.3 -> t left uncertain
          (3.0, 6.0, 1.7, 2.0, 1.2, 6, 30, ("t",)), (4.0, 8.0, 2.3, 2.5, 1.8, 8, 40, ("t",)),
          (5.0, 10.0, 2.8, 3.0, 2.3, 8, 50, ("t",))]],
    # --- countersunk torx ISO 14581 (small sizes) ---
    *[ScrewHead("csk", "ISO 14581", d, dk, k, "torx", T, t, csk_angle=90, lengths=_r(lo, hi),
                src=Source("ISO 14581:2013", note="dk theoretical max", uncertain_fields=("t",)))
      for d, dk, k, T, t, lo, hi in [(1.6, 3.0, 0.96, 5, 0.4, 3, 16), (2.0, 3.8, 1.2, 6, 0.6, 3, 20),
                                     (2.5, 4.7, 1.5, 8, 0.75, 4, 25), (3.0, 5.5, 1.65, 10, 0.85, 5, 30),
                                     (4.0, 8.4, 2.7, 20, 1.3, 6, 40), (5.0, 9.3, 2.7, 25, 1.4, 8, 50)]],
    # --- pan phillips ISO 7045 ---
    *[ScrewHead("pan", "ISO 7045", d, dk, k, "phillips", ph, lengths=_r(lo, hi), src=Source("ISO 7045:2011"))
      for d, dk, k, ph, lo, hi in [(1.6, 3.2, 1.3, 0, 3, 16), (2.0, 4.0, 1.6, 0, 3, 20), (2.5, 5.0, 2.1, 1, 3, 25),
                                   (3.0, 5.6, 2.4, 1, 4, 30), (4.0, 8.0, 3.1, 2, 5, 40), (5.0, 9.5, 3.7, 2, 6, 45)]],
    # --- pan torx ISO 14583 ---
    *[ScrewHead("pan", "ISO 14583", d, dk, k, "torx", T, lengths=_r(lo, hi), src=Source("ISO 14583:2011"))
      for d, dk, k, T, lo, hi in [(2.0, 4.0, 1.6, 6, 3, 20), (2.5, 5.0, 2.1, 8, 3, 25), (3.0, 5.6, 2.4, 10, 4, 30),
                                  (4.0, 8.0, 3.1, 20, 5, 40), (5.0, 9.5, 3.7, 25, 6, 45)]],
    # --- cheese slotted ISO 1207 ---
    *[ScrewHead("cheese", "ISO 1207", d, dk, k, "slot", n, lengths=_r(lo, hi),
                src=Source("ISO 1207:2011", note="s = slot width n nominal"))
      for d, dk, k, n, lo, hi in [(1.6, 3.0, 1.1, 0.4, 2, 16), (2.0, 3.8, 1.4, 0.5, 3, 20), (2.5, 4.5, 1.8, 0.6, 3, 25),
                                  (3.0, 5.5, 2.0, 0.8, 4, 30), (4.0, 7.0, 2.6, 1.2, 5, 40), (5.0, 8.5, 3.3, 1.2, 6, 50)]],
    # --- set screws (dk = d, k = 0) ---
    *[ScrewHead(fam, std, d, d, 0.0, "hex", s, t, lengths=_r(lo, hi),
                src=Source(std + ":2003", note=note, uncertain_fields=("t",)))
      for fam, std, note in [("grub_flat", "ISO 4026", "flat point"), ("grub_cup", "ISO 4029", "cup point")]
      for d, s, t, lo, hi in [(1.6, 0.7, 0.7, 2, 8), (2.0, 0.9, 0.8, 2, 10), (2.5, 1.3, 1.2, 2, 12),
                              (3.0, 1.5, 1.2, 2.5, 16), (4.0, 2.0, 1.5, 3, 20), (5.0, 2.5, 2.0, 4, 25)]],
    # --- thread-forming for plastics, PT / Delta PT (WN 1411) style pan torx ---
    *[ScrewHead("thread_forming_pan", "WN 1411", d, dk, k, "torx", T, lengths=_r(lo, hi),
                src=Source("EJOT DELTA PT WN 1411 catalogue", note="30 deg flank thread; head approx",
                           uncertain_fields=("dk", "k", "lengths")))
      for d, dk, k, T, lo, hi in [(2.2, 4.2, 1.6, 6, 4, 12), (2.5, 4.7, 1.8, 8, 5, 16), (3.0, 5.7, 2.1, 10, 6, 20),
                                  (4.0, 7.6, 2.8, 20, 8, 25), (5.0, 9.5, 3.5, 25, 10, 30)]],
]

# Pilot-hole diameter factor (x nominal d) for thread-forming screws in plastic (EJOT DELTA PT guideline);
# boss OD ~ 2.0 d, engagement ~ 2.0 d. All values uncertain (vendor guidance, material-dependent).
PLASTIC_PILOT: dict[str, float] = {
    "PP": 0.70, "PE": 0.70, "POM": 0.75, "PA6": 0.75, "ABS": 0.80, "PC": 0.85, "PC/ABS": 0.80,
    "PA-GF30": 0.80, "PBT-GF30": 0.82, "PLA": 0.80, "PETG": 0.80,  # PLA/PETG: FDM practice, not EJOT
}
