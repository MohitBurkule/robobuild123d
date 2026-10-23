"""Alternative COTS parts for an antweight (Revron class): weapon outrunners, drive gearmotors, LiPo packs, ESCs,
connectors/switches and fully parametric wheels/tyres.

Every vendor number lives in exactly one data table below (one dict per part) with a `src` entry naming where it came
from (vendor page / drawing / datasheet, mirrored under research/cots/<category>/<model>/raw). Numbers marked in a
part's `derived` / `assumed` notes are not vendor numbers. The generators turn a table row into a `catalog.CatalogEntry`
with the same frame, kind, ports, shaft and props keys as the existing built-ins, so any of these swaps in by changing
one `"catalog": "<id>"` setting in a template.

Frames (same as catalog.py): motors and wheels have their shaft/axle along local +X with the shaft out of the +X end;
batteries lie with the long side along X; flat electronics lie in the XY plane; connectors mate along +X.

Vendor STEP files downloaded for comparison (research/cots/*/*/cad_ref) are reference only and are never imported.
"""

from __future__ import annotations

import math

from robot.catalog import CatalogEntry, at, box, cyl, cyl_x, minus, rot, union

COTS_ROOT = "research/cots"   # shared research folder (raw downloads, cad_ref, INDEX.md)
EPS = 0.05                    # overlap so booleans fuse/cut cleanly
SILICONE_G_CM3 = 1.1          # tyre (silicone/rubber) density, for generated wheel masses
PLA_G_CM3 = 1.24              # printed hub density


# ----------------------------------------------------------------------------------------------- shape helpers
def ring_x(r_out, r_in, length):
    """Tube along X, centred on the origin."""
    return minus(cyl_x(r_out, length), [cyl_x(r_in, length + 2 * EPS)])


def bolt_circle(pcd, n, phase_deg=45.0):
    """(y, z) points of `n` holes equally spaced on a pitch circle `pcd` round the X axis."""
    return [(pcd / 2 * math.cos(math.radians(phase_deg + 360.0 * i / n)), pcd / 2 * math.sin(math.radians(phase_deg + 360.0 * i / n)))
            for i in range(n)]


def holes_x(points, d, x, depth):
    """Blind/through hole cylinders along X at (y, z) points, centred at x."""
    return [at(cyl_x(d / 2, depth), x, y, z) for y, z in points]


def d_shaft_x(d, flat, length):
    """D-shaft along X: cylinder `d` with one flat leaving `flat` across (flat face on +Z)."""
    cut_h = d - flat
    return minus(cyl_x(d / 2, length), [at(box(length + 2 * EPS, d + 1, cut_h + EPS), 0, 0, d / 2 - cut_h / 2 + EPS / 2)])


def d_bore_z(d, flat, h):
    """D-shaped hole along Z (for cutting): cylinder `d` intersected with the half-space below the flat."""
    return {"type": "intersect", "items": [cyl(d / 2, h), at(box(d + 1, d + 1, h + 1), 0, -(d + 1) / 2 + (flat - d / 2), 0)]}


# =============================================================================================== WEAPON MOTORS
# Outrunner model: stator base flange (base_d x base_h) with the motor mount bolt circle(s) tapped into its back face,
# bell can (bell_d x bell_len) with blade-mount holes in its top face, output shaft (shaft_d, protruding shaft_out past
# the bell top), optional rear shaft stub, and a lead bundle leaving the base radially. Lengths along X.
WEAPON_MOTORS = {
    "repeat_2004_1400kv": dict(
        name="Repeat Robotics DirectDrive 2004 1400 kV outrunner (3 mm through shaft, 3x M3 on 15 mm both ends)",
        bell_d=24.7, body_len=14.8, bell_len=13.8, base_d=10.0, base_h=1.0, shaft_d=3.0, overall=30.25, rear_stub=2.5,
        base_holes=[(15.0, 3, 3.0)], top_holes=[(15.0, 3, 3.0)], kv=1400, mass_g=18.0, cells="2-4S",
        max_current_a=None, wires_mm=None,
        src={"page": "https://shop.bristolbotbuilders.com/product/2004/",
             "drawing": "Repeat DirectDrive 2004 drawing (cloudfront original.PNG on the BBB page): dia 24.70, 30.25 overall, 14.80 body, "
                        "13.80 bell, 4.40 / 2.50 rear hub, dia 3.00 shaft, 3x M3 tap on dia 15 both faces",
             "mass": "BBB page: ~18 g incl. wires", "kv": "BBB page: 1400kv, 2800kv",
             "cad_ref": "research/cots/weapon_motor/repeat_2004/cad_ref (STEP bbox 24.70 x 30.75 x 24.70)"},
        derived="base_d/base_h: rear hub boss read off the drawing (4.40 - 2.50 hub step), not dimensioned as a diameter"),
    "repeat_2004_2800kv": dict(_like="repeat_2004_1400kv", kv=2800,
                               name="Repeat Robotics DirectDrive 2004 2800 kV outrunner (3 mm through shaft, 3x M3 on 15 mm both ends)"),
    "bbb_be1806_2300kv": dict(
        name="BBB BE1806 2300 kV outrunner (23 mm bell, 4x M2 base on 12/16 mm, 4x M2 top on 9 mm)",
        bell_d=23.0, body_len=18.5, bell_len=15.0, base_d=19.0, base_h=3.5, shaft_d=2.0, overall=21.5, rear_stub=0.0,
        base_holes=[(12.0, 2, 2.0, 0.0), (16.0, 2, 2.0, 90.0)], top_holes=[(9.0, 4, 2.0)], kv=2300, mass_g=23.0, cells="2-4S",
        max_current_a=None, wires_mm=150,
        src={"page": "https://shop.bristolbotbuilders.com/product/brushlessmotor/",
             "drawing": "be3.jpg on the BBB page: dia 23 bell, 18.5 body, 21.5 incl. shaft; bottom 4-M2 on dia 12 and dia 16; top 4-M2 on dia 9",
             "mass": "BBB page: ~23 g including wires (150 mm)", "shaft": "BBB page: 3x2mm output shaft / 2mm internal",
             "cad_ref": "research/cots/weapon_motor/bbb_be1806/cad_ref (STEP bbox 23.10 x 22.15 x 23.10, surfaces only)"},
        derived="bell_len 15 / base 19 x 3.5 split of the 18.5 body follows the existing be1806_bbb envelope"),
    "brotherhobby_tc1404_3800kv": dict(
        name="BrotherHobby TC 1404 3800 kV outrunner (18.2 x 16, 4x M2 on 9 mm base, 4x M2 on 5 mm bell, 1.5 mm shaft)",
        bell_d=18.2, body_len=12.0, bell_len=10.0, base_d=12.0, base_h=2.0, shaft_d=1.5, overall=16.0, rear_stub=0.0,
        base_holes=[(9.0, 4, 2.0)], top_holes=[(5.0, 4, 2.0)], kv=3800, mass_g=8.6, cells="4S",
        max_current_a=8.1, wires_mm=100, internal_resistance_mohm=322.4,
        src={"page": "https://www.brotherhobbystore.com/products/tc-1404-ultralight-motor-139",
             "drawing": "01bab18143.jpg: dia 18.2, 16 overall, 4 shaft stick-out, dia 1.5 shaft, 4-M2 on dia 9 (base), 4-M2 on dia 5 (bell)",
             "spec": "85357ed61f.jpg TC1404-3800KV table: 8.6 g (100 mm), phi18.2x16, 4S, 322.40 mOhm, 8.1 A max, 129.6 W, 30 AWG 100 mm",
             "note": "page text says 'Bolt Pattern M2 9X9'; the drawing dimensions it as a dia 9 circle - drawing used"},
        derived="body_len = 16 overall - 4 shaft; bell/base split of the body estimated from the drawing"),
    "brotherhobby_tc1404_4600kv": dict(_like="brotherhobby_tc1404_3800kv", kv=4600, mass_g=8.7, max_current_a=13.6, internal_resistance_mohm=207.48,
                                       name="BrotherHobby TC 1404 4600 kV outrunner (18.2 x 16, 4x M2 on 9 mm base, 1.5 mm shaft)"),
    "emax_eco2207_1900kv": dict(
        name="EMAX ECO 2207 1900 kV outrunner (27.45 x 32.6, 4x M3 16x16, M5 prop shaft)",
        bell_d=27.45, body_len=20.6, bell_len=16.0, base_d=22.0, base_h=4.6, shaft_d=5.0, overall=32.6, rear_stub=0.0,
        base_holes=[(16.0 * math.sqrt(2), 4, 3.0)], top_holes=[], kv=1900, mass_g=31.5, cells="3-6S",
        max_current_a=None, wires_mm=None,
        src={"page": "https://shop.emaxmodel.com/products/emax-eco-series-2207-3-6s-1700kv-1900kv-2400kv-brushless-motor-for-rc-drone-fpv-racing",
             "spec": "EMAX page: Length 32.6mm, Diameter 27.45mm, 12N14P, 31.5g (W/O silicone wire), prop adapter M5, 3-6s (1700/1900KV)",
             "mount": "https://shop.emax-usa.com/products/eco-ii-2207-brushless-motor-1700kv-1900kv-2400kv : 16x16mm mounting pattern",
             "note": "no dimension drawing published; mass excludes wires"},
        derived="M3 for the 16x16 pattern and the 12 mm M5 shaft stick-out (body 20.6) are assumed; 16x16 square = dia 22.6 circle at 45 deg"),
}

# ============================================================================================== DRIVE GEARMOTORS
# Micro metal gearmotor (N10 / N20 format): 12 x 10 gearbox block of length gb_len with 2x M1.6 tapped holes at
# +-hole_dx in its output face, output bushing, 3 mm D-shaft, round can (can_d with flats to `flats`) of can_len,
# brush end cap with two solder tabs.
GEARMOTOR_FORMAT = dict(gb_w=12.0, gb_h=10.0, can_d=12.0, flats=10.0, hole_d=1.6, hole_dx=4.5, bush_d=4.0, bush_h=0.7,
                        shaft_d=3.0, shaft_flat=2.5, tab_w=1.5, tab_t=0.3, tab_len=1.5,
                        src="Pololu micro-metal-gearmotors-dimensions.pdf (research/cots/drive_motor/pololu_mmgm/raw): 12.0 x 10.0 gearbox, "
                            "2x M1.6 at 4.5 either side of the shaft, dia 4.0 x 0.7 bushing, dia 3.0 D-shaft with 2.5 across the flat, 10 mm shaft, "
                            "gearbox L 9 (all but 1000:1), motor 15")
GEARMOTORS = {
    "pololu_hpcb6v_30to1": dict(
        name="Pololu 30:1 Micro Metal Gearmotor HPCB 6V (#3062/#3072)", gb_len=9.0, can_len=15.0, shaft_len=10.0, mass_g=None,
        nominal_v=6.0, rpm_nominal=1100.0, no_load_current_a=0.15, stall_current_a=1.5, stall_torque_gcm=450.0,
        src={"page": "https://www.pololu.com/product/3072", "spec": "1100 RPM, 150 mA, 1.5 A stall, 0.45 kg.cm (6.2 oz.in) stall",
             "dims": "GEARMOTOR_FORMAT drawing"}),
    "pololu_hpcb6v_50to1": dict(
        name="Pololu 50:1 Micro Metal Gearmotor HPCB 6V (#3063/#3073)", gb_len=9.0, can_len=15.0, shaft_len=10.0, mass_g=None,
        nominal_v=6.0, rpm_nominal=650.0, no_load_current_a=0.15, stall_current_a=1.5, stall_torque_gcm=740.0,
        src={"page": "https://www.pololu.com/product/3073", "datasheet": "https://www.pololu.com/file/0J1487/pololu-micro-metal-gearmotors-rev-6-2.pdf HPCB 6V table, items #3063/#3073: 51.45:1, 650 rpm, stall 7.4 kg.mm, 1.5 A",
             "dims": "GEARMOTOR_FORMAT drawing"}),
    "pololu_hpcb6v_75to1": dict(
        name="Pololu 75:1 Micro Metal Gearmotor HPCB 6V (#3064/#3074)", gb_len=9.0, can_len=15.0, shaft_len=10.0, mass_g=None,
        nominal_v=6.0, rpm_nominal=430.0, no_load_current_a=0.15, stall_current_a=1.5, stall_torque_gcm=1100.0,
        src={"page": "https://www.pololu.com/product/3074", "spec": "430 RPM, 150 mA, 1.5 A stall, 1.1 kg.cm stall", "dims": "GEARMOTOR_FORMAT drawing"}),
    "bbb_n20_600rpm": dict(
        name="BBB pair-of-N20 600 rpm gearmotor (50:1, 36 x 12 x 10)", gb_len=9.0, overall=36.0, shaft_len=9.0, mass_g=9.7,
        nominal_v=6.0, rpm_nominal=600.0, no_load_current_a=0.1, stall_current_a=None, stall_torque_gcm=None,
        src={"page": "https://shop.bristolbotbuilders.com/product/n20/",
             "spec": "36x12x10mm per motor, 9x3mm output shaft, 9.7g per motor, ~600rpm at 6V (50:1), no load ~0.1A at 7.8V",
             "cad_ref": "research/cots/drive_motor/bbb_n20/cad_ref (STEP bbox 12.00 x 36.20 x 10.00)"},
        derived="can_len = overall - shaft_len - gb_len - tab_len (gearbox length from the Pololu format drawing)"),
    "bbb_hpn20_1000rpm": dict(
        name="BBB High Power N20 1000 rpm gearmotor (35 x 12 x 10, ~2.2 A stall at 2S)", gb_len=9.0, overall=35.0, shaft_len=9.0, mass_g=9.5,
        nominal_v=6.0, rpm_nominal=1000.0, no_load_current_a=0.2, stall_current_a=2.2, stall_torque_gcm=None,
        src={"page": "https://shop.bristolbotbuilders.com/product/hpn20/",
             "spec": "35x12x10mm per motor, 9x3mm output shaft, ~9.5g, ~100/600/1000/1500rpm at 6V, no load ~0.2A, stall ~2.2A at 2S"},
        derived="can_len = overall - shaft_len - gb_len - tab_len"),
    "bbb_n10_600rpm": dict(
        name="BBBxN&B N10 600 rpm gearmotor (33 x 12 x 10, steel plates)", gb_len=9.0, overall=33.0, shaft_len=9.0, mass_g=8.0,
        nominal_v=6.0, rpm_nominal=600.0, no_load_current_a=0.1, stall_current_a=1.0, stall_torque_gcm=None,
        src={"page": "https://shop.bristolbotbuilders.com/product/n10/",
             "spec": "33x12x10mm per motor, 9x3mm output shaft, ~8g, ~100/300/600/1000/1500rpm at 6V, no load ~0.1A, stall ~1A at 7.8V",
             "cad_ref": "research/cots/drive_motor/bbb_n10/cad_ref (STEP bbox 12.00 x 10.00 x 32.50)"},
        derived="can_len = overall - shaft_len - gb_len - tab_len"),
    "bbb_n10_1000rpm": dict(_like="bbb_n10_600rpm", rpm_nominal=1000.0, name="BBBxN&B N10 1000 rpm gearmotor (33 x 12 x 10, steel plates)"),
}

# ===================================================================================================== BATTERIES
# Pack: l x w x h block with rounded long edges (soft pouch), lead pair leaving the +Y face, connector body at lead end.
BATTERIES = {
    "palmpower_2s_180_45c": dict(name="Palm Power Gen2 2S 180 mAh 45C (JST)", l=36.25, w=19.75, h=9.9, mass_g=13.3, cells=2, mah=180, c=45, conn="jst_rcy",
                                 src={"page": "https://palmbeachbots.com/products/palm-power-2s-180mah-45c-lipo-battery",
                                      "spec": "180mAh, 45C, 13.3g, 36.25x19.75x9.9mm (+/-), discharge plug JST"}),
    "palmpower_2s_300_65c": dict(name="Palm Power Gen2 2S 300 mAh 65C (JST)", l=46.25, w=16.25, h=13.2, mass_g=20.2, cells=2, mah=300, c=65, conn="jst_rcy",
                                 src={"page": "https://palmbeachbots.com/products/palm-power-2s-300mah-65c-lipo-battery",
                                      "spec": "300mAh, 65C, 20.2 g, 46.25x16.25x13.2mm (+/-), discharge plug JST"}),
    "tattu_2s_300_75c_hv": dict(name="Tattu 2S1P 300 mAh 75C HV 7.6 V (JST-PHR)", l=45.0, w=16.0, h=12.0, mass_g=16.0, cells=2, mah=300, c=75, conn="jst_ph",
                                hv=True, src={"page": "https://racedayquads.com/products/tattu-300mah-7-6v-75c-2s1p-lipo-jst",
                                              "spec": "300mAh, 7.6V, 75C (150C burst), 2S1P, net weight 16, L 45 / W 16 / H 12, connector JST"}),
    "betafpv_2s_300_45c": dict(name="BETAFPV 2S 300 mAh 45C (XT30)", l=45.0, w=17.0, h=12.0, mass_g=18.4, cells=2, mah=300, c=45, conn="xt30",
                               src={"page": "https://betafpv.com/products/300mah-2s-lipo-battery-2pcs",
                                    "spec": "Weight 18.4g, Size 45*17*12 mm, XT30 with 18AWG silicone wire"}),
    "gnb_2s_350_70c_hv": dict(name="GNB (Gaoneng) 2S 350 mAh 70C HV 7.6 V (XT30)", l=48.0, w=18.0, h=12.0, mass_g=17.0, cells=2, mah=350, c=70, conn="xt30",
                              hv=True, src={"page": "https://www.kiwiquads.co.nz/product/gnb-lipo-battery-7-6v-70c-350mah-2s-hv/",
                                            "spec": "XT30, 350mAh, 70C, 17g, 12*18*48mm"}),
    "gnb_2s_450_80c": dict(name="GNB (Gaoneng) 2S 450 mAh 80C (XT30)", l=61.0, w=17.0, h=14.0, mass_g=28.0, cells=2, mah=450, c=80, conn="xt30",
                           src={"page": "https://racedayquads.com/products/gaoneng-7-4v-2s-450mah-80c-lipo-whoop-micro-battery-w-xt30",
                                "spec": "450mAh, 7.6V nominal, 80C/160C, 14x17x61mm appr., 28g (+/-1g), XT30, JST-XH 3P balance"}),
    "gnb_3s_300_80c_hv": dict(name="GNB (Gaoneng) 3S 300 mAh 80C HV 11.4 V (XT30, GNB3003S80AHV)", l=53.0, w=17.0, h=18.0, mass_g=28.0, cells=3, mah=300, c=80,
                              conn="xt30", hv=True,
                              src={"page": "https://www.fpv24.com/en/gaoneng/gaoneng-gnb-lipo-akku-lihv-300mah-3s-114v-80c-xt30",
                                   "spec": "18 x 17 x 53 mm (H x W x L), 28g (+/-2g)"}),
}
BATTERY_LEAD = dict(len=30.0, d=1.6, pitch=3.0)   # assumed lead stub drawn on every pack (pigtail length varies by vendor)

# ========================================================================================================== ESCs
# Flat PCB in heat-shrink: l x w x h block, optional wire stubs out of the ends at the given port points.
ESCS = {
    "bbb_malenki_nano": dict(kind="esc", name="BBB Malenki-Nano (receiver + 3x 1 A brushed ESC + 2 PWM out)", l=32.0, w=19.0, h=2.5, mass_g=2.3,
                             ports={"bat": [-16.0, -6.0, 0], "m1": [16.0, 6.0, 0], "m2": [-16.0, 6.0, 0], "wpn": [16.0, -6.0, 0]},
                             props={"cont_current_a": 1.0, "burst_current_a": 1.8, "channels": 3.0, "max_cells": 2.0},
                             src={"page": "https://shop.bristolbotbuilders.com/product/malenki/",
                                  "spec": "32x19x2.5mm, 2.3g, 1-2S (3.6-10V), 3 channels of 1A continuous 1.8A peak, built-in AFHDS 2A receiver",
                                  "cad_ref": "research/cots/esc/bbb_malenki/cad_ref (zip)"}),
    "bbb_dual_esc_v31": dict(kind="esc", name="BBB Antweight Dual ESC v3.1 (2x 2 A brushed, 5 V 1 A BEC)", l=23.0, w=19.0, h=6.0, mass_g=7.0,
                             ports={"bat": [-11.5, -6.0, 0], "m1": [11.5, 6.0, 0], "m2": [11.5, -6.0, 0], "rx": [-11.5, 6.0, 0]},
                             props={"cont_current_a": 2.0, "burst_current_a": 4.0, "channels": 2.0, "max_cells": 4.0, "bec_a": 1.0},
                             src={"page": "https://shop.bristolbotbuilders.com/product/bbbv3/",
                                  "spec": "23x19x6mm, ~7g with motor wire cut to length, 2-4S, 2 channels of 2A continuous 4A peak, 5V 1A BEC"}),
    "bbb_brushless_esc_20a": dict(kind="esc", name="BBB Antweight Spinner Brushless ESC 20 A (no BEC)", l=23.0, w=12.0, h=4.0, mass_g=5.0,
                                  ports={"bat": [-11.5, -3.0, 0], "motor": [11.5, 0, 0], "rx": [-11.5, 3.0, 0]},
                                  props={"cont_current_a": 20.0, "burst_current_a": 25.0, "channels": 1.0, "max_cells": 4.0},
                                  src={"page": "https://shop.bristolbotbuilders.com/product/brushless/",
                                       "spec": "23x12x4mm (main pcb), ~5g including wires, 2-4S, 20A continuous, 25A burst for 10s, no BEC",
                                       "cad_ref": "research/cots/esc/bbb_brushless/cad_ref (STEP bbox 13.0 x 46.7 x 5.5 incl. leads)"}),
    "bbb_red_esc": dict(kind="esc", name="BBB N10/N20 Red ESC (single 1 A brushed, motor mounted)", l=20.0, w=11.6, h=4.0, mass_g=1.4,
                        ports={"motor": [10.0, 0, 0], "rx": [-10.0, 0, 0]},
                        props={"cont_current_a": 1.0, "burst_current_a": 1.8, "channels": 1.0, "max_cells": 2.0},
                        src={"page": "https://shop.bristolbotbuilders.com/product/redesc/",
                             "spec": "20x11.6x4mm, ~80mm cable, ~0.4g (1.4g including wire), 1-2S, 1A continuous 1.8A peak"}),
}

# ======================================================================================== CONNECTORS AND SWITCHES
CONNECTORS = {
    "xt30u_m": dict(name="Amass XT30U-M (male, controller side)", w=5.2, h=10.2, l=13.7, pin_pitch=5.0, pin_d=2.0, cup_len=3.0, mass_g=None,
                    rated_a=15.0, peak_a=30.0, awg=18,
                    src={"datasheet": "XT30U datasheet (LCSC C99101, research/cots/connector/amass_xt30/raw/XT30U_datasheet.pdf p7): "
                                      "5.20 x 10.20, 13.70 long, pins on 5.00, 3.00 solder cups; 15A rated, 30A peak, 0.70 mOhm, 18AWG"},
                    derived="pin_d 2.0 (XT30 is a 2 mm bullet family) is not dimensioned on the drawing"),
    "xt30u_f": dict(name="Amass XT30U-F (female, battery side)", w=5.2, h=10.2, l=12.4, pin_pitch=5.0, pin_d=2.0, cup_len=3.0, mass_g=None,
                    rated_a=15.0, peak_a=30.0, awg=18, src={"datasheet": "same sheet: XT30U-F 5.20 x 10.20, 12.40 long, 3.00 cups, 6.00 socket"}),
    "betafpv_bt20_m": dict(name="BETAFPV BT2.0 male", w=4.2, h=6.0, l=10.5, pin_pitch=None, pin_d=None, cup_len=0.0, mass_g=0.34,
                           rated_a=9.0, peak_a=15.0, awg=None,
                           src={"page": "https://www.fpvfaster.com.au/products/betafpv-bt2-0-connectors-male-female-5-pairs",
                                "spec": "Male 6.0*4.2*10.5mm, Female 6.0*4.2*8.3mm, Male 0.34g, Female 0.24g, 9A continuous 15A burst"}),
    "jst_phr2": dict(name="JST PHR-2 housing (2.0 mm pitch, 2 way)", w=4.5, h=5.8, l=6.0, pin_pitch=2.0, pin_d=None, cup_len=0.0, mass_g=None,
                     rated_a=2.0, peak_a=None, awg="32-24",
                     src={"page": "https://www.arrow.com/en/products/phr-2/jst-manufacturing.html",
                          "spec": "product length 5.8, depth 4.5, 2 A; JST ePH.pdf downloaded but its fonts are unrenderable here"},
                     derived="l (height along the wire) 6.0 is an estimate"),
}
SWITCHES = {
    "fingertech_mini_switch": dict(
        name="FingerTech Mini Power Switch (12.7 cube-ish, 2 holes on 7.62, 40 A)", body=(12.7, 12.7, 6.35), hole_pitch=7.62, hole_d=2.2,
        term_w=3.5, term_t=1.0, term_len=6.35, screw_d=3.0, mass_g=2.15, rated_a=40.0, burst_a=100.0,
        src={"page": "https://www.fingertechrobotics.com/proddetail.php?prod=ft-mini-switch",
             "spec": "12.7 x 12.7 x 6.35mm, terminals 3.5mm x 1mm extend 6.35mm, 2.15 g, two holes 7.62mm apart pass 2mm screws, 40A rated, 100A 10 s",
             "cad_ref": "research/cots/connector/fingertech_mini_switch/cad_ref/Mini_Power_Switch.IGS"},
        derived="hole_d 2.2 (M2 clearance) and the 3 mm actuating screw diameter are assumed"),
}

# ============================================================================================ WHEELS AND TYRES
# Fully parametric: tyre(od, tyre_t, width, tread) + hub(rim, width, bore, d_flat, boss, spokes); wheel() = both.
WHEEL_DEFAULTS = dict(od=34.0, width=6.5, tyre_t=3.25, bore=3.0, d_flat=2.5, hub_boss_d=7.0, boss_len=2.0, web_t=1.5,
                      spokes=3, spoke_w=2.0, tread="smooth", tread_n=0, tread_depth=0.0, tread_w=1.0, mass_g=None)
WHEELS = {
    "bbb_wheel_34x6_5": dict(name="BBB 34 mm antweight wheel (rubber tread, plastic hub, 3 mm D)", od=34.0, width=6.5, tyre_t=3.25, bore=3.0,
                             hub_boss_d=7.0, boss_len=2.0, spokes=3, mass_g=4.1,
                             src={"page": "https://shop.bristolbotbuilders.com/product/wheels/",
                                  "spec": "34mm diameter, 6.5mm tyre width, ~4.1g per wheel, 3mm D shaft; wheel2.jpg: 34MM, 6.5MM, 2MM boss",
                                  "cad_ref": "research/cots/wheel/bbb_wheels/cad_ref STEP: OD 34 (r17), rim r13.75, boss r3.5, bore r1.5, 8.6 wide"},
                             derived="tyre_t 3.25 (= 17 - 13.75) and boss dia 7 measured from the vendor STEP"),
    "bbb_wheel_22x10": dict(name="BBB 22 mm antweight wheel (10 mm rubber tyre, PLA+ hub)", od=22.0, width=10.7, tyre_t=1.75, bore=3.0,
                            hub_boss_d=12.5, boss_len=0.0, spokes=0, mass_g=3.5,
                            src={"page": "https://shop.bristolbotbuilders.com/product/22mmwheels/",
                                 "spec": "22mm diameter, 10.7mm max width, ~3.5g per wheel",
                                 "cad_ref": "research/cots/wheel/bbb_22mmwheels/cad_ref STEP: r11 OD, r9.25 rim, r6.25 boss, r1.5 bore, 10.7 wide"},
                            derived="tyre_t / boss from the vendor STEP"),
    "durahubs_25": dict(name="DuraHubs 25 mm (silicone tread, PLA-ST hub)", od=25.0, width=6.0, tyre_t=3.0, bore=3.0, boss_len=2.0, spokes=3,
                        tread="blocks", tread_n=30, tread_depth=0.7, mass_g=3.0,
                        src={"page": "https://shop.bristolbotbuilders.com/product/durahubs/",
                             "spec": "25/30/35mm diameter, 6mm (+2mm D-hole) or 14mm thick tyre, ~3g (25) ~4g (30) ~11g (35)"},
                        derived="tyre_t, tread count/depth scaled from the 35 mm STEP"),
    "durahubs_30": dict(_like="durahubs_25", name="DuraHubs 30 mm (silicone tread, PLA-ST hub)", od=30.0, tread_n=36, mass_g=4.0),
    "durahubs_35": dict(_like="durahubs_25", name="DuraHubs 35 mm wide (14 mm silicone tread)", od=36.0, width=14.0, boss_len=0.0, tyre_t=7.6,
                        hub_boss_d=8.0, tread_n=54, tread_depth=1.0, mass_g=11.0,
                        cad_ref="research/cots/wheel/bbb_durahubs/cad_ref STEP: 36.0 OD over 54 tread blocks (r17/r18), hub r10.4, boss r4, bore r1.5, 14 wide"),
}


def _resolve(table):
    out = {}
    for k, v in table.items():
        v = dict(v)
        base = v.pop("_like", None)
        out[k] = {**table[base], **v} if base else v
    return out


# ------------------------------------------------------------------------------------------------- generators
def outrunner(cid, s) -> CatalogEntry:
    """Outrunner on +X: base flange at the -X end, bell over the body, shaft out of the +X (bell) face."""
    L, bell_len, base_h = s["body_len"], s["bell_len"], s["base_h"]
    x0, x1 = -L / 2, L / 2
    shaft_out = s["overall"] - L - s["rear_stub"]
    stator_d = min(s["base_d"], s["bell_d"] - 2.0)
    bell = at(cyl_x(s["bell_d"] / 2, bell_len), x1 - bell_len / 2, 0, 0)
    gap = max(L - bell_len - base_h, 0.0)   # stator neck between base flange and bell (0 when the bell sits on the flange)
    neck = at(cyl_x(stator_d / 2 - 0.5, gap + 4 * EPS), x0 + base_h + gap / 2, 0, 0)
    base = at(cyl_x(s["base_d"] / 2, base_h), x0 + base_h / 2, 0, 0)
    shaft = at(cyl_x(s["shaft_d"] / 2, shaft_out + EPS), x1 + shaft_out / 2 - EPS / 2, 0, 0)
    parts = [bell, base, shaft, neck]
    if s["rear_stub"] > 0:
        parts.append(at(cyl_x(s["shaft_d"] / 2, s["rear_stub"] + EPS), x0 - s["rear_stub"] / 2 + EPS / 2, 0, 0))
    lead_r = 0.6
    lead_x = x0 + base_h / 2
    leads = [at(rot(cyl(lead_r, s["base_d"] / 2 + 3.0), [90, 0, 0]), lead_x, -(s["base_d"] / 2 + 3.0) / 2, z) for z in (-1.4, 0.0, 1.4)]
    depth = 3.0
    cuts = []
    for spec in s["base_holes"]:
        pcd, n, d = spec[:3]
        cuts += holes_x(bolt_circle(pcd, n, spec[3] if len(spec) > 3 else 45.0), d * 0.8, x0, 2 * depth)
    for spec in s["top_holes"]:
        pcd, n, d = spec[:3]
        cuts += holes_x(bolt_circle(pcd, n, spec[3] if len(spec) > 3 else 45.0), d * 0.8, x1, 2 * min(depth, bell_len / 2))
    props = {"kv": s["kv"], "max_current_a": s.get("max_current_a") or 15.0, "typ_current_a": (s.get("max_current_a") or 15.0) / 2,
             "bell_mass_frac": 0.5, "cells": s["cells"], "lead_len_mm": s.get("wires_mm"),
             "mount_holes": [list(h) for h in s["base_holes"]], "top_holes": [list(h) for h in s["top_holes"]],
             # mounting geometry (catalog frame): stator base back / bell top, bell radius and length, base flange, shaft through the body
             "body_x": [x0, x1], "bell_r": s["bell_d"] / 2, "bell_len": bell_len, "base_h": base_h, "base_r": s["base_d"] / 2,
             "base_hub_r": s["shaft_d"] / 2 + 1.0, "rear_stub": s["rear_stub"], "shaft_thread_mm": 0.0, "shaft_through": True}
    if s.get("internal_resistance_mohm"):
        props["internal_resistance_mohm"] = s["internal_resistance_mohm"]
    return CatalogEntry(cid, "weapon_motor", s["name"], s["mass_g"], "datasheet", union([minus(union(parts), cuts)] + leads),
                        {"phases": [lead_x, -(s["base_d"] / 2 + 3.0), 0]},
                        {"at": [x1, 0, 0], "dir": [1, 0, 0], "len": shaft_out, "dia": s["shaft_d"]}, props, "#3a3d42", s["src"].get("page", ""))


def gearmotor(cid, s, f=GEARMOTOR_FORMAT) -> CatalogEntry:
    """Micro metal gearmotor on +X: brush cap at -X, can, gearbox, bushing, D-shaft out of +X."""
    can_len = s.get("can_len") or s["overall"] - s["shaft_len"] - s["gb_len"] - f["tab_len"]   # vendor overall includes shaft and tabs
    body = can_len + s["gb_len"]
    x0, x_gb = -body / 2, -body / 2 + can_len
    x1 = body / 2
    can = at({"type": "intersect", "items": [cyl_x(f["can_d"] / 2, can_len), box(can_len + 1, f["can_d"] + 1, f["flats"])]}, x0 + can_len / 2, 0, 0)
    gb = at(box(s["gb_len"], f["gb_w"], f["gb_h"]), x_gb + s["gb_len"] / 2, 0, 0)
    bush = at(cyl_x(f["bush_d"] / 2, f["bush_h"] + EPS), x1 + f["bush_h"] / 2 - EPS / 2, 0, 0)
    shaft = at(d_shaft_x(f["shaft_d"], f["shaft_flat"], s["shaft_len"] + EPS), x1 + s["shaft_len"] / 2 - EPS / 2, 0, 0)
    tabs = [at(box(f["tab_len"] + EPS, f["tab_w"], f["tab_t"]), x0 - f["tab_len"] / 2 + EPS / 2, y, 0) for y in (-3.0, 3.0)]
    holes = holes_x([(-f["hole_dx"], 0.0), (f["hole_dx"], 0.0)], f["hole_d"] * 0.8, x1, 6.0)
    props = {k: s[k] for k in ("nominal_v", "rpm_nominal", "stall_current_a", "no_load_current_a", "stall_torque_gcm") if s.get(k) is not None}
    props["mount_holes_mm"] = [[x1, -f["hole_dx"], 0.0], [x1, f["hole_dx"], 0.0]]
    props["mount_thread"] = "M1.6"
    mass = s["mass_g"] if s["mass_g"] is not None else 9.5
    conf = "datasheet" if s["mass_g"] is not None else "estimate"
    return CatalogEntry(cid, "motor", s["name"], mass, conf, minus(union([can, gb, bush, shaft] + tabs), holes),
                        {"terminals": [x0 - f["tab_len"], 0, 0]},
                        {"at": [x1, 0, 0], "dir": [1, 0, 0], "len": s["shaft_len"], "dia": f["shaft_d"]}, props, "#9aa0a6",
                        s["src"].get("page", s["src"].get("datasheet", "")))


def connector_body(c):
    """Connector housing mating along +X, centred on the origin, pin holes in the +X face."""
    shape = box(c["l"], c["w"], c["h"])
    if c.get("pin_pitch") and c.get("pin_d"):
        shape = minus(shape, holes_x([(0.0, -c["pin_pitch"] / 2), (0.0, c["pin_pitch"] / 2)], c["pin_d"], c["l"] / 2, c["l"] - c["cup_len"]))
    return shape


def lipo(cid, s) -> CatalogEntry:
    l, w, h = s["l"], s["w"], s["h"]
    r = min(h, w) * 0.2
    pouch = union([box(l, w - 2 * r, h), box(l, w, h - 2 * r)] + [at(cyl_x(r, l), 0, sy * (w / 2 - r), sz * (h / 2 - r)) for sy in (-1, 1) for sz in (-1, 1)])
    lead = BATTERY_LEAD
    leads = [at(rot(cyl(lead["d"] / 2, lead["len"] + EPS), [90, 0, 0]), dx, w / 2 + lead["len"] / 2 - EPS / 2, 0) for dx in (-lead["pitch"] / 2, lead["pitch"] / 2)]
    conn = CONNECTORS.get({"xt30": "xt30u_f", "jst_ph": "jst_phr2"}.get(s["conn"], ""), None)
    parts = [pouch] + leads
    port_y = w / 2 + lead["len"]
    if conn:
        parts.append(at(rot(connector_body(conn), [0, 0, 90]), 0, port_y + conn["l"] / 2 - EPS, 0))
        port_y += conn["l"]
    cells = s["cells"]
    nominal = (3.8 if s.get("hv") else 3.7) * cells
    return CatalogEntry(cid, "battery", s["name"], s["mass_g"], "datasheet", union(parts), {s["conn"]: [0, port_y, 0]}, None, {
        "cells": cells, "capacity_mah": s["mah"], "c_rating": s["c"], "nominal_v": nominal,
        "internal_resistance_mohm": 90 / max(s["mah"] / 100, 0.5) * cells}, "#2a9d8f", s["src"]["page"])


def esc(cid, s) -> CatalogEntry:
    l, w, h = s["l"], s["w"], s["h"]
    board = union([box(l, w - h, h), box(l - h, w, h)] + [at(cyl_x(h / 2, l - h), 0, sy * (w / 2 - h / 2), 0) for sy in (-1, 1)])
    return CatalogEntry(cid, s["kind"], s["name"], s["mass_g"], "datasheet", board, dict(s["ports"]), None, dict(s["props"]),
                        "#e76f51" if s["props"]["channels"] > 1 else "#d4af37", s["src"]["page"])


def connector(cid, s) -> CatalogEntry:
    props = {"rated_current_a": s["rated_a"], "peak_current_a": s["peak_a"], "awg": s["awg"]}
    return CatalogEntry(cid, "connector", s["name"], s["mass_g"] if s["mass_g"] is not None else 0.5,
                        "datasheet" if s["mass_g"] is not None else "estimate", connector_body(s),
                        {"mate": [s["l"] / 2, 0, 0], "wire": [-s["l"] / 2, 0, 0]}, None, props, "#f2b134", next(iter(s["src"].values())))


def power_switch(cid, s) -> CatalogEntry:
    bx, by, bz = s["body"]
    body = minus(box(bx, by, bz), [at(cyl(s["hole_d"] / 2, bz + 1), sx * s["hole_pitch"] / 2, 0, 0) for sx in (-1, 1)]
                 + [at(cyl(s["screw_d"] / 2, bz + 1), 0, by / 4, 0)])
    terms = [at(box(s["term_w"], s["term_len"] + EPS, s["term_t"]), sx * s["hole_pitch"] / 2, -by / 2 - s["term_len"] / 2 + EPS / 2, 0) for sx in (-1, 1)]
    pts = {"in": [-s["hole_pitch"] / 2, -by / 2 - s["term_len"], 0], "out": [s["hole_pitch"] / 2, -by / 2 - s["term_len"], 0]}
    return CatalogEntry(cid, "switch", s["name"], s["mass_g"], "datasheet", union([body] + terms), pts, None,
                        {"rated_current_a": s["rated_a"], "burst_current_a": s["burst_a"], "mount_thread": "M2",
                         "mount_holes_mm": [[-s["hole_pitch"] / 2, 0, bz / 2], [s["hole_pitch"] / 2, 0, bz / 2]]}, "#111111", s["src"]["page"])


# ---------------------------------------------------------------------------------------------- wheels / tyres
def _wheel_params(**kw):
    p = {**WHEEL_DEFAULTS, **{k: v for k, v in kw.items() if v is not None}}
    if p["tyre_t"] <= 0 or p["tyre_t"] >= p["od"] / 2 - p["bore"] / 2:
        raise ValueError("tyre_t must be > 0 and leave room for the hub")
    if not 0 < p["d_flat"] <= p["bore"]:
        raise ValueError("d_flat must be in (0, bore]")
    return p


def tyre_shape(od, width, tyre_t, tread="smooth", tread_n=0, tread_depth=0.0, tread_w=1.0, **_):
    """Tyre on the X axis: annulus od/2 .. od/2 - tyre_t, `width` wide. tread: 'smooth', 'grooves' (circumferential
    channels), or 'blocks' (`tread_n` axial bars `tread_depth` deep)."""
    r_o, r_i = od / 2, od / 2 - tyre_t
    t = ring_x(r_o, r_i, width)
    if tread == "blocks" and tread_n > 0 and tread_depth > 0:
        cuts = [rot(at(box(width + 1, tread_w, 2 * tread_depth), 0, 0, r_o), [360.0 * i / tread_n + 180.0 / tread_n, 0, 0]) for i in range(tread_n)]
        t = minus(t, cuts)
    elif tread == "grooves" and tread_n > 0 and tread_depth > 0:
        pitch = width / (tread_n + 1)
        cuts = [at(ring_x(r_o + 1, r_o - tread_depth, tread_w), -width / 2 + pitch * (i + 1), 0, 0) for i in range(tread_n)]
        t = minus(t, cuts)
    return t


def hub_shape(od, width, tyre_t, bore, d_flat, hub_boss_d, boss_len, web_t, spokes, spoke_w, **_):
    """Hub on the X axis: rim under the tyre, central web (solid, or `spokes` spokes with windows), boss of
    `hub_boss_d` standing `boss_len` proud of the -X face, D-bore `bore` with `d_flat` across the flat."""
    r_rim = od / 2 - tyre_t
    rim_t = min(1.2, r_rim / 4)
    parts = [ring_x(r_rim + EPS, r_rim - rim_t, width)]
    web = cyl_x(r_rim - rim_t + EPS, web_t)
    if spokes and spokes > 0:
        win_r_in, win_r_out = hub_boss_d / 2 + 0.6, r_rim - rim_t - 0.6
        if win_r_out - win_r_in > 1.0:
            windows = [rot(at(box(web_t + 1, (win_r_out - win_r_in) * 0.9, win_r_out - win_r_in), 0, 0, (win_r_in + win_r_out) / 2),
                           [360.0 * i / spokes + 180.0 / spokes, 0, 0]) for i in range(spokes)]
            web = minus(web, windows)
    parts.append(at(web, 0, 0, 0))
    boss_total = width + boss_len
    parts.append(at(cyl_x(hub_boss_d / 2, boss_total), -boss_len / 2, 0, 0))
    bore_cut = rot(d_bore_z(bore, d_flat, boss_total + 2), [0, 90, 0])
    return minus(union(parts), [at(bore_cut, -boss_len / 2, 0, 0)])


def wheel_mass_g(p):
    """Mass from volumes: tyre annulus in silicone + hub (rim, web, boss) in PLA, ignoring windows and tread."""
    r_o, r_i = p["od"] / 2, p["od"] / 2 - p["tyre_t"]
    tyre = math.pi * (r_o ** 2 - r_i ** 2) * p["width"]
    rim = math.pi * (r_i ** 2 - (r_i - min(1.2, r_i / 4)) ** 2) * p["width"]
    web = math.pi * (r_i - 1.2) ** 2 * p["web_t"] * (0.5 if p["spokes"] else 1.0)
    boss = math.pi * ((p["hub_boss_d"] / 2) ** 2 - (p["bore"] / 2) ** 2) * (p["width"] + p["boss_len"])
    return (tyre * SILICONE_G_CM3 + (rim + web + boss) * PLA_G_CM3) / 1000.0


def wheel(cid=None, name=None, **kw) -> CatalogEntry:
    """Parametric wheel: tyre + hub. Any of WHEEL_DEFAULTS can be overridden (od, width, tyre_t, bore, d_flat,
    hub_boss_d, boss_len, web_t, spokes, spoke_w, tread, tread_n, tread_depth, tread_w, mass_g)."""
    src = kw.pop("src", None)
    for k in ("derived", "cad_ref"):
        kw.pop(k, None)
    p = _wheel_params(**kw)
    cid = cid or f"wheel_p_{p['od']:g}x{p['width']:g}_b{p['bore']:g}"
    mass = p["mass_g"] if p["mass_g"] is not None else round(wheel_mass_g(p), 2)
    w = p["width"]
    shape = union([tyre_shape(**p), hub_shape(**p)])
    return CatalogEntry(cid, "wheel", name or f"{p['od']:g} x {w:g} mm parametric wheel ({p['tread']} tyre, {p['bore']:g} mm D-bore)",
                        mass, "datasheet" if p["mass_g"] is not None else "estimate", shape, {},
                        {"at": [-w / 2 - p["boss_len"], 0, 0], "dir": [1, 0, 0], "len": w + p["boss_len"], "dia": p["bore"]},
                        {"diameter_mm": p["od"], "width_mm": w, "friction": 0.9, "tyre_t_mm": p["tyre_t"], "bore_mm": p["bore"],
                         "d_flat_mm": p["d_flat"], "tread": p["tread"], "params": {k: p[k] for k in WHEEL_DEFAULTS}},
                        "#25282c", (src or {}).get("page", "parametric"))


def tyre(cid=None, **kw) -> CatalogEntry:
    """Parametric tyre alone (kind 'tyre'), for printing/moulding or fitting to a custom hub."""
    kw.pop("src", None)
    p = _wheel_params(**kw)
    cid = cid or f"tyre_p_{p['od']:g}x{p['width']:g}_t{p['tyre_t']:g}"
    r_o, r_i = p["od"] / 2, p["od"] / 2 - p["tyre_t"]
    mass = round(math.pi * (r_o ** 2 - r_i ** 2) * p["width"] * SILICONE_G_CM3 / 1000.0, 2)
    return CatalogEntry(cid, "tyre", f"{p['od']:g} x {p['width']:g} mm tyre, {p['tyre_t']:g} thick ({p['tread']})", mass, "estimate",
                        tyre_shape(**p), {}, None, {"diameter_mm": p["od"], "inner_diameter_mm": 2 * r_i, "width_mm": p["width"]}, "#25282c", "parametric")


# ------------------------------------------------------------------------------------------------------ registry
def entries() -> list[CatalogEntry]:
    out = [outrunner(k, s) for k, s in _resolve(WEAPON_MOTORS).items()]
    out += [gearmotor(k, s) for k, s in _resolve(GEARMOTORS).items()]
    out += [lipo(k, s) for k, s in BATTERIES.items()]
    out += [esc(k, s) for k, s in ESCS.items()]
    out += [connector(k, s) for k, s in CONNECTORS.items()]
    out += [power_switch(k, s) for k, s in SWITCHES.items()]
    out += [wheel(k, **{kk: vv for kk, vv in s.items() if kk != "name"}, name=s["name"]) for k, s in _resolve(WHEELS).items()]
    return out


def sources() -> dict:
    """id -> source dict, for the INDEX / BOM."""
    out = {}
    for table in (_resolve(WEAPON_MOTORS), _resolve(GEARMOTORS), BATTERIES, ESCS, CONNECTORS, SWITCHES, _resolve(WHEELS)):
        for k, s in table.items():
            out[k] = s.get("src", {})
    return out
