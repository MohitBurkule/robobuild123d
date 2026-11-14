"""Data model of the wiring harness: the one contract every module of `robot.wiring` shares.

Pipeline (see plan.py):  devices -> terminals (typed, placed, with an exit axis)
                         netlist  -> nets and conductors (who connects to whom, at what current)
                         field    -> free space, keep-outs (rotating parts, fasteners, weapon), walls
                         router   -> bundles and smooth B-spline centrelines that respect each gauge's bend radius
                         solids   -> swept round wire solids in their insulation colour, connector bodies
                         channels -> cable channels and tie points in the chassis, derived from the routes
                         checks   -> clearance, bend radius, length / slack, current vs gauge, lid pinch, exposure

Units mm, grams, amps. World frame: X lateral, Y forward, Z up. Nothing here is Revron-specific: every number lives in
the gauge / connector catalogues (data/*.json) or in the named settings (settings.py), never in code.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

# Net / conductor kinds (the spec's wires[].kind) and terminal roles.
POWER, MOTOR, SIGNAL = "power", "motor", "signal"
KINDS = (POWER, MOTOR, SIGNAL)
POS, NEG = "pos", "neg"                                  # battery + / -
PHASE_A, PHASE_B, PHASE_C = "phase_a", "phase_b", "phase_c"   # brushless phases
MOTOR_A, MOTOR_B = "motor_a", "motor_b"                  # brushed motor tabs
SIG, VCC, GND = "sig", "vcc", "gnd"                      # servo-style signal lead
ROLES = (POS, NEG, PHASE_A, PHASE_B, PHASE_C, MOTOR_A, MOTOR_B, SIG, VCC, GND)
PHASES = (PHASE_A, PHASE_B, PHASE_C)
HALF = 1 / 2   # radius = HALF x diameter (named so no bare literal repeats through the package)
ROLES_OF_KIND = {POWER: (POS, NEG), MOTOR: PHASES, SIGNAL: (SIG, VCC, GND)}   # default roles a `kind` lead carries


@dataclass(frozen=True)
class Gauge:
    """One real hook-up wire size (silicone insulated, fine stranded), a row of data/gauges.json."""

    awg: int
    conductor_d_mm: float      # stranded conductor diameter
    od_mm: float               # over the insulation
    min_bend_r_mm: float       # static inside bend radius of the centreline
    g_per_mm: float            # copper + insulation
    amps_cont: float           # continuous, short chassis runs
    amps_burst: float          # seconds (stall, spin-up)
    ohm_per_m: float
    strands: str = ""          # e.g. "65/0.08"
    insulation: str = "silicone"

    @property
    def r_mm(self) -> float:
        return self.od_mm * HALF


@dataclass(frozen=True)
class ConnectorType:
    """A catalogue connector (or solder joint) with typed pins, a row of data/connectors.json.

    Local frame: origin at the centre of the mating face, +X = the direction the wires LEAVE the housing (so the mating
    half sits on -X). Pins are spread along Y at `pitch_mm`, centred."""

    id: str                    # e.g. "jst_ph_2", "xt30_m", "bullet_2mm_f", "solder_pad"
    family: str                # "jst_ph", "jst_sh", "micro_jst_1.25", "xt30", "bullet_2mm", "solder_pad", "solder_tab", ...
    pins: int
    pitch_mm: float
    body_mm: tuple             # housing (length along X, width along Y, height along Z); zeros for a bare solder joint
    gender: str                # "m" | "f" | "" (solder)
    amps_per_pin: float
    awg_min: int               # thinnest wire the crimp / cup takes (largest AWG number)
    awg_max: int               # thickest (smallest AWG number)
    mass_g: float
    unplug_mm: float           # travel along -X to separate the halves: the service slack one end needs
    boot_mm: float             # stiff length behind the housing (crimp barrel, heat-shrink) the wire leaves straight
    mates_with: tuple = ()     # connector ids this one plugs into
    solder: bool = False
    polarised: bool = True
    colour: str = "#e8e4d8"

    def pin_offsets(self) -> np.ndarray:
        """(pins, 3) local positions of the wire exits on the back of the housing."""
        k = np.arange(self.pins) - (self.pins - 1) * HALF
        out = np.zeros((self.pins, 3))
        out[:, 0] = self.body_mm[0]
        out[:, 1] = k * self.pitch_mm
        return out


@dataclass(frozen=True)
class Terminal:
    """One electrical connection point of a device, in the device's local frame."""

    device: str                # part id
    name: str                  # port name; ref = "device.name"
    role: str                  # one of ROLES
    pos: tuple                 # local position of the wire exit
    axis: tuple                # local unit vector the wire leaves along
    connector: str = "solder_pad"   # ConnectorType id on the DEVICE side
    pin: int = 0               # pin index inside that connector
    group: str = ""            # terminals sharing a housing / lead set share a group (e.g. "bat", "phases")
    pigtail_mm: float = 0.0    # length of factory lead already on the device (battery lead, motor phases)
    pigtail_awg: int | None = None
    max_a: float | None = None

    @property
    def ref(self) -> str:
        return f"{self.device}.{self.name}"


@dataclass(frozen=True)
class WorldTerminal:
    """A Terminal placed in the world frame (after part placement, mates and joints)."""

    terminal: Terminal
    pos: np.ndarray            # (3,)
    axis: np.ndarray           # (3,) unit

    @property
    def ref(self) -> str:
        return self.terminal.ref


@dataclass
class Net:
    """An electrical node: every pin on it is at the same potential."""

    id: str
    kind: str                  # POWER | MOTOR | SIGNAL
    role: str                  # one of ROLES
    pins: list = field(default_factory=list)       # terminal refs
    amps_cont: float = 0.0     # worst continuous current through any branch
    amps_burst: float = 0.0
    volts: float = 0.0


@dataclass
class Conductor:
    """One physical insulated wire between two terminals (a branch of a net)."""

    id: str
    net: str
    a: str                     # terminal ref
    b: str
    kind: str
    role: str
    awg: int
    colour: str                # insulation colour (hex)
    lead: str = ""             # the spec wire (or derived lead) it belongs to: conductors of one lead run as one bundle
    slack_mm: float | None = None    # declared; None = derived from the end connectors (settings.slack)
    amps_cont: float = 0.0
    amps_burst: float = 0.0
    via: list = field(default_factory=list)        # optional designer waypoints (world)
    waive: dict = field(default_factory=dict)      # {"harness.<check>": reason}
    splice_a: bool = False     # end a joins another conductor (Y-splice), not a device terminal
    splice_b: bool = False


@dataclass
class Netlist:
    nets: list = field(default_factory=list)
    conductors: list = field(default_factory=list)
    problems: list = field(default_factory=list)   # [(code, message, refs)]: unknown port, open net, role clash...

    def net(self, nid):
        return next((n for n in self.nets if n.id == nid), None)

    def conductor(self, cid):
        return next((c for c in self.conductors if c.id == cid), None)

    def leads(self) -> dict:
        """lead id -> its conductors, in declaration order."""
        out: dict = {}
        for c in self.conductors:
            out.setdefault(c.lead or c.id, []).append(c)
        return out


@dataclass
class WirePath:
    """The routed centreline of one conductor: a clamped cubic B-spline and its dense sampling."""

    conductor: str
    ctrl: np.ndarray           # (n, 3) B-spline control points (world)
    pts: np.ndarray            # (m, 3) samples every settings.spline.sample_mm
    od_mm: float
    length_mm: float           # arc length of the centreline, service slack included
    slack_mm: float            # how much of length_mm is service slack (loop / lay-in excess)
    min_radius_mm: float       # tightest centreline radius along pts
    bundle: str = ""           # Bundle id it runs in ("" = alone)
    straight_a_mm: float = 0.0 # straight run leaving terminal a along its axis
    straight_b_mm: float = 0.0
    ok: bool = True            # False: the router found no clear path (pts is then the best attempt)
    why: str = ""


@dataclass
class Bundle:
    """Conductors laid side by side along a shared spine (a lead's 3 phases, a +/- pair, or leads sharing a channel)."""

    id: str
    members: list              # conductor ids
    spine: np.ndarray          # (m, 3) samples of the shared centreline
    radius_mm: float           # circumscribed radius of the lay
    lay: str = "round"         # "round" (twisted / tied) | "flat" (ribbon in a channel)
    span: tuple = (0.0, 0.0)   # arc-length range of the spine the members share


@dataclass
class TiePoint:
    """Where a bundle is held to the chassis: a pair of slots for a cable tie, a printed clip or a channel lip."""

    id: str
    at: np.ndarray             # (3,) on the bundle centreline
    along: np.ndarray          # (3,) unit tangent of the run
    normal: np.ndarray         # (3,) unit, from the supporting wall into free space
    part: str                  # chassis part that carries it
    kind: str = "tie_slot"     # "tie_slot" | "clip" | "channel_lip"
    bundle: str = ""
    radius_mm: float = 0.0


@dataclass
class Channel:
    """A groove in a chassis part that a run lies in: derived from the route, cut from the part."""

    id: str
    part: str
    pts: np.ndarray            # (m, 3) centreline of the groove floor run (world)
    width_mm: float
    depth_mm: float
    normal: np.ndarray         # (3,) unit, out of the wall (the open side of the groove)
    members: list = field(default_factory=list)    # conductor ids lying in it


@dataclass
class PlacedConnector:
    """A connector housing in the world (device side or the mating wire side)."""

    id: str
    type: str                  # ConnectorType id
    at: np.ndarray             # (3,) origin (mating face centre)
    x_dir: np.ndarray          # (3,) unit, the wire exit direction
    y_dir: np.ndarray          # (3,) unit, the pin row
    device: str = ""
    refs: list = field(default_factory=list)       # terminal refs it carries


@dataclass
class Harness:
    """Everything the wiring of one robot is: the result of plan.build()."""

    netlist: Netlist
    terminals: dict = field(default_factory=dict)  # ref -> WorldTerminal
    paths: dict = field(default_factory=dict)      # conductor id -> WirePath
    bundles: list = field(default_factory=list)
    ties: list = field(default_factory=list)
    channels: list = field(default_factory=list)
    connectors: list = field(default_factory=list)
    settings: dict = field(default_factory=dict)
    mass_g: float = 0.0
    length_mm: float = 0.0

    def path(self, cid):
        return self.paths.get(cid)
