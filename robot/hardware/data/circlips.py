"""Retaining rings. DIN 471 (external), DIN 472 (internal), DIN 6799 (E-clips)."""

from ..types import Circlip, Source

_S471 = Source("DIN 471:2011")
_S472 = Source("DIN 472:2011")
_S6799 = Source("DIN 6799:2009", note="shaft_d = upper end of shaft range; groove_d is the defining size")

CIRCLIPS: list[Circlip] = [
    # DIN 471: shaft, groove d2, groove m (H13), thickness s
    Circlip("ext_din471", "DIN 471", 3, 2.8, 0.5, 0.4, src=_S471),
    Circlip("ext_din471", "DIN 471", 4, 3.8, 0.5, 0.4, src=_S471),
    Circlip("ext_din471", "DIN 471", 5, 4.8, 0.7, 0.6, src=_S471),
    Circlip("ext_din471", "DIN 471", 6, 5.7, 0.8, 0.7, src=_S471),
    Circlip("ext_din471", "DIN 471", 7, 6.7, 0.9, 0.8, src=_S471),
    Circlip("ext_din471", "DIN 471", 8, 7.6, 0.9, 0.8, src=_S471),
    Circlip("ext_din471", "DIN 471", 9, 8.6, 1.1, 1.0, src=_S471),
    Circlip("ext_din471", "DIN 471", 10, 9.6, 1.1, 1.0, src=_S471),
    # DIN 472: bore, groove d2, m, s (smallest standard bore 8)
    Circlip("int_din472", "DIN 472", 8, 8.4, 0.9, 0.8, src=_S472),
    Circlip("int_din472", "DIN 472", 9, 9.4, 0.9, 0.8, src=_S472),
    Circlip("int_din472", "DIN 472", 10, 10.4, 1.1, 1.0, src=_S472),
    # DIN 6799 E-clips: nominal = groove d
    Circlip("e_clip_din6799", "DIN 6799", 2.0, 1.5, 0.44, 0.4, src=_S6799),
    Circlip("e_clip_din6799", "DIN 6799", 2.5, 1.9, 0.54, 0.5, src=_S6799),
    Circlip("e_clip_din6799", "DIN 6799", 3.0, 2.3, 0.64, 0.6, src=_S6799),
    Circlip("e_clip_din6799", "DIN 6799", 4.0, 3.2, 0.64, 0.6, src=_S6799),
    Circlip("e_clip_din6799", "DIN 6799", 5.0, 4.0, 0.74, 0.7, src=_S6799),
    Circlip("e_clip_din6799", "DIN 6799", 7.0, 5.0, 0.74, 0.7, src=_S6799),
    Circlip("e_clip_din6799", "DIN 6799", 8.0, 6.0, 0.74, 0.7, src=_S6799),
    Circlip("e_clip_din6799", "DIN 6799", 9.0, 7.0, 0.94, 0.9, src=_S6799),
    Circlip("e_clip_din6799", "DIN 6799", 10.0, 8.0, 1.05, 1.0, src=_S6799),
]
