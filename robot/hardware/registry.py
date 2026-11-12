"""One lookup for every standard part: `get("M3x8 DIN7991")` -> Part(kind, record, length, ...).

Data lives in `robot.hardware.data.<module>` (one list per kind). Modules are imported lazily; a module that is missing
or fails to import gives an empty list and its error is kept in `load_errors()` (so one broken table never takes the
whole registry down, and the data tests report it).

Accepted designations (case and spacing do not matter):
    "M3x8 DIN7991"  "M3x8 ISO 10642"  "M2.5x6 cap"  "M3x10 shcs"  "M3x6 bhcs"  "M3x8 fhcs"  "M3x4 grub"
    "M3 nut"  "M3 nut ISO4032"  "M3 nyloc"  "M3 thin nut"  "M3 square nut"  "M3 washer ISO7089"  "M3 large washer"
    "M3 insert Ruthex"  "M3x5.7 insert"  "M3x10 standoff mf"  "M3 thread"
    "MR85ZZ"  "683"  "F683ZZ"  "608-2RS"  "dowel 3x10"  "spring pin 2x8"  "DIN471 5"  "e-clip 3"  "oring 6x1.5"
    "shaft 5 h6"  "shaft 3 d_shaft"
"""

from __future__ import annotations

import importlib
import re
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any

# kind -> (data module, attribute)
SOURCES = {
    "thread": ("threads", "THREADS"), "screw": ("screws", "SCREWS"), "nut": ("nuts", "NUTS"),
    "washer": ("washers", "WASHERS"), "insert": ("inserts", "INSERTS"), "standoff": ("standoffs", "STANDOFFS"),
    "pin": ("pins", "PINS"), "circlip": ("circlips", "CIRCLIPS"), "bearing": ("bearings", "BEARINGS"),
    "oring": ("orings", "ORINGS"), "shaft": ("shafts", "SHAFTS"),
}
KINDS = tuple(SOURCES)

# Withdrawn / national standards -> ISO equivalent (normalised, no spaces) and a note when they are not identical.
STD_ALIASES: dict[str, tuple[str, str]] = {
    "DIN912": ("ISO4762", ""),
    "DIN934": ("ISO4032", "DIN 934 is withdrawn; ISO 4032 is close but not identical (taller m; s differs at M10/M12/M14/M22)"),
    "DIN439": ("ISO4035", "DIN 439 ~ ISO 4035"),
    "DIN985": ("ISO10511", "DIN 985 ~ ISO 10511 (heights differ slightly)"),
    "ISO10511": ("DIN985", "ISO 10511 ~ DIN 985 (heights differ slightly)"),
    "DIN125": ("ISO7089", ""), "DIN125A": ("ISO7089", ""), "DIN433": ("ISO7092", ""), "DIN9021": ("ISO7093-1", "DIN 9021 ~ ISO 7093-1"),
    "DIN913": ("ISO4026", ""), "DIN916": ("ISO4029", ""), "DIN84": ("ISO1207", ""), "DIN7985": ("ISO7045", ""),
    "DIN7": ("ISO2338", ""), "DIN6325": ("ISO8734", ""), "DIN1481": ("ISO8752", ""),
    "ISO7380": ("ISO7380-1", ""),
}

SCREW_WORDS = {
    "cap": "cap", "shcs": "cap", "socket": "cap", "socketcap": "cap",
    "button": "button", "bhcs": "button",
    "csk": "csk", "fhcs": "csk", "countersunk": "csk", "flat": "csk",
    "pan": "pan", "cheese": "cheese",
    "grub": "grub", "set": "grub", "setscrew": "grub",
    "pt": "thread_forming", "tf": "thread_forming", "thread-forming": "thread_forming",
    "threadforming": "thread_forming", "plastite": "thread_forming",
}
# preferred standard when several match (first hit wins)
DEFAULT_STD = {"cap": "ISO4762", "button": "ISO7380-1", "csk": "ISO10642", "pan": "ISO7045", "cheese": "ISO1207",
               "hex": "ISO4032", "thin": "ISO4035", "nyloc": "DIN985", "plain": "ISO7089"}
NUT_WORDS = {"nut": None, "hex": "hex", "thin": "thin", "jam": "thin", "nyloc": "nyloc", "locknut": "nyloc",
             "square": "square"}
WASHER_WORDS = {"washer": None, "plain": "plain", "small": "plain_small", "large": "large", "fender": "large",
                "spring": "spring"}
BEARING_SUFFIX = re.compile(r"(-?2RS1|-?2RSH|-?2RS|-?RS|-?ZZ|-?2Z|-?Z|-?OPEN)$")


@dataclass(frozen=True)
class Part:
    """A resolved standard part: the family record (dimensions at this size) plus the chosen length/variant."""
    kind: str
    record: Any
    length: float | None = None
    designation: str = ""
    variant: str = ""  # e.g. bearing seal suffix asked for ("ZZ", "2RS") when the table lists another
    notes: tuple[str, ...] = field(default_factory=tuple)

    @property
    def d(self) -> float | None:
        r = self.record
        for name in ("d", "shaft_d"):
            if hasattr(r, name):
                return getattr(r, name)
        return getattr(r, "id", None)

    @property
    def standard(self) -> str:
        return getattr(self.record, "standard", "") or getattr(getattr(self.record, "src", None), "standard", "")

    @property
    def uncertain(self) -> tuple[str, ...]:
        return tuple(getattr(getattr(self.record, "src", None), "uncertain_fields", ()) or ())


def _n(x) -> str:
    return f"{float(x):g}"


def norm_std(s: str) -> str:
    """'ISO 4762:2004' -> 'ISO4762'; 'din 7991' -> 'DIN7991'."""
    s = re.sub(r":\d{4}\b.*$", "", str(s).upper())
    return re.sub(r"\s+", "", s)


def _std_match(want: str, have: str) -> bool:
    h = norm_std(have)
    return h == want or h.startswith(want + "-")


def _std_candidates(token: str) -> tuple[set[str], str]:
    n = norm_std(token)
    alias, note = STD_ALIASES.get(n, ("", ""))
    return ({n, alias} - {""}), note


# --------------------------------------------------------------------------------------------- loading
_ERRORS: dict[str, str] = {}


@lru_cache(maxsize=None)
def records(kind: str) -> tuple:
    """All records of one kind (empty tuple when the data module is missing)."""
    if kind not in SOURCES:
        raise ValueError(f"unknown kind `{kind}`; kinds: {', '.join(KINDS)}")
    mod, attr = SOURCES[kind]
    try:
        data = getattr(importlib.import_module(f"robot.hardware.data.{mod}"), attr)
    except Exception as e:  # noqa: BLE001 - keep the registry usable when one table is broken
        _ERRORS[kind] = f"{type(e).__name__}: {e}"
        return ()
    if isinstance(data, dict):
        data = list(data.values())
    return tuple(data)


def load_errors() -> dict[str, str]:
    for k in KINDS:
        records(k)
    return dict(_ERRORS)


def plastic_pilot() -> dict[str, float]:
    """Pilot-hole factor x d for thread-forming screws by plastic (data/screws.PLASTIC_PILOT), {} when absent."""
    try:
        return dict(getattr(importlib.import_module("robot.hardware.data.screws"), "PLASTIC_PILOT", {}))
    except Exception:  # noqa: BLE001
        return {}


def thread(d: float):
    for t in records("thread"):
        if abs(t.d - float(d)) < 1e-9:
            return t
    raise ValueError(f"no thread data for M{_n(d)} (have M{', M'.join(_n(t.d) for t in records('thread'))})")


def list_family(kind: str, family: str | None = None, d: float | None = None, standard: str | None = None) -> list:
    """Records of `kind`, filtered by family (prefix match: 'grub' matches grub_flat), size and standard."""
    out = []
    want = _std_candidates(standard)[0] if standard else None
    for r in records(kind):
        fam = getattr(r, "family", None)
        if family and not (fam and (fam == family or fam.startswith(family))):
            continue
        if d is not None:
            rd = getattr(r, "d", getattr(r, "shaft_d", getattr(r, "id", None)))
            if rd is None or abs(rd - float(d)) > 1e-9:
                continue
        if want and not any(_std_match(w, getattr(r, "standard", r.src.standard)) for w in want):
            continue
        out.append(r)
    return out


def nearest_length(part_or_record, length: float, mode: str = "ceil") -> float:
    """Nearest standard length of a screw/pin record (or Part). mode: ceil (>= length), floor (<=), nearest."""
    rec = getattr(part_or_record, "record", part_or_record)
    if isinstance(part_or_record, str):
        rec = get(part_or_record, strict=False).record
    Ls = sorted(getattr(rec, "lengths", ()) or ())
    if not Ls:
        raise ValueError(f"{type(rec).__name__} has no standard lengths")
    if mode == "ceil":
        up = [L for L in Ls if L >= length - 1e-9]
        if not up:
            raise ValueError(f"no standard length >= {_n(length)} (max {_n(Ls[-1])})")
        return float(up[0])
    if mode == "floor":
        dn = [L for L in Ls if L <= length + 1e-9]
        if not dn:
            raise ValueError(f"no standard length <= {_n(length)} (min {_n(Ls[0])})")
        return float(dn[-1])
    if mode == "nearest":
        return float(min(Ls, key=lambda L: (abs(L - length), L)))
    raise ValueError(f"mode must be ceil | floor | nearest, not `{mode}`")


# --------------------------------------------------------------------------------------------- parsing
_NUM = r"(\d+(?:\.\d+)?)"
_M = re.compile(rf"^M{_NUM}(?:\s*X\s*{_NUM})?(?:\s+(.*))?$")


def _pick(cands: list, prefer_std: str | None, what: str):
    if prefer_std:
        for c in cands:
            if _std_match(prefer_std, getattr(c, "standard", "")):
                return c
    return cands[0]


def _check_length(rec, L, strict, what, notes):
    Ls = tuple(getattr(rec, "lengths", ()) or ())
    if L is None or not Ls or any(abs(L - x) < 1e-9 for x in Ls):
        return
    msg = f"{what}: length {_n(L)} is not a standard length (have {', '.join(_n(x) for x in Ls)})"
    if strict:
        raise ValueError(msg)
    notes.append(msg)


def _screw(d, L, words, stds, notes, strict, raw):
    fam = None
    for w in words:
        if w in SCREW_WORDS:
            fam = SCREW_WORDS[w]
        else:
            raise ValueError(f"`{raw}`: unknown word `{w}` (screw words: {', '.join(sorted(SCREW_WORDS))})")
    at_d = list_family("screw", d=d)
    if not at_d:
        have = sorted({r.d for r in records("screw")})
        raise ValueError(f"`{raw}`: no screws at M{_n(d)} (have M{', M'.join(map(_n, have))})")
    c = [r for r in at_d if fam is None or r.family == fam or r.family.startswith(fam)]
    if stds:
        c = [r for r in c if any(_std_match(s, r.standard) for s in stds)]
    if not c:
        opts = sorted({f"{r.family} {r.standard}" for r in at_d})
        raise ValueError(f"`{raw}`: no M{_n(d)} screw matches; options at M{_n(d)}: {'; '.join(opts)}")
    fam = fam or ("cap" if any(r.family == "cap" for r in c) else c[0].family)
    c = [r for r in c if r.family == fam or r.family.startswith(fam)] or c
    rec = _pick(c, None if stds else DEFAULT_STD.get(fam), raw)
    if len({r.standard for r in c}) > 1:
        notes.append(f"also available: {', '.join(sorted({r.standard for r in c} - {rec.standard}))}")
    what = f"M{_n(d)} {rec.family} {rec.standard}"
    _check_length(rec, L, strict, what, notes)
    des = f"M{_n(d)}x{_n(L)} {rec.standard}" if L is not None else f"M{_n(d)} {rec.standard}"
    return Part("screw", rec, L, des, "", tuple(notes))


def _simple(kind, words_map, d, words, stds, notes, raw, default_fam):
    fam = None
    for w in words:
        if w not in words_map:
            raise ValueError(f"`{raw}`: unknown word `{w}` ({kind} words: {', '.join(sorted(words_map))})")
        fam = words_map[w] or fam
    at_d = list_family(kind, d=d)
    c = [r for r in at_d if r.family == (fam or default_fam)] if (fam or not stds) else list(at_d)
    if stds:
        c = [r for r in c if any(_std_match(s, r.standard) for s in stds)]
    if not c:
        opts = sorted({f"{r.family} {r.standard}" for r in at_d}) or ["none"]
        raise ValueError(f"`{raw}`: no M{_n(d)} {fam or default_fam} {kind}; options at M{_n(d)}: {'; '.join(opts)}")
    rec = _pick(c, None if stds else DEFAULT_STD.get(c[0].family), raw)
    return Part(kind, rec, None, f"M{_n(d)} {rec.family} {kind} {rec.standard}", "", tuple(notes))


def _insert(d, L, words, notes, raw):
    c = list_family("insert", d=d)
    if not c:
        raise ValueError(f"`{raw}`: no heat-set insert for M{_n(d)}")
    makers = {r.maker.lower().replace(" ", ""): r.maker for r in c}
    for w in words:
        key = w.lower().replace(" ", "")
        hits = [m for k, m in makers.items() if key in k]
        if not hits:
            raise ValueError(f"`{raw}`: unknown insert maker `{w}` (have {', '.join(sorted(set(makers.values())))})")
        c = [r for r in c if r.maker == hits[0]]
    if L is not None:
        c2 = [r for r in c if abs(r.length - L) < 1e-6]
        if not c2:
            raise ValueError(f"`{raw}`: no M{_n(d)} insert {_n(L)} long (have {', '.join(f'{r.maker} {r.part_no}' for r in c)})")
        c = c2
    else:
        pref = [r for r in c if r.maker == "Ruthex"] or c
        c = sorted(pref, key=lambda r: -r.length)  # the "standard" (longest common) insert first
    rec = c[0]
    return Part("insert", rec, rec.length, f"M{_n(d)} insert {rec.maker} {rec.part_no}", "", tuple(notes))


def _standoff(d, L, words, notes, raw):
    fam = next((w for w in words if w in ("ff", "mf", "mm")), "ff")
    bad = [w for w in words if w not in ("ff", "mf", "mm", "brass", "hex")]
    if bad:
        raise ValueError(f"`{raw}`: unknown word `{bad[0]}` (standoff words: ff, mf, mm)")
    c = [r for r in list_family("standoff", family=fam, d=d) if L is None or abs(r.length - L) < 1e-6]
    if not c:
        have = sorted({r.length for r in list_family("standoff", family=fam, d=d)})
        raise ValueError(f"`{raw}`: no M{_n(d)} {fam} standoff {'' if L is None else _n(L)} "
                         f"(lengths: {', '.join(map(_n, have)) or 'none'})")
    rec = c[0]
    return Part("standoff", rec, rec.length, f"M{_n(d)}x{_n(rec.length)} {fam} standoff", "", tuple(notes))


def _bearing(s, raw):
    key = re.sub(r"[\s]", "", s.upper())
    idx = {}
    for r in records("bearing"):
        full = r.designation.upper().replace(" ", "")
        idx.setdefault(full, (r, ""))
        base = BEARING_SUFFIX.sub("", full)
        idx.setdefault(base, (r, ""))
    if key in idx:
        rec, _ = idx[key]
        return Part("bearing", rec, rec.B, rec.designation)
    m = BEARING_SUFFIX.search(key)
    base = BEARING_SUFFIX.sub("", key)
    if base in idx:
        rec, _ = idx[base]
        suffix = m.group(0).lstrip("-") if m else ""
        note = f"asked for {suffix}; table entry is {rec.designation} (same envelope assumed)"
        return Part("bearing", rec, rec.B, rec.designation, suffix, (note,))
    return None


def get(designation: str, strict: bool = True) -> Part:
    """Resolve a designation string. Raises ValueError naming the options when nothing matches.
    strict=False accepts a non-standard screw/pin length (a note is added instead)."""
    raw = str(designation or "").strip()
    if not raw:
        raise ValueError("empty designation")
    s = re.sub(r"\s+", " ", raw.upper())
    s = re.sub(r"\b(ISO|DIN|EN|WN)\s+(\d)", r"\1\2", s)  # 'DIN 7991' -> 'DIN7991'
    notes: list[str] = []

    m = _M.match(s)
    if m:
        d = float(m.group(1))
        L = float(m.group(2)) if m.group(2) else None
        stds: set[str] = set()
        words = []
        for tok in (m.group(3) or "").split():
            if re.match(r"^(ISO|DIN|EN|WN)\d", tok):
                cands, note = _std_candidates(tok)
                stds |= cands
                if note:
                    notes.append(note)
            else:
                words.append(tok.lower())
        if "thread" in words:
            return Part("thread", thread(d), None, f"M{_n(d)}")
        if any(w in NUT_WORDS and w != "hex" for w in words) or (not words and stds and _std_kind(stds) == "nut"):
            return _simple("nut", NUT_WORDS, d, words, stds, notes, raw, "hex")
        if any(w in WASHER_WORDS and w not in ("plain",) for w in words) or (not words and stds and _std_kind(stds) == "washer"):
            return _simple("washer", WASHER_WORDS, d, words, stds, notes, raw, "plain")
        if "insert" in words:
            return _insert(d, L, [w for w in words if w not in ("insert", "heatset", "heat-set")], notes, raw)
        if "standoff" in words or "spacer" in words:
            return _standoff(d, L, [w for w in words if w not in ("standoff", "spacer")], notes, raw)
        return _screw(d, L, words, stds, notes, strict, raw)

    p = _bearing(s, raw)
    if p is not None:
        return p

    m = re.match(rf"^(DOWEL|PIN|SPRING PIN|ROLL PIN|HARDENED DOWEL)\s*{_NUM}\s*X\s*{_NUM}(?:\s+(\S+))?$", s)
    if m:
        kind_word, d, L = m.group(1), float(m.group(2)), float(m.group(3))
        fam = "spring" if kind_word in ("SPRING PIN", "ROLL PIN") else "dowel_hardened" if kind_word.startswith("HARD") else "dowel"
        c = list_family("pin", family=fam, d=d)
        if m.group(4):
            c = [r for r in c if any(_std_match(x, r.standard) for x in _std_candidates(m.group(4))[0])] or \
                [r for r in c if r.family.endswith(m.group(4).lower())]
        if not c:
            have = sorted({r.d for r in list_family("pin", family=fam)})
            raise ValueError(f"`{raw}`: no {fam} pin d{_n(d)} (have d {', '.join(map(_n, have)) or 'none'})")
        rec = c[0]
        _check_length(rec, L, strict, f"{rec.standard} d{_n(d)}", notes)
        return Part("pin", rec, L, f"{rec.standard} {_n(d)}x{_n(L)}", "", tuple(notes))

    m = re.match(rf"^(DIN471|DIN472|DIN6799|CIRCLIP|INTERNAL CIRCLIP|E-?CLIP|RETAINING RING)\s*{_NUM}$", s) or \
        re.match(rf"^{_NUM}\s*(DIN471|DIN472|DIN6799|CIRCLIP|E-?CLIP)$", s)
    if m:
        g = [x for x in m.groups()]
        word, size = (g[0], float(g[1])) if not g[0][0].isdigit() else (g[1], float(g[0]))
        fam = "int" if word in ("DIN472", "INTERNAL CIRCLIP") else "e_clip" if ("6799" in word or "CLIP" in word and word.startswith("E")) else "ext"
        c = [r for r in list_family("circlip", family=fam) if abs(r.shaft_d - size) < 1e-9]
        if not c:
            have = sorted({r.shaft_d for r in list_family("circlip", family=fam)})
            raise ValueError(f"`{raw}`: no {fam} circlip for {_n(size)} (have {', '.join(map(_n, have)) or 'none'})")
        rec = c[0]
        return Part("circlip", rec, None, f"{rec.standard} {_n(size)}")

    m = re.match(rf"^O-?RING\s*{_NUM}\s*X\s*{_NUM}$", s)
    if m:
        i, cs = float(m.group(1)), float(m.group(2))
        c = [r for r in records("oring") if abs(r.id - i) < 1e-6 and abs(r.cs - cs) < 1e-6]
        if not c:
            near = sorted(r.designation for r in records("oring") if abs(r.cs - cs) < 1e-6) or \
                sorted({_n(r.cs) for r in records("oring")})
            raise ValueError(f"`{raw}`: no O-ring {_n(i)}x{_n(cs)}; options: {', '.join(near)}")
        return Part("oring", c[0], None, f"O-ring {c[0].designation}")

    m = re.match(rf"^SHAFT\s*{_NUM}(?:\s*MM)?(?:\s+(\S+))?$", s)
    if m:
        d, opt = float(m.group(1)), (m.group(2) or "").lower()
        c = [r for r in records("shaft") if abs(r.d - d) < 1e-9]
        if opt:
            c = [r for r in c if r.form.lower() == opt or r.tolerance.lower() == opt]
        if not c:
            raise ValueError(f"`{raw}`: no shaft d{_n(d)} {opt}; have "
                             f"{', '.join(sorted({f'{_n(r.d)} {r.form} {r.tolerance}' for r in records('shaft')}))}")
        return Part("shaft", c[0], None, f"shaft {_n(d)} {c[0].form} {c[0].tolerance}")

    raise ValueError(f"cannot parse `{raw}`: expected e.g. 'M3x8 ISO 4762', 'M3 nut', 'M3 washer', 'M3 insert', "
                     f"'MR85ZZ', 'dowel 3x10', 'DIN471 5', 'oring 6x1.5', 'shaft 5 h6'")


def _std_kind(stds: set[str]) -> str | None:
    for kind in ("nut", "washer", "screw"):
        if any(_std_match(s, getattr(r, "standard", "")) for r in records(kind) for s in stds):
            return kind
    return None
