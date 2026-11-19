// Browser port of the repo's fight sim (robot/fight/*.py): same robot data (robot.fight.webexport), same models.
// arena.py: free chassis, wheel/weapon hinges, weapon on a sprung carrier (wobble.py: imbalance, mount + tilt springs),
//   breakable parts on welds that snap above their fastener-derived break force, debris that later hits its own robot.
// physics.py: DC motor curves (torque falls with speed), ESC current limit, ONE shared battery with internal resistance
//   (weapon spin-up sags the drive), state of charge, copper heating + thermal cut-out.
// materials.py: per-part friction + restitution; hazards.py: tyre cuts, switch knock-off, wire cuts, debris jams;
// brains.py: AI drivers with 150 ms reaction delay + steering noise. Gyroscopic effects come from MuJoCo's rigid-body
// dynamics with the real weapon inertia. Units m, kg, s.
export const ARENAS = {
  aws2025: { name: 'AWS 2025 (drop-off slot + pit)', half: 0.5, wall_h: 0.3, roof: true, gaps: { e: [[-0.2, 0.2]] }, pits: [[0, 0.32, 0.1, 0.1, 0]], spawn: 0.3 },
  aws_classic: { name: 'AWS classic (raised platform)', half: 0.381, wall_h: 0.3, roof: true, gaps: { s: [[-0.381, 0.381]], e: [[-0.381, 0.381]] }, pits: [], spawn: 0.2 },
  beetle_champs: { name: 'Beetle Champs (OOTA gap + pit opens at 30 s)', half: 0.6, wall_h: 0.3, roof: true, gaps: { n: [[-0.15, 0.15]] }, pits: [[0, -0.38, 0.125, 0.125, 30]], spawn: 0.3 },
  closed: { name: 'Closed box (no way out)', half: 0.6, wall_h: 0.4, roof: true, gaps: {}, pits: [], spawn: 0.3 },
};
export const DT = 1e-4;           // physics step (python uses 5e-5; 1e-4 keeps the browser real-time, contact tc stays 0.3 ms)
const SUB = 8;                    // steps per tick (0.8 ms)
const CONTROL_DT = 0.004;         // brain / driver input rate (run.py)
const PLANT_EVERY = 5;            // motor + battery update every 5 steps (run.py dtp = 5 * timestep)
const DROP_Z = -0.1, OUT_Z = -0.03, FLOOR_MU = 0.05, CONTACT_TC = 6e-4, ARMATURE = 2e-5;
const T_AMB = 25, ALPHA_CU = 0.0039, COUNT_S = 10;
const POWER_KINDS = ['battery', 'switch', 'esc', 'receiver', 'bec'];
const KIND_RGBA = { wheel: '0.08 0.08 0.09 1', tyre: '0.08 0.08 0.09 1', weapon: '0.78 0.8 0.85 1', fork: '0.75 0.77 0.82 1', battery: '0.2 0.4 0.9 1',
  esc: '0.1 0.45 0.2 1', receiver: '0.1 0.45 0.2 1', motor: '0.55 0.55 0.6 1', drive_motor: '0.55 0.55 0.6 1', weapon_motor: '0.55 0.55 0.6 1',
  servo: '0.2 0.2 0.25 1', switch: '0.85 0.1 0.1 1' };
const f6 = v => +v.toFixed(6), fv = a => a.map(f6).join(' '), fp = a => a.map(v => v.toPrecision(7)).join(' ');
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const norm = a => Math.hypot(...a), unit = a => { const n = norm(a) || 1; return a.map(v => v / n); };
const wrap = a => ((a + Math.PI) % (2 * Math.PI) + 2 * Math.PI) % (2 * Math.PI) - Math.PI;
const dampRatio = e => { e = Math.min(Math.max(e, 1e-3), 0.99); const l = Math.log(e); return -l / Math.sqrt(Math.PI ** 2 + l * l); };
function basis(axis) { const a = unit(axis); let u = cross(a, Math.abs(a[0]) < 0.9 ? [1, 0, 0] : [0, 1, 0]); u = unit(u); return [a, u, cross(a, u)]; }
function rng(seed) { let s = seed >>> 0 || 1; return () => { s ^= s << 13; s ^= s >>> 17; s ^= s << 5; return ((s >>> 0) / 4294967296); }; }
function gauss(r) { return Math.sqrt(-2 * Math.log(r() + 1e-12)) * Math.cos(2 * Math.PI * r()); }

// ---------------- electrical plant (physics.py 1:1) ----------------
class Battery {
  constructor(b) { this.cells = b.cells; this.mah = b.mah; this.r_int = b.r_int; this.soc = 1; this.i = 0; this.v = this.ocv(); }
  ocv() { return this.cells * (3.45 + 0.75 * Math.max(0, Math.min(1, this.soc))); }
  update(i, dt) { this.i = i; this.v = Math.max(0, this.ocv() - i * this.r_int); this.soc -= Math.max(0, i) * dt / (this.mah * 3.6); }
}
class Motor {
  constructor(m) { Object.assign(this, m); this.temp = T_AMB; this.i = 0; this.dead = false; }
  get r() { return this.r20 * (1 + ALPHA_CU * (this.temp - 20)); }
  torque(duty, vb, om) {
    if (this.dead) { this.i = 0; return 0; }
    const vm = Math.max(-1, Math.min(1, duty)) * vb;
    this.i = Math.max(-this.i_max, Math.min(this.i_max, (vm - this.ke * om) / this.r));
    return this.ke * this.i;
  }
  heat(dt) { const p = this.i * this.i * this.r; this.temp += (p - (this.temp - T_AMB) / this.r_th) * dt / this.c_th; if (this.temp > this.t_cut) this.dead = true; }
}

// ---------------- arena (arenas.py 1:1) ----------------
function arenaXml(A) {
  const h = A.half, t = 0.01, wh = A.wall_h, fl = `friction="${FLOOR_MU} 0.005 0.0001" solref="${CONTACT_TC} ${dampRatio(0.6).toFixed(4)}"`;
  let s = `<geom name="drop_floor" type="box" size="2 2 0.01" pos="0 0 ${DROP_Z - 0.01}" ${fl} rgba="0.1 0.1 0.12 1"/>`;
  const xs = [...new Set([-h, h, ...A.pits.flatMap(([cx, , hx]) => [cx - hx, cx + hx])])].sort((a, b) => a - b);
  const ys = [...new Set([-h, h, ...A.pits.flatMap(([, cy, , hy]) => [cy - hy, cy + hy])])].sort((a, b) => a - b);
  let k = 0;
  for (let i = 0; i < xs.length - 1; i++) for (let j = 0; j < ys.length - 1; j++) {
    const cx = (xs[i] + xs[i + 1]) / 2, cy = (ys[j] + ys[j + 1]) / 2;
    const pit = A.pits.findIndex(([px, py, hx, hy]) => Math.abs(cx - px) < hx && Math.abs(cy - py) < hy);
    if (pit >= 0 && A.pits[pit][4] <= 0) continue;
    s += `<geom name="${pit >= 0 ? 'cover' + pit + '_' : 'floor_t'}${k++}" type="box" size="${(xs[i + 1] - xs[i]) / 2} ${(ys[j + 1] - ys[j]) / 2} ${t}" pos="${cx} ${cy} ${-t}" ${fl} rgba="${pit >= 0 ? '0.55 0.45 0.1 1' : '0.3 0.32 0.35 1'}"/>`;
  }
  const E = { n: [0, 1], s: [0, -1], e: [1, 0], w: [-1, 0] };
  for (const e of ['n', 's', 'e', 'w']) {
    const spans = [...(A.gaps[e] || [])].sort((a, b) => a[0] - b[0]), cuts = []; let a = -h - 2 * t;
    for (const [a0, a1] of spans) { cuts.push([a, a0]); a = a1; }
    cuts.push([a, h + 2 * t]);
    cuts.forEach(([a0, a1], j) => {
      if (a1 - a0 < 1e-3) return;
      const m = (a0 + a1) / 2, L = (a1 - a0) / 2, [ex, ey] = E[e];
      const pos = ex ? [ex * (h + t), m] : [m, ey * (h + t)], size = ex ? [t, L] : [L, t];
      s += `<geom name="wall_${e}${j}" type="box" size="${size[0]} ${size[1]} ${wh / 2}" pos="${pos[0]} ${pos[1]} ${wh / 2}" solref="${CONTACT_TC} ${dampRatio(0.5).toFixed(4)}" rgba="0.7 0.8 0.9 0.25"/>`;
    });
  }
  if (A.roof) s += `<geom name="roof" type="box" size="${h + 2 * t} ${h + 2 * t} 0.005" pos="0 0 ${wh + 0.005}" rgba="0.6 0.7 0.8 0"/>`;
  return s;
}
function onPlatform(A, x, y, t) {
  if (Math.abs(x) > A.half || Math.abs(y) > A.half) return false;
  return !A.pits.some(([cx, cy, hx, hy, ot]) => t >= ot && Math.abs(x - cx) < hx && Math.abs(y - cy) < hy);
}
function hazardPoints(A, t) {
  const pts = A.pits.filter(p => t >= p[4]).map(([cx, cy]) => [cx, cy]), h = A.half + 0.06;
  for (const [e, spans] of Object.entries(A.gaps)) for (const [a0, a1] of spans) { const m = (a0 + a1) / 2; pts.push({ n: [m, h], s: [m, -h], e: [h, m], w: [-h, m] }[e]); }
  return pts;
}

// ---------------- robot MJCF (arena.py add_fighter) ----------------
function robotXml(P, doc, accent, place, yaw, info) {
  const [lo, hi] = doc.bounds, hd = Math.atan2(doc.forward[1], doc.forward[0]);
  const ang = yaw - hd, c = Math.cos(ang), s = Math.sin(ang);
  const ctr = [(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2];
  const t = [place[0] - (c * ctr[0] - s * ctr[1]), place[1] - (s * ctr[0] + c * ctr[1]), 0.0015 - lo[2]];
  const euler = `0 0 ${(ang * 180 / Math.PI).toFixed(5)}`;
  const tc = Math.max(CONTACT_TC, 2.5 * DT), lift = doc.lifter && doc.lifter.group;
  let assets = '', n = 0, acts = '', loose = '', eqs = '';
  const out = { wheels: [], weaponAct: null, weaponJoint: null, liftAct: null, hd, loose: [], groups: {} };
  const geomsOf = (g, gi, tag = '') => {
    let x = '';
    for (const p of g.parts) {
      const nm = `${P}m${n}`;
      assets += `<mesh name="${nm}" vertex="${p.verts.map(v => +v.toFixed(5)).join(' ')}"/>`;
      const col = KIND_RGBA[p.kind] || (['armor', 'wedge', 'plate', 'structure'].includes(p.kind) || !p.kind ? accent : '0.4 0.42 0.46 1');
      const ptc = g.kind === 'weapon' ? Math.max(tc, doc.blade_tc || 4e-4) : tc;
      const gname = `${P}g${gi}_${n}${tag}`;
      info[gname] = { r: P === 'a_' ? 0 : 1, group: g.name, gkind: g.kind, part: p.part, kind: p.kind, copy: tag === 'c', ghost: tag === 'x' };
      x += `<geom name="${gname}" type="mesh" mesh="${nm}" rgba="${col}" friction="${p.mu} 0.005 0.0001" solref="${ptc} ${dampRatio(p.e).toFixed(4)}" density="0"/>`;
      n++;
    }
    return x;
  };
  const inert = g => `<inertial pos="${fv(g.com)}" mass="${Math.max(g.mass, 1e-5)}" fullinertia="${fp(g.inertia.map((v, i) => i < 3 ? v + 1e-10 : v))}"/>`;
  let kids = '', chassis = '', lcopy = '';
  doc.groups.forEach((g, gi) => {
    out.groups[g.name] = g;
    if (g.kind === 'chassis') { chassis = inert(g) + geomsOf(g, gi); return; }
    if (g.kind === 'loose') {  // breakable part. Attached: rigid collision copy on the chassis (a gram-scale part on a soft weld
      // jitters and tips the robot). Its mass rides on a non-colliding welded twin that takes over the instant the part breaks.
      lcopy += geomsOf(g, gi, 'c');
      let I = g.inertia.slice(); const mI = g.mass * 0.002 ** 2 / 12 * 4; I[0] += mI; I[1] += mI; I[2] += mI;
      loose += `<body name="${P}${g.name}" pos="${fv(t)}" euler="${euler}"><freejoint name="${P}${g.name}_free"/>
        <inertial pos="${fv(g.com)}" mass="${Math.max(g.mass, 1e-5)}" fullinertia="${fp(I.map((v, i) => i < 3 ? v + 1e-10 : v))}"/>${geomsOf(g, gi, 'x')}</body>`;
      eqs += `<weld name="${P}${g.name}_weld" body1="${P}ch" body2="${P}${g.name}" solref="0.004 1"/>`;
      out.loose.push({ name: g.name, eq: `${P}${g.name}_weld`, body: `${P}${g.name}`, joint: `${P}${g.name}_free`, break_N: g.break_N || 150, mass: g.mass, broken: null, peak: 0, debris: false });
      return;
    }
    const jn = `${P}${g.name}_j`;
    if (g.kind === 'weapon') {  // wobble.py carrier: radial + tilt springs, real imbalance
      const [a, u, v] = basis(g.axis), wp = doc.wobble || {};
      const com = g.com.map((x, i) => x + u[i] * (wp.imbalance_mm ?? 0.05) * 1e-3);
      kids += `<body name="${P}carrier" pos="${fv(g.pivot)}"><inertial pos="0 0 0" mass="0.0001" diaginertia="1e-10 1e-10 1e-10"/>
        <joint name="${P}ru" type="slide" axis="${fv(u)}" stiffness="${wp.mount_k_Npm ?? 2e5}" damping="5" armature="0.001"/>
        <joint name="${P}rv" type="slide" axis="${fv(v)}" stiffness="${wp.mount_k_Npm ?? 2e5}" damping="5" armature="0.001"/>
        <joint name="${P}tu" type="hinge" axis="${fv(u)}" stiffness="${wp.tilt_k_Nm ?? 20}" damping="0.01" armature="2e-6"/>
        <joint name="${P}tv" type="hinge" axis="${fv(v)}" stiffness="${wp.tilt_k_Nm ?? 20}" damping="0.01" armature="2e-6"/>
        <body name="${P}${g.name}" pos="${fv(g.pivot.map(x => -x))}">${inert({ ...g, com })}
        <joint name="${jn}" type="hinge" pos="${fv(g.pivot)}" axis="${fv(g.axis)}" damping="1e-5" armature="${ARMATURE}"/>${geomsOf(g, gi)}</body></body>`;
      acts += `<motor name="${P}${g.name}_a" joint="${jn}" gear="1" forcelimited="true" forcerange="-10 10"/>`;
      out.weaponAct = `${P}${g.name}_a`; out.weaponJoint = jn; out.weaponGroup = g.name;
      out.weaponI = dot(g.axis, [0, 1, 2].map(i => g.inertia[i] * g.axis[i] + (i === 0 ? g.inertia[3] * g.axis[1] + g.inertia[4] * g.axis[2] : i === 1 ? g.inertia[3] * g.axis[0] + g.inertia[5] * g.axis[2] : g.inertia[4] * g.axis[0] + g.inertia[5] * g.axis[1])));
      return;
    }
    const lim = g.name === lift ? ` limited="true" range="${Math.min(doc.lifter.down_rad, doc.lifter.up_rad) - 0.05} ${Math.max(doc.lifter.down_rad, doc.lifter.up_rad) + 0.05}"` : '';
    kids += `<body name="${P}${g.name}">${inert(g)}<joint name="${jn}" type="hinge" pos="${fv(g.pivot)}" axis="${fv(g.axis)}" damping="1e-5" armature="${ARMATURE}"${lim}/>${geomsOf(g, gi)}</body>`;
    if (g.name === lift) { acts += `<position name="${P}${g.name}_a" joint="${jn}" kp="2" kv="0.02" forcelimited="true" forcerange="-${doc.lifter.torque_Nm} ${doc.lifter.torque_Nm}"/>`; out.liftAct = `${P}${g.name}_a`; out.liftJoint = jn; }
    else if (g.kind === 'wheel') {
      acts += `<motor name="${P}${g.name}_a" joint="${jn}" gear="1" forcelimited="true" forcerange="-10 10"/>`;
      const left = [-doc.forward[1], doc.forward[0], 0], rel = [g.pivot[0] - ctr[0], g.pivot[1] - ctr[1], 0];
      const roll = Math.sign(dot(cross(g.axis, [0, 0, 1]), [doc.forward[0], doc.forward[1], 0])) || 1;
      out.wheels.push({ name: g.name, act: `${P}${g.name}_a`, joint: jn, side: Math.sign(dot(left, rel)) || 1, roll });
    }
  });
  out.xml = `<body name="${P}ch" pos="${fv(t)}" euler="${euler}"><freejoint name="${P}free"/>${chassis}${lcopy}${kids}</body>${loose}`;
  Object.assign(out, { assets, acts, eqs });
  return out;
}

// ---------------- the sim ----------------
export class Sim {
  constructor(mj, docs, arena = 'aws2025', opts = {}) {
    this.mj = mj; this.docs = docs; this.arena = arena; this.A = ARENAS[arena];
    const accents = ['0.25 0.5 0.95 1', '0.9 0.3 0.25 1'];
    this.info = {};
    const sx = this.A.spawn;
    const R = this.R = ['a_', 'b_'].map((P, i) => robotXml(P, docs[i], accents[i], [i ? sx : -sx, i ? 0.05 : -0.05], i ? Math.PI : 0, this.info));
    const xml = `<mujoco><option timestep="${DT}" gravity="0 0 -9.81" cone="elliptic" impratio="2" integrator="implicitfast"/>
      <default><geom condim="4" solimp="0.95 0.99 0.001"/></default>
      <asset>${R[0].assets}${R[1].assets}</asset>
      <worldbody>${arenaXml(this.A)}${R[0].xml}${R[1].xml}</worldbody>
      <equality>${R[0].eqs}${R[1].eqs}</equality>
      <actuator>${R[0].acts}${R[1].acts}</actuator></mujoco>`;
    const m = this.model = mj.MjModel.from_xml_string(xml);
    this.data = new mj.MjData(m);
    this.gname = [...Array(m.ngeom).keys()].map(g => m.geom(g).name);
    this.ginfo = this.gname.map(n => this.info[n] || null);
    for (let g = 0; g < m.ngeom; g++) {  // own-robot geoms never collide (hazards.setup_collision_bits)
      const gi = this.ginfo[g];
      if (gi) { const b = gi.r ? 4 : 2; m.geom_contype[g] = gi.ghost ? 0 : b; m.geom_conaffinity[g] = gi.ghost ? 0 : 0xFFFF & ~b; } else { m.geom_contype[g] = 1; m.geom_conaffinity[g] = 0xFFFF; }
    }
    this.mu0 = Float64Array.from(m.geom_friction);
    this.act = {}; for (let i = 0; i < m.nu; i++) this.act[m.actuator(i).name] = i;
    this.dof = n => m.jnt_dofadr[m.jnt(n).id];
    this.chId = ['a_', 'b_'].map(p => m.body(p + 'ch').id);
    this.rob = R.map((r, i) => {
      const doc = docs[i], bat = new Battery(doc.battery || { cells: 2, mah: 180, r_int: 0.08 }), motors = {}, duty = {};
      for (const w of r.wheels) { motors[w.name] = new Motor(doc.motors[w.name]); duty[w.name] = 0; w.dof = this.dof(w.joint); }
      if (r.weaponJoint) { motors[r.weaponGroup] = new Motor(doc.motors[r.weaponGroup]); duty[r.weaponGroup] = 0; r.wdof = this.dof(r.weaponJoint); }
      for (const L of r.loose) { L.eqId = m.eq(L.eq).id; L.bodyId = m.body(L.body).id; L.qv = this.dof(L.joint); }
      return { bat, motors, duty, lifter: doc.lifter, dead: null, cut: new Set(), tyre: {}, stall: {}, out: false, flipT: 0, prevW: 0, dealt: 0, hits: 0,
        lift: doc.lifter ? doc.lifter.down_rad : 0, queue: [], peakTilt: 0 };
    });
    this.t = 0; this.k = 0; this.nextCtrl = 0; this.events = []; this.pitsOpen = false; this.firstOut = null;
    this.input = [{ l: 0, r: 0, w: 0 }, { l: 0, r: 0, w: 0 }];
    this.rand = rng(opts.seed || 12345);
    this.brains = [null, null];
    mj.mj_forward(m, this.data);
  }
  setInput(i, c) { this.input[i] = c; }
  setAI(i, on) { this.brains[i] = on ? makeBrain(this.docs[i], i) : null; }
  ev(type, r, text) { this.events.push({ t: +this.t.toFixed(2), type, r, text }); if (this.events.length > 60) this.events.shift(); }

  // --- controls: duty for each motor (spin_weapon: throttle so no-load speed on a full pack = declared rpm)
  _control() {
    for (let i = 0; i < 2; i++) {
      const rb = this.rob[i], r = this.R[i], doc = this.docs[i];
      let c = this.input[i];
      if (this.brains[i]) {  // AI: brain decides, command lands after the driver's reaction delay with steering noise
        const cmd = this.brains[i].act(this, i, this.t), hz = doc.hazards || {};
        const nz = (hz.steer_noise ?? 0.03) * gauss(this.rand);
        rb.queue.push([this.t, { l: cmd.l - nz, r: cmd.r + nz, w: cmd.w }]);
        while (rb.queue.length && this.t - rb.queue[0][0] >= (hz.reaction_s ?? 0.15)) rb.aiCmd = rb.queue.shift()[1];
        c = rb.aiCmd || { l: 0, r: 0, w: cmd.w };
      }
      if (rb.dead) { for (const k in rb.duty) rb.duty[k] = 0; continue; }
      for (const w of r.wheels) rb.duty[w.name] = Math.max(-1, Math.min(1, w.roll * (w.side > 0 ? c.l : c.r)));
      if (r.weaponJoint) { const mo = rb.motors[r.weaponGroup]; rb.duty[r.weaponGroup] = Math.max(-1, Math.min(1, Math.max(0, Math.min(1, +c.w || 0)) * doc.weapon.omega * mo.ke / rb.bat.ocv())); }  // throttle 0..1 of the declared rpm
      if (r.liftAct && rb.lifter) this.data.ctrl[this.act[r.liftAct]] = c.w ? doc.lifter.up_rad : doc.lifter.down_rad;
    }
  }
  _plant(dt) {  // physics.py step_plant: torque from throttle, battery voltage and speed; battery sag + heat
    const d = this.data, qv = d.qvel, ctrl = d.ctrl;
    for (let i = 0; i < 2; i++) {
      const rb = this.rob[i], r = this.R[i]; let itot = 0;
      for (const w of r.wheels) { const mo = rb.motors[w.name]; ctrl[this.act[w.act]] = mo.torque(rb.duty[w.name], rb.bat.v, qv[w.dof]); itot += Math.abs(rb.duty[w.name] * mo.i); mo.heat(dt); }
      if (r.weaponJoint) { const mo = rb.motors[r.weaponGroup]; ctrl[this.act[r.weaponAct]] = mo.torque(rb.duty[r.weaponGroup], rb.bat.v, qv[r.wdof]); itot += Math.abs(rb.duty[r.weaponGroup] * mo.i); mo.heat(dt); }
      rb.bat.update(itot, dt);
    }
  }
  step(n = 1) {
    const mj = this.mj, m = this.model, d = this.data;
    for (let k = 0; k < n * SUB; k++) {
      if (this.t >= this.nextCtrl) { this.nextCtrl += CONTROL_DT; this._control(); this._perControl(); }
      if (this.k % PLANT_EVERY === 0) this._plant(PLANT_EVERY * DT);
      mj.mj_step(m, d); this.k++; this.t += DT;
      this._contacts(); this._welds();
    }
  }
  _perControl() {
    const d = this.data;
    for (let i = 0; i < 2; i++) {
      const rb = this.rob[i], r = this.R[i];
      if (r.weaponJoint) {  // run.py: a weapon hit = sudden drop in spinner speed; energy dealt = 1/2 I (w0^2 - w1^2)
        const w = d.qvel[r.wdof];
        if (Math.abs(rb.prevW) - Math.abs(w) > 60) { const e = 0.5 * r.weaponI * (rb.prevW ** 2 - w ** 2); if (e > 0.05) { rb.dealt += e; rb.hits++; this.ev('hit', i, `${this.docs[i].name} weapon hit ${e.toFixed(1)} J`); } }
        rb.prevW = w;
      }
      if (!rb.out && this.pos(i)[2] < OUT_Z) { rb.out = true; if (this.firstOut === null) this.firstOut = i; this.ev('out', i, `${this.docs[i].name} is OUT of the arena`); }
      const inv = this.upZ(i) < -0.3 && !this.docs[i].can_run_inverted && !rb.lifter;
      rb.flipT = inv ? rb.flipT + CONTROL_DT : 0;
      rb.peakTilt = Math.max(rb.peakTilt, Math.acos(Math.max(-1, Math.min(1, this.upZ(i)))) * 57.3);
      // debris: once a broken part has left its robot's envelope it collides with its own robot too
      for (const L of r.loose) if (L.broken !== null && !L.debris) {
        const rel = this.local(i, [d.xipos[L.bodyId * 3], d.xipos[L.bodyId * 3 + 1], d.xipos[L.bodyId * 3 + 2]]), [lo, hi] = this.docs[i].bounds;
        if (rel.every((v, k) => v > lo[k] - 0.002 && v < hi[k] + 0.002)) continue;
        L.debris = true; const m = this.model;
        this.gname.forEach((nm, g) => { const gi = this.ginfo[g]; if (gi && gi.r === i && gi.group === L.name && gi.ghost) { m.geom_contype[g] = 1 << 15; m.geom_conaffinity[g] = 0xFFFF; } });
      }
      // jams: commanded but stalled while debris touches it
      for (const [name, mo] of Object.entries(rb.motors)) {
        const w = r.wheels.find(x => x.name === name), dof = w ? w.dof : r.wdof, om = Math.abs(d.qvel[dof]), w0 = 8.4 / mo.ke;
        const stalled = Math.abs(rb.duty[name]) > 0.3 && om < 0.05 * w0 && this._debrisTouch?.has(`${i}/${name}`);
        rb.stall[name] = stalled ? (rb.stall[name] || 0) + CONTROL_DT : 0;
        if (stalled && Math.abs(rb.stall[name] - (this.docs[i].hazards?.jam_s ?? 0.3)) < CONTROL_DT / 2) this.ev('jam', i, `${this.docs[i].name} ${name} jammed by debris`);
      }
    }
    this._debrisTouch = new Set();
    for (const p of this.A.pits) if (p[4] > 0 && this.t >= p[4] && !this.pitsOpen) { this.pitsOpen = true; this._openPits(); this.ev('pit', -1, 'Pit is now OPEN'); }
  }
  _openPits() { const m = this.model; this.gname.forEach((n, g) => { if (n.startsWith('cover')) { m.geom_contype[g] = 0; m.geom_conaffinity[g] = 0; m.geom_rgba[g * 4 + 3] = 0; } }); }
  _welds() {  // arena.py step_damage: weld force above the part's break force -> the part comes off
    const d = this.data;
    for (let r = 0; r < 2; r++) for (const L of this.R[r].loose) {
      if (L.broken !== null) continue;
      const fn = this._load?.get(`${r}/${L.name}`) || 0; L.peak = Math.max(L.peak, fn);
      if (fn > L.break_N) { this._detach(r, L); this.ev('break', r, `${this.docs[r].name} lost ${L.name} (${fn.toFixed(0)} N > ${L.break_N.toFixed(0)} N)`); }
    }
    for (let r = 0; r < 2; r++) for (const L of this.R[r].loose) if (L.broken !== null) {  // cap debris at speeds no real chunk reaches
      const q = d.qvel, a = L.qv, sv = Math.hypot(q[a], q[a + 1], q[a + 2]), so = Math.hypot(q[a + 3], q[a + 4], q[a + 5]);
      if (sv > 100) for (let k = 0; k < 3; k++) q[a + k] *= 100 / sv;
      if (so > 5000) for (let k = 3; k < 6; k++) q[a + k] *= 5000 / so;
    }
  }
  _detach(r, L) {  // fasteners let go: hide the rigid copy, the welded twin (same pose + velocity) becomes the free part
    const m = this.model, b = r ? 4 : 2; this.data.eq_active[L.eqId] = 0; L.broken = this.t;
    this.ginfo.forEach((gi, g) => { if (!gi || gi.r !== r || gi.group !== L.name) return;
      if (gi.copy) { m.geom_contype[g] = 0; m.geom_conaffinity[g] = 0; } else if (gi.ghost) { m.geom_contype[g] = b; m.geom_conaffinity[g] = 0xFFFF & ~b; } });
  }
  visible(g) { const gi = this.ginfo[g]; if (!gi || !(gi.copy || gi.ghost)) return true; const br = this.R[gi.r].loose.find(L => L.name === gi.group)?.broken != null; return gi.copy ? !br : br; }
  _contacts() {  // hazards.py tick: tyre cuts, switch knock-off, wire cuts, debris touch
    const d = this.data, nc = d.ncon;
    if (!nc) return;
    const cs = d.contact, fr = d.efc_force; this._load = new Map();
    for (let i = 0; i < nc; i++) {
      const c = cs.get(i);
      const g1 = c.geom1, g2 = c.geom2, ea = c.efc_address, pos = c.pos ? [c.pos[0], c.pos[1], c.pos[2]] : null;
      c.delete?.();
      const oa = this.ginfo[g1], ob = this.ginfo[g2];
      if (!oa && !ob) continue;
      const fn = ea >= 0 ? Math.abs(fr[ea]) : 0;
      for (const [me, other] of [[oa, ob], [ob, oa]]) {
        if (!me) continue;
        const r = me.r, rb = this.rob[r];
        if (me.copy) { const k = `${r}/${me.group}`; this._load.set(k, (this._load.get(k) || 0) + fn); }
        const otherDebris = other && this.R[other.r].loose.some(L => L.name === other.group && L.debris);
        if (otherDebris) this._debrisTouch?.add(`${r}/${me.group}`);
        if (!other || other.r === r || otherDebris) continue;
        const hz = this.docs[r].hazards || {}, weaponHit = other.gkind === 'weapon' || other.kind === 'weapon';
        if ((me.kind === 'wheel' || me.kind === 'tyre') && weaponHit && fn > (hz.tyre_cut_N ?? 250)) {
          rb.tyre[me.group] = (rb.tyre[me.group] || 0) + fn / 1000; this._setGrip(r, me.group);
          this.ev('tyre', r, `${this.docs[r].name} ${me.group} tyre cut (${Math.round(Math.min(1, rb.tyre[me.group]) * 100)}%)`);
        }
        if (!pos) continue;
        const lp = this.local(r, pos);
        if (!rb.dead && fn > (hz.switch_N ?? 60)) for (const [sw, sc] of Object.entries(this.docs[r].switches || {}))
          if (norm(lp.map((v, k) => v - sc[k])) < (hz.switch_mm ?? 8) * 1e-3 + 0.006) this._kill(r, `switch ${sw} knocked off (${fn.toFixed(0)} N)`);
        if (fn > (hz.wire_N ?? 200)) for (const w of this.docs[r].wires || []) {
          if (rb.cut.has(w.id) || segDist(lp, w.pts) >= (hz.wire_mm ?? 6) * 1e-3) continue;
          rb.cut.add(w.id); const eff = wireEffect(this.docs[r], w); this.ev('wire', r, `${this.docs[r].name} wire ${w.id} cut → ${eff || 'nothing'}`); this._applyWire(r, eff);
        }
      }
    }
    cs.delete?.();
  }
  _setGrip(r, wheel) {
    const dmg = this.rob[r].tyre[wheel], hz = this.docs[r].hazards || {}, m = this.model;
    const sc = dmg >= (hz.tyre_destroy ?? 1) ? 0.2 : Math.max(0.3, 1 - 0.7 * dmg);
    this.ginfo.forEach((gi, g) => { if (gi && gi.r === r && gi.group === wheel) m.geom_friction[g * 3] = this.mu0[g * 3] * sc; });
  }
  _kill(r, why) { if (this.rob[r].dead) return; this.rob[r].dead = why; this.ev('dead', r, `${this.docs[r].name} DEAD: ${why}`); }
  _applyWire(r, eff) {
    const rb = this.rob[r], R = this.R[r];
    if (eff === 'all') this._kill(r, 'power wire cut');
    else if (eff === 'weapon' && R.weaponGroup) rb.motors[R.weaponGroup].dead = true;
    else if (eff && eff.startsWith('side:')) { const s = eff.slice(-1); for (const w of R.wheels) if ((this.docs[r].groups.find(g => g.name === w.name).com[0] < 0) === (s === 'l')) rb.motors[w.name].dead = true; }
    else if (eff === 'lifter') rb.lifter = null;
  }
  // --- state readers
  pos(i) { const p = this.data.xipos, b = this.chId[i] * 3; return [p[b], p[b + 1], p[b + 2]]; }
  quat(i) { const q = this.data.xquat, b = this.chId[i] * 4; return [q[b], q[b + 1], q[b + 2], q[b + 3]]; }
  yaw(i) { const [w, x, y, z] = this.quat(i); return Math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z)) + this.R[i].hd; }
  upZ(i) { const [, x, y] = this.quat(i); return 1 - 2 * (x * x + y * y); }
  vel(i) { const a = this.dof(['a_', 'b_'][i] + 'free'); return [this.data.qvel[a], this.data.qvel[a + 1]]; }
  yawRate(i) { const a = this.dof(['a_', 'b_'][i] + 'free'); return this.data.qvel[a + 5]; }
  local(i, p) {  // world point -> robot frame
    const b = this.chId[i], xm = this.data.xmat, o = [this.data.xpos[b * 3], this.data.xpos[b * 3 + 1], this.data.xpos[b * 3 + 2]], dd = p.map((v, k) => v - o[k]);
    return [0, 1, 2].map(c => xm[b * 9 + c] * dd[0] + xm[b * 9 + 3 + c] * dd[1] + xm[b * 9 + 6 + c] * dd[2]);
  }
  touching() { const d = this.data, cs = d.contact; let t = false; for (let i = 0; i < d.ncon && !t; i++) { const c = cs.get(i); const a = this.ginfo[c.geom1], b = this.ginfo[c.geom2]; c.delete?.(); if (a && b && a.r !== b.r) t = true; } cs.delete?.(); return t; }
  telemetry() {
    return this.rob.map((rb, i) => {
      const r = this.R[i], tot = r.loose.reduce((s, L) => s + L.mass, 0), lost = r.loose.filter(L => L.broken !== null);
      const drive = r.wheels.map(w => rb.motors[w.name]);
      return { name: this.docs[i].name, v: +rb.bat.v.toFixed(2), soc: +(rb.bat.soc * 100).toFixed(1), amps: +rb.bat.i.toFixed(1),
        rpm: r.weaponJoint ? Math.round(Math.abs(this.data.qvel[r.wdof]) * 60 / 2 / Math.PI) : null, rpmMax: this.docs[i].weapon ? Math.round(this.docs[i].weapon.omega * 60 / 2 / Math.PI) : null,
        wT: r.weaponJoint ? +rb.motors[r.weaponGroup].temp.toFixed(0) : null, wDead: r.weaponJoint ? rb.motors[r.weaponGroup].dead : false,
        dT: Math.max(...drive.map(m => m.temp)).toFixed(0) * 1, dDead: drive.filter(m => m.dead).length, wheels: drive.length,
        armour: tot ? Math.round(100 * (1 - lost.reduce((s, L) => s + L.mass, 0) / tot)) : 100, lost: lost.map(L => L.name),
        tyre: Math.round(100 * Math.max(0, ...Object.values(rb.tyre).map(v => Math.min(1, v)))), cut: [...rb.cut], dead: rb.dead,
        dealt: +rb.dealt.toFixed(1), hits: rb.hits, flip: +rb.flipT.toFixed(1), out: rb.out, lifter: !!this.docs[i].lifter, lifterOk: !!rb.lifter };
    });
  }
  // run.py outcome + judge (first out loses, dead loses, stuck upside down 10 s = KO, else parts lost*10 + energy dealt)
  result(limit = 180) {
    const T = this.telemetry();
    if (this.firstOut !== null) return { winner: 1 - this.firstOut, why: `${T[this.firstOut].name} out of the arena` };
    const dead = [0, 1].map(i => !!this.rob[i].dead);
    if (dead[0] !== dead[1]) return { winner: dead[0] ? 1 : 0, why: `${T[dead[0] ? 0 : 1].name}: ${this.rob[dead[0] ? 0 : 1].dead}` };
    const ko = [0, 1].map(i => this.rob[i].flipT > COUNT_S);
    if (ko[0] !== ko[1]) return { winner: ko[0] ? 1 : 0, why: `${T[ko[0] ? 0 : 1].name} counted out (stuck upside down)` };
    if (this.t >= limit || (dead[0] && dead[1])) {
      const s = [0, 1].map(i => T[1 - i].lost.length * 10 + T[i].dealt);
      return { winner: Math.abs(s[0] - s[1]) < 0.5 ? -1 : s[0] > s[1] ? 0 : 1, why: `judges (${s[0].toFixed(1)} : ${s[1].toFixed(1)})` };
    }
    return null;
  }
  snapshot() {
    const o = [], d = this.data;
    for (let i = 0; i < this.model.nbody; i++) o.push(d.xpos[i * 3], d.xpos[i * 3 + 1], d.xpos[i * 3 + 2], d.xquat[i * 4], d.xquat[i * 4 + 1], d.xquat[i * 4 + 2], d.xquat[i * 4 + 3]);
    return { st: this.t, br: this.R.map(r => r.loose.map(L => L.broken != null ? 1 : 0)), p: o.map(v => +v.toFixed(5)), g: this.pitsOpen, tel: this.telemetry(), ev: this.events.slice(-8) };
  }
}
function segDist(p, pts) {
  let best = 1e9;
  for (let k = 0; k < pts.length - 1; k++) {
    const a = pts[k], b = pts[k + 1], ab = b.map((v, i) => v - a[i]), L = dot(ab, ab);
    const s = L < 1e-12 ? 0 : Math.max(0, Math.min(1, dot(p.map((v, i) => v - a[i]), ab) / L));
    best = Math.min(best, norm(p.map((v, i) => v - (a[i] + s * ab[i]))));
  }
  return best;
}
function wireEffect(doc, w) {
  const k = w.kinds, e = w.ends;
  if (k.some(x => POWER_KINDS.includes(x)) && !k.some(x => ['motor', 'weapon_motor', 'servo'].includes(x))) return 'all';
  if (k.includes('weapon_motor') || e.some(x => x.includes('weapon') || (x.startsWith('w') && x.includes('esc')))) return 'weapon';
  for (let i = 0; i < 2; i++) { if (k[i] === 'motor') return 'side:' + (doc.part_coms[e[i]][0] < 0 ? 'l' : 'r'); if (k[i] === 'servo') return 'lifter'; }
  return null;
}

// ---------------- AI drivers (brains.py) ----------------
function makeBrain(doc, me) { return new Brain(doc.strategy, me); }
class Brain {
  constructor(strategy, me) { this.kind = strategy; this.me = me; this.opp = 1 - me; this.state = 'approach'; this.tSafe = 0; this.fireT = null; this.patience = 4; }
  frame(sim, i) { const p = sim.pos(i); return [[p[0], p[1]], sim.yaw(i)]; }
  bearingInOpp(sim) { const [mp] = this.frame(sim, this.me), [op, oh] = this.frame(sim, this.opp); const d = [mp[0] - op[0], mp[1] - op[1]]; return [wrap(Math.atan2(d[1], d[0]) - oh), Math.hypot(...d)]; }
  danger(sim, b, dist) { return (sim.docs[this.opp].danger || []).some(([c, h, r]) => Math.abs(wrap(b - c)) < h && dist < r + 0.06); }
  safeBearing(sim) {
    const arcs = sim.docs[this.opp].danger || []; let best = Math.PI, score = -1;
    for (let k = 0; k < 36; k++) { const b = wrap(k * Math.PI / 18); const s = arcs.length ? Math.min(...arcs.map(([c, h]) => Math.abs(wrap(b - c)) - h)) : Math.PI; if (s > score) { best = b; score = s; } }
    return best;
  }
  steer(sim, tgt, speed = 1, reverseOk = false) {
    let [mp, mh] = this.frame(sim, this.me); const T = sim.docs[this.me].hazards?.reaction_s ?? 0.15;
    mh += sim.yawRate(this.me) * T; const v = sim.vel(this.me); mp = [mp[0] + v[0] * T, mp[1] + v[1] * T];
    const [op] = this.frame(sim, this.opp);
    if (Math.abs(tgt[0] - op[0]) < 1e-9 && Math.abs(tgt[1] - op[1]) < 1e-9) { const ov = sim.vel(this.opp); tgt = [tgt[0] + ov[0] * T, tgt[1] + ov[1] * T]; }
    let err = wrap(Math.atan2(tgt[1] - mp[1], tgt[0] - mp[0]) - mh);
    if (reverseOk && Math.abs(err) > 2.2) { err = wrap(err + Math.PI); speed = -speed; }
    const turn = Math.max(-1, Math.min(1, 2 * err)), fwd = speed * Math.max(0, Math.cos(err)) ** 2;
    return [fwd - turn, fwd + turn];
  }
  orbitPoint(sim, b, dist, safe) {
    const [op, oh] = this.frame(sim, this.opp), dz = sim.docs[this.opp].danger || [];
    const r = dz.length ? Math.max(0.14, dz[0][2] + 0.08) : 0.14, d = wrap(safe - b), step = Math.sign(d) * Math.min(Math.abs(d), 0.9), a = oh + b + step;
    return [op[0] + r * Math.cos(a), op[1] + r * Math.sin(a)];
  }
  edgeGuard(sim, t, [l, r]) {
    const [mp, mh] = this.frame(sim, this.me), [lo, hi] = sim.docs[this.me].bounds, reach = 0.5 * Math.max(hi[0] - lo[0], hi[1] - lo[1]) + 0.015;
    const s = l + r >= 0 ? 1 : -1, ahead = [mp[0] + s * reach * Math.cos(mh), mp[1] + s * reach * Math.sin(mh)];
    return onPlatform(sim.A, ahead[0], ahead[1], t) ? [l, r] : [-s * 0.6, -s * 0.6];
  }
  base(sim, t) {
    const [b, dist] = this.bearingInOpp(sim), safe = this.safeBearing(sim), [op] = this.frame(sim, this.opp), off = Math.abs(wrap(b - safe));
    if (this.state === 'approach') { this.tSafe += CONTROL_DT; if (off < 0.6 || this.tSafe > this.patience || (!this.danger(sim, b, dist) && dist < 0.12)) this.state = 'attack'; }
    else if (dist > 0.3 && !sim.touching()) { this.state = 'approach'; this.tSafe = 0; }
    const lr = this.state === 'approach' && dist < 0.5 ? this.steer(sim, this.orbitPoint(sim, b, dist, safe)) : this.steer(sim, op);
    return this.edgeGuard(sim, t, lr);
  }
  act(sim, me, t) {
    const doc = sim.docs[me];
    if (this.kind === 'pusher') return this.pusher(sim, t);
    let [l, r] = this.base(sim, t), w = 0;
    if (this.kind === 'spinner') {
      w = 1;
      if (t < 0.6) [l, r] = [0, 0];
      if (this.state === 'attack' && sim.R[me].weaponJoint) {
        const om = Math.abs(sim.data.qvel[sim.R[me].wdof]);
        if (om < 0.25 * Math.abs(doc.weapon.omega) && !sim.touching()) { const [a, b2] = this.steer(sim, this.frame(sim, this.opp)[0]); [l, r] = [-0.6 * a, -0.6 * b2]; }
      }
    } else if (this.kind === 'lifter' && sim.rob[me].lifter) {
      if (sim.upZ(me) < -0.3) w = 1;
      else if (this.fireT !== null && t - this.fireT < 0.35) w = 1;
      else if (this.overPlate(sim) && (this.fireT === null || t - this.fireT > 0.8)) { this.fireT = t; w = 1; }
    }
    return { l, r, w };
  }
  overPlate(sim) {
    const op = sim.pos(this.opp), [mp, mh] = this.frame(sim, this.me), rel = [op[0] - mp[0], op[1] - mp[1]], f = [Math.cos(mh), Math.sin(mh)];
    const along = rel[0] * f[0] + rel[1] * f[1], side = Math.abs(rel[0] * -f[1] + rel[1] * f[0]);
    return sim.touching() && along > 0.02 && along < 0.11 && side < 0.04;
  }
  pusher(sim, t) {
    const pts = hazardPoints(sim.A, t);
    if (!pts.length) { const [l, r] = this.base(sim, t); return { l, r, w: 0 }; }
    const [op] = this.frame(sim, this.opp), [mp] = this.frame(sim, this.me);
    const hz = pts.reduce((a, p) => Math.hypot(p[0] - op[0], p[1] - op[1]) < Math.hypot(a[0] - op[0], a[1] - op[1]) ? p : a);
    const u = unit([hz[0] - op[0], hz[1] - op[1], 0]), to = [op[0] - mp[0], op[1] - mp[1]], dist = Math.hypot(...to), cosang = (to[0] * u[0] + to[1] * u[1]) / (dist || 1);
    const [b] = this.bearingInOpp(sim); let lr;
    if ((sim.touching() && cosang > 0.5) || cosang > 0.85) lr = this.steer(sim, op);
    else {
      let back = [op[0] - 0.16 * u[0], op[1] - 0.16 * u[1]]; const side = [-u[1], u[0]];
      if ((mp[0] - op[0]) * u[0] + (mp[1] - op[1]) * u[1] > -0.05) { const sg = (mp[0] - op[0]) * side[0] + (mp[1] - op[1]) * side[1] >= 0 ? 1 : -1; back = [op[0] + 0.18 * side[0] * sg - 0.05 * u[0], op[1] + 0.18 * side[1] * sg - 0.05 * u[1]]; }
      if (this.danger(sim, b, dist) && dist < 0.2) back = [mp[0] + 0.1 * (mp[0] - op[0]) / (dist || 1) + 0.1 * side[0], mp[1] + 0.1 * (mp[1] - op[1]) / (dist || 1) + 0.1 * side[1]];
      lr = this.steer(sim, back, 1, true);
    }
    const [l, r] = this.edgeGuard(sim, t, lr); return { l, r, w: 0 };
  }
}
