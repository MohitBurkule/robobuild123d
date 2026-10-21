"""[drawing] ISO 5457 sheet: trimmed size, frame (20 mm filing margin left, 10 mm elsewhere), zone grid with
numbers / letters, centring marks, a title block (ISO 7200 fields) and the third-angle projection symbol."""
from __future__ import annotations

from dataclasses import dataclass

SIZES = {"A1": (841.0, 594.0, 16, 12), "A2": (594.0, 420.0, 12, 8), "A3": (420.0, 297.0, 8, 6)}
ROWS = "ABCDEFGHJKLMNPQR"           # zone letters skip I and O
TB_W, TB_H = 180.0, 56.0


@dataclass
class Sheet:
    size: str
    w: float
    h: float
    cols: int
    rows: int
    frame: tuple                    # x0, y0, x1, y1 of the drawing frame
    title_block: tuple              # x0, y0, x1, y1

    def zone_of(self, x, y):
        x0, y0, x1, y1 = self.frame
        c = self.cols - int((x - x0) / (x1 - x0) * self.cols)   # numbers run right to left like the reference sheet
        r = int((y - y0) / (y1 - y0) * self.rows)
        return f"{ROWS[min(max(r, 0), self.rows - 1)]}{min(max(c, 1), self.cols)}"


def make_sheet(size="A1"):
    w, h, cols, rows = SIZES[size]
    frame = (20.0, 10.0, w - 10.0, h - 10.0)
    tb = (frame[2] - TB_W, frame[1], frame[2], frame[1] + TB_H)
    return Sheet(size, w, h, cols, rows, frame, tb)


def draw_frame(c, sh: Sheet):
    x0, y0, x1, y1 = sh.frame
    c.rect(x0, y0, x1, y1, "frame")
    c.rect(x0 - 5, y0 - 5, x1 + 5, y1 + 5, "thin")          # zone band outer edge
    cw, rh = (x1 - x0) / sh.cols, (y1 - y0) / sh.rows
    for i in range(sh.cols):
        xa = x0 + i * cw
        for yy, ya, yb in ((y0 - 5, y0 - 5, y0), (y1, y1, y1 + 5)):
            c.line((xa, ya), (xa, yb), "thin")
            c.text((xa + cw / 2, yy + 1.2), str(sh.cols - i), 3.5, "middle")
    for j in range(sh.rows):
        ya = y0 + j * rh
        for xx, xa, xb in ((x0 - 5, x0 - 5, x0), (x1, x1, x1 + 5)):
            c.line((xa, ya), (xb, ya), "thin")
            c.text((xx + 2.5, ya + rh / 2 - 1.2), ROWS[j], 3.5, "middle")
    # centring marks
    for (a, b) in (((sh.w / 2, 0), (sh.w / 2, y0)), ((sh.w / 2, y1), (sh.w / 2, sh.h)), ((0, sh.h / 2), (x0, sh.h / 2)), ((x1, sh.h / 2), (sh.w, sh.h / 2))):
        c.line(a, b, "frame")


def projection_symbol(c, x, y, s=1.0):
    """ISO 5456-2 third-angle symbol at (x, y) bottom-left: frustum side view left, its end view (circles) right."""
    h, d1, d2, L = 10 * s, 10 * s, 5 * s, 10 * s
    cy = y + h / 2
    c.poly([(x, cy - d2 / 2), (x + L, cy - d1 / 2), (x + L, cy + d1 / 2), (x, cy + d2 / 2)], "visible", closed=True)
    c.line((x - 2 * s, cy), (x + L + 2 * s, cy), "center")
    import numpy as np
    cx = x + L + 8 * s + d1 / 2
    for r in (d1 / 2, d2 / 2):
        t = np.linspace(0, 2 * np.pi, 73)
        c.poly(np.c_[cx + r * np.cos(t), cy + r * np.sin(t)], "visible", closed=True)
    c.line((cx - d1 / 2 - 2 * s, cy), (cx + d1 / 2 + 2 * s, cy), "center")
    c.line((cx, cy - d1 / 2 - 2 * s), (cx, cy + d1 / 2 + 2 * s), "center")


def title_block(c, sh: Sheet, fields: dict):
    """fields: title, part, dwg_no, material, mass, scale, date, units, drawn, source, sheet, notes (list)."""
    x0, y0, x1, y1 = sh.title_block
    c.rect(x0, y0, x1, y1, "frame")
    rows = [y0, y0 + 10, y0 + 20, y0 + 30, y0 + 42, y1]
    for yy in rows[1:-1]:
        c.line((x0, yy), (x1, yy), "thin")
    xm = x0 + 90
    c.line((xm, y0), (xm, rows[4]), "thin")
    c.line((x0 + 135, y0), (x0 + 135, rows[3]), "thin")

    def cell(x, y, label, value, size=3.5):
        c.text((x + 1.5, y + 6.8), label, 2.0)
        c.text((x + 1.5, y + 1.8), str(value), size)

    cell(x0, rows[4], "TITLE", fields.get("title", ""), 5.0)
    c.text((x1 - 2, rows[4] + 1.8), fields.get("size", sh.size), 5.0, "end")
    cell(x0, rows[3], "PART", fields.get("part", ""))
    cell(xm, rows[3], "DWG NO.", fields.get("dwg_no", ""))
    cell(x0, rows[2], "MATERIAL", fields.get("material", ""))
    cell(xm, rows[2], "MASS (from model)", fields.get("mass", ""))
    cell(x0 + 135, rows[2], "SCALE", fields.get("scale", ""))
    cell(x0, rows[1], "DRAWN", fields.get("drawn", ""), 3.0)
    cell(xm, rows[1], "DATE", fields.get("date", ""))
    cell(x0 + 135, rows[1], "UNITS", fields.get("units", "mm"))
    cell(x0, rows[0], "SOURCE", fields.get("source", ""), 2.5)
    cell(xm, rows[0], "SHEET", fields.get("sheet", "1 OF 1"))
    projection_symbol(c, x0 + 140, y0 + 1.5, 0.75)
    # general notes just above the title block
    for i, n in enumerate(fields.get("notes", [])):
        c.text((x0, y1 + 3 + 5 * (len(fields.get("notes", [])) - 1 - i)), n, 2.8)
