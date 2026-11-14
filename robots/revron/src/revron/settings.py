"""Revron design settings: every build choice of the generator, declared once (name, type, default, allowed values, doc,
legacy env var). `python -m robot.design schema robots/revron` prints this as JSON.

The generator modules read a setting where they use it, as `setting("REVRON_X", "<default>")` (robot.design.value): the
active robot.design.Design if it sets it, else the env var REVRON_X, else the default. They read at IMPORT time into
module constants, so one import of the `revron` package is one design; `build_revron(design)` imports the package afresh
under the design and puts the previous modules back.

This file imports nothing from the package (robot.design.load_settings loads it on its own, without building anything).
robot/tests/test_design.py keeps the defaults and allowed values here in step with the read sites and hooks.json.
"""
import os, sys
SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # robots/revron/src
ROOT = os.path.abspath(os.path.join(SRC, "..", "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from robot.design import Schema, Setting, fresh_import, use, value as setting   # noqa: E402,F401  (setting: the read the generator modules call)

SIZE_DOC = "a delta in mm (4, \"-3.5\") or a percentage of the stock dimension (\"10%\"; the swept steps are -30% .. 30% in tens). A shrink stops where the contents touch"
SCHEMA = Schema("revron", [
    Setting("weapon.type", "choice", "drisk", env="REVRON_WEAPON_TYPE", choices=("drisk", "vspin_drum", "vspin_eggbeater", "hspin_bar"),
            doc="weapon style. Only drisk is built: any other value fails the build with the reason (WeaponTypeError)"),
    Setting("weapon.motor", "choice", "gr1507", env="REVRON_WEAPON_MOTOR",
            choices=("gr1507", "gr1507_step", "bbb_be1806_2300kv", "brotherhobby_tc1404_3800kv", "brotherhobby_tc1404_4600kv", "repeat_2004_1400kv", "repeat_2004_2800kv",
                     "emax_eco2207_1900kv", "bl_1806_2300kv", "bl_2306_1400kv", "be1806_bbb", "c_bbb_be1806_2300kv", "c_repeat_2004_antweight_spinner_motor"),
            doc="catalog id of the weapon motor: stator, bell, shaft, mount bores and spider screws come from that entry; a motor that does not fit fails the build with the reason"),
    Setting("weapon.motor_variant", "choice", "datasheet", env="REVRON_MOTOR_VARIANT", choices=("datasheet", "step"),
            doc="model of the GR1507 (only when weapon.motor is gr1507): datasheet = the real motor, step = the simplified RVRN 2.0 STEP motor"),
    Setting("weapon.mount_variant", "choice", "original", env="REVRON_MOUNT_VARIANT", choices=("original", "printable"),
            doc="weapon mounts RV02 / RV03: original = as the STEP draws them; printable = nose pad, thickened notch tip, relieved corners, loose screw holes"),
    Setting("weapon.lead_groove", "flag", "off", env="REVRON_LEAD_GROOVE",
            doc="cut the snap-in C-groove for the motor phase leads in RV03 (off = the original: leads taped over the lug)"),
    Setting("wheel.rear", "choice", "stock", env="REVRON_REAR_WHEEL",
            choices=("stock", "wheel_20x8", "wheel_28x10", "wheel_30x8", "bbb_wheel_22x10", "bbb_wheel_34x6_5", "durahubs_25", "durahubs_30", "durahubs_35"),
            doc="rear wheel: stock = the RVRN 2.0 tyre (21.5 x 9.5), else a catalog wheel id; it sizes the tyre and sets the rear axle height"),
    Setting("chassis.compartments", "choice", "standard", env="REVRON_COMPARTMENTS", choices=("standard", "none", "split_battery_bay"),
            doc="interior layout of the tub: standard = motor pockets and pack bay; none = no compartment features; split_battery_bay = standard plus a rib between the pack and the electronics"),
    Setting("size.width", "size", "0", env="REVRON_SIZE_WIDTH", doc="overall width, both side walls move: " + SIZE_DOC + " (the two gearmotors a skin apart, the pack clear of the insert columns)"),
    Setting("size.length", "size", "0", env="REVRON_SIZE_LENGTH", doc="overall length, the nose moves (front wall, front axle, weapon axis); the rear wall and drive axle stay: " + SIZE_DOC + " (the pack against the front wall)"),
    Setting("size.height", "size", "0", env="REVRON_SIZE_HEIGHT", doc="overall height, the rim moves (deck, top panel, weapon axis): " + SIZE_DOC + " (the gearbox top under the deck)"),
    Setting("drive.location", "choice", "rear", env="REVRON_DRIVE_LOCATION", choices=("rear", "mid", "front", "front_motors_rear_driven"),
            doc="axle line of the drive gearmotors; the motor pockets and the pack bay follow it. front_motors_rear_driven is declared but not built (DriveLocationError)"),
    Setting("drive.motor", "choice", "n10_2200rpm_spicy", env="REVRON_DRIVE_MOTOR",
            choices=("n10_2200rpm_spicy", "n10_300rpm_6v", "n10_2200rpm_6v", "n20_1000rpm_6v", "pololu_hpcb6v_30to1", "pololu_hpcb6v_50to1", "pololu_hpcb6v_75to1", "bbb_n20_600rpm",
                     "bbb_hpn20_1000rpm", "bbb_n10_600rpm", "bbb_n10_1000rpm", "c_pair_of_600rpm_antweight_n20_gearmotors", "c_bbb_high_power_n20_gearmotor", "c_bbbxn_b_antweight_n10_gearmotors"),
            doc="catalog id of the two drive gearmotors; the tub pockets, key tab, stop wall and the size floors are derived from it"),
    Setting("switch.power", "choice", "switch_bbb_ant_rvrn2", env="REVRON_SWITCH", choices=("switch_bbb_ant_rvrn2", "switch_slide_12x4", "switch_slide_bbb_ant", "fingertech_mini_switch"),
            doc="catalog id of the power switch; its pad, pilots, screws and pocket in the tub are derived from it"),
    Setting("battery.pack", "choice", "lipo_2s_180_turnabot", env="REVRON_BATTERY",
            choices=("lipo_2s_180_turnabot", "lipo_2s_180", "lipo_2s_350", "lipo_1s_300", "palmpower_2s_180_45c", "palmpower_2s_300_65c", "tattu_2s_300_75c_hv", "betafpv_2s_300_45c",
                     "gnb_2s_350_70c_hv", "gnb_2s_450_80c", "gnb_3s_300_80c_hv", "c_palm_power_2s_300mah_65c_us_ref_not_uk", "c_typical_2s_300mah_lipo_lihv_betafpv_tbs_"),
            doc="catalog id of the pack; the bay is cut from its envelope. A pack too large for the chassis fails the build (grow size.width / size.length)"),
    Setting("drive.esc", "choice", "malenki_nano_rvrn2", env="REVRON_RXESC",
            choices=("malenki_nano_rvrn2", "esc_dual_brushed", "malenki_nano", "bbb_malenki_nano", "bbb_dual_esc_v31", "c_malenki_nano_antweight_esc_receiver", "c_bbb_antweight_dual_esc_v3_1",
                     "c_antweight_n10_n20_red_esc_motor_mounted"),
            doc="catalog id of the receiver / drive ESC; its bay is cut from the envelope"),
    Setting("weapon.esc", "choice", "bbb_ant_esc_rvrn2", env="REVRON_WESC",
            choices=("bbb_ant_esc_rvrn2", "esc_brushless_12a", "bbb_ant_esc", "bbb_brushless_esc_20a", "bbb_red_esc", "c_bbb_antweight_spinner_brushless_esc"),
            doc="catalog id of the weapon ESC; its bay is cut from the envelope"),
    Setting("variants", "set", "", env="REVRON_VARIANTS", choices=("battery_pad", "esc_tray", "rxesc_strap", "base_csk_fit", "open_keyhole", "pad_preload", "nut_press"),
            doc="deliberate departures from the original RVRN 2.0, all off by default (variants.py lists what each one changes)"),
])


def build_revron(design=None, model_file="src/build_revron.py"):
    """The Revron spec dict built under `design` (None = env / defaults, a dict {setting: value}, or a robot.design.Design).

    In-process and without setting env vars; safe to call again with another design. The `revron` package is imported
    afresh for the call and the modules that were loaded before are put back after it, so the import-time constants of
    a `revron` imported elsewhere do not change. Limits: the import swap is process-global (locked, but not safe against
    another thread importing `revron` meanwhile); the returned spec names its parts by `model_file`, so building their
    GEOMETRY later needs the same design again (`with use(design), fresh_import("revron", SRC)`, or a subprocess given
    `design.env()`)."""
    import importlib
    design = SCHEMA.design(design)
    with use(design), fresh_import("revron", SRC):
        return importlib.import_module("revron.spec").full_spec(model_file)


build = build_revron   # robot.design.build_spec entry
