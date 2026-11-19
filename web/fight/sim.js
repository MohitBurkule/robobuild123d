// Physics for the fight game: builds MJCF from exported robot JSON (robot.fight.webexport: real CAD hulls, mass, inertia,
// motors) and the arena presets of robot/fight/arenas.py. Runs in browser and node. Units m, kg, s.
export const ARENAS = {
  aws2025: { name: 'AWS 2025 (drop-off slot + pit)', half: 0.5, wall_h: 0.3, roof: true, gaps: { e: [[-0.2, 0.2]] }, pits: [[0, 0.32, 0.1, 0.1, 0]], spawn: 0.3 },
  aws_classic: { name: 'AWS classic (raised platform)', half: 0.381, wall_h: 0.3, roof: true, gaps: { s: [[-0.381, 0.381]], e: [[-0.381, 0.381]] }, pits: [], spawn: 0.2 },
  beetle_champs: { name: 'Beetle Champs (OOTA gap + pit opens at 30 s)', half: 0.6, wall_h: 0.3, roof: true, gaps: { n: [[-0.15, 0.15]] }, pits: [[0, -0.38, 0.125, 0.125, 30]], spawn: 0.3 },
  closed: { name: 'Closed box (no way out)', half: 0.6, wall_h: 0.4, roof: true, gaps: {}, pits: [], spawn: 0.3, closed: true },
};
const DROP_Z = -0.1, OUT_Z = -0.03;
const DT = 1e-4, SUB = 8;  // 0.8 ms per tick
const KIND_RGBA = { wheel: '0.08 0.08 0.09 1', weapon: '0.78 0.8 0.85 1', fork: '0.78 0.8 0.85 1', armor: null, wedge: null, plate: null,
  battery: '0.2 0.4 0.9 1', esc: '0.1 0.45 0.2 1', receiver: '0.1 0.45 0.2 1', motor: '0.55 0.55 0.6 1', drive_motor: '0.55 0.55 0.6 1',
  weapon_motor: '0.55 0.55 0.6 1', servo: '0.2 0.2 0.25 1', switch: '0.8 0.1 0.1 1', structure: null };
const f = a => a.map(v => +v.toFixed(6)).join(' ');
const fp = a => a.map(v => v.toPrecision(7)).join(' ');
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];

function arenaXml(A) {
  const h = A.half, t = 0.01, wh = A.wall_h;
  let s = `<geom name="drop_floor" type="box" size="2 2 0.01" pos="0 0 ${DROP_Z - 0.01}" rgba="0.1 0.1 0.12 1"/>`;
  const xs = [...new Set([-h, h, ...A.pits.flatMap(([cx, , hx]) => [cx - hx, cx + hx])])].sort((a, b) => a - b);
  const ys = [...new Set([-h, h, ...A.pits.flatMap(([, cy, , hy]) => [cy - hy, cy + hy])])].sort((a, b) => a - b);
  let k = 0;
  for (let i = 0; i < xs.length - 1; i++) for (let j = 0; j < ys.length - 1; j++) {
    const cx = (xs[i] + xs[i + 1]) / 2, cy = (ys[j] + ys[j + 1]) / 2;
    const pit = A.pits.findIndex(([px, py, hx, hy]) => Math.abs(cx - px) < hx && Math.abs(cy - py) < hy);
    if (pit >= 0 && A.pits[pit][4] <= 0) continue;
    s += `<geom name="${pit >= 0 ? 'cover' + pit + '_' : 'floor_t'}${k++}" type="box" size="${(xs[i + 1] - xs[i]) / 2} ${(ys[j + 1] - ys[j]) / 2} ${t}" pos="${cx} ${cy} ${-t}" friction="0.6 0.005 0.0001" rgba="${pit >= 0 ? '0.55 0.45 0.1 1' : '0.3 0.32 0.35 1'}"/>`;
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
      s += `<geom name="wall_${e}${j}" type="box" size="${size[0]} ${size[1]} ${wh / 2}" pos="${pos[0]} ${pos[1]} ${wh / 2}" rgba="0.7 0.8 0.9 0.25"/>`;
    });
  }
  if (A.roof) s += `<geom name="roof" type="box" size="${h + 2 * t} ${h + 2 * t} 0.005" pos="0 0 ${wh + 0.005}" rgba="0.6 0.7 0.8 0"/>`;
  return s;
}

function robotXml(P, doc, accent, place, yaw) {
  const [lo, hi] = doc.bounds, hd = Math.atan2(doc.forward[1], doc.forward[0]);
  const ang = yaw - hd, c = Math.cos(ang), s = Math.sin(ang);
  const ctr = [(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2];
  const t = [place[0] - (c * ctr[0] - s * ctr[1]), place[1] - (s * ctr[0] + c * ctr[1]), 0.0015 - lo[2]];
  const wheelsInfo = [];
  const lift = doc.lifter && doc.lifter.group;
  // chassis = chassis group + loose groups (merged: no breakable welds in the browser game)
  const chassisG = doc.groups.filter(g => g.kind === 'chassis' || g.kind === 'loose');
  const moving = doc.groups.filter(g => !(g.kind === 'chassis' || g.kind === 'loose'));
  let mass = 0, com = [0, 0, 0];
  for (const g of chassisG) { mass += g.mass; for (let i = 0; i < 3; i++) com[i] += g.mass * g.com[i]; }
  com = com.map(v => v / mass);
  const I = [0, 0, 0, 0, 0, 0];  // xx yy zz xy xz yz
  for (const g of chassisG) {
    const d = g.com.map((v, i) => v - com[i]), d2 = dot(d, d);
    I[0] += g.inertia[0] + g.mass * (d2 - d[0] * d[0]); I[1] += g.inertia[1] + g.mass * (d2 - d[1] * d[1]); I[2] += g.inertia[2] + g.mass * (d2 - d[2] * d[2]);
    I[3] += g.inertia[3] - g.mass * d[0] * d[1]; I[4] += g.inertia[4] - g.mass * d[0] * d[2]; I[5] += g.inertia[5] - g.mass * d[1] * d[2];
  }
  let assets = '', geoms = '', n = 0;
  const addParts = (g, pre) => {
    let out = '';
    for (const p of g.parts) {
      const nm = `${P}m${n}`;
      assets += `<mesh name="${nm}" vertex="${p.verts.map(v => +v.toFixed(5)).join(' ')}"/>`;
      const col = KIND_RGBA[p.kind] === undefined ? '0.4 0.42 0.46 1' : KIND_RGBA[p.kind] || accent;
      const fr = g.kind === 'wheel' ? '1.3 0.01 0.001' : '0.5 0.005 0.0001';
      out += `<geom name="${P}${pre}_${n}" type="mesh" mesh="${nm}" rgba="${col}" friction="${fr}" density="1000"/>`;
      n++;
    }
    return out;
  };
  for (const g of chassisG) geoms += addParts(g, 'c');
  let kids = '', acts = '';
  for (const g of moving) {
    const tag = g.kind === 'weapon' ? 'w' : g.kind === 'wheel' ? 'h' : 'x';
    const jn = `${P}${g.name}_j`;
    const lim = g.name === lift ? ` limited="true" range="${Math.min(doc.lifter.down_rad, doc.lifter.up_rad) - 0.05} ${Math.max(doc.lifter.down_rad, doc.lifter.up_rad) + 0.05}"` : '';
    kids += `<body name="${P}${g.name}"><inertial pos="${f(g.com)}" mass="${Math.max(g.mass, 1e-5)}" fullinertia="${fp(g.inertia.map((v, i) => i < 3 ? v + 1e-10 : v))}"/>
      <joint name="${jn}" type="hinge" pos="${f(g.pivot)}" axis="${f(g.axis)}" damping="1e-5" armature="2e-7"${lim}/>${addParts(g, tag + g.name)}</body>`;
    if (g.name === lift) acts += `<position name="${P}${g.name}_a" joint="${jn}" kp="2" kv="0.02" forcerange="-${doc.lifter.torque_Nm} ${doc.lifter.torque_Nm}"/>`;
    else if (g.kind === 'weapon') acts += `<velocity name="${P}${g.name}_a" joint="${jn}" kv="0.004" forcerange="-${doc.weapon.torque_Nm} ${doc.weapon.torque_Nm}"/>`;
    else if (g.kind === 'wheel') {
      acts += `<velocity name="${P}${g.name}_a" joint="${jn}" kv="0.01" forcerange="-${doc.drive.torque_Nm} ${doc.drive.torque_Nm}"/>`;
      const left = [-doc.forward[1], doc.forward[0], 0], rel = [g.pivot[0] - ctr[0], g.pivot[1] - ctr[1], 0];
      const roll = Math.sign(dot(cross(g.axis, [0, 0, 1]), [doc.forward[0], doc.forward[1], 0])) || 1;
      wheelsInfo.push({ act: `${P}${g.name}_a`, side: Math.sign(dot(left, rel)) || 1, roll });
    }
  }
  const xml = `<body name="${P}ch" pos="${f(t)}" euler="0 0 ${(ang * 180 / Math.PI).toFixed(4)}"><freejoint name="${P}free"/>
    <inertial pos="${f(com)}" mass="${mass}" fullinertia="${fp(I.map((v, i) => i < 3 ? v + 1e-10 : v))}"/>${geoms}${kids}</body>`;
  return { xml, assets, acts, wheelsInfo, weaponAct: moving.find(g => g.kind === 'weapon') ? `${P}${moving.find(g => g.kind === 'weapon').name}_a` : null,
    liftAct: lift ? `${P}${lift}_a` : null, hd, weaponJoint: moving.find(g => g.kind === 'weapon') ? `${P}${moving.find(g => g.kind === 'weapon').name}_j` : null };
}

export class Sim {
  constructor(mj, docs, arena = 'aws2025', accents = ['0.25 0.5 0.95 1', '0.9 0.3 0.25 1']) {
    this.mj = mj; this.docs = docs; this.arena = arena; this.A = ARENAS[arena];
    const sx = this.A.spawn, R = ['a_', 'b_'].map((P, i) => robotXml(P, docs[i], accents[i], [i ? sx : -sx, i ? 0.05 : -0.05], i ? Math.PI : 0));
    this.R = R;
    const xml = `<mujoco><option timestep="${DT}" gravity="0 0 -9.81" cone="elliptic" impratio="2"/>
      <default><geom condim="4" solref="0.0003 1" solimp="0.95 0.99 0.001"/></default>
      <asset>${R[0].assets}${R[1].assets}</asset>
      <worldbody>${arenaXml(this.A)}${R[0].xml}${R[1].xml}</worldbody><actuator>${R[0].acts}${R[1].acts}</actuator></mujoco>`;
    this.xml = xml;
    this.model = mj.MjModel.from_xml_string(xml);
    this.data = new mj.MjData(this.model);
    const m = this.model;
    this.gname = [...Array(m.ngeom).keys()].map(g => m.geom(g).name);
    // contact filtering: own-robot geoms never collide with each other
    for (let g = 0; g < m.ngeom; g++) {
      const nm = this.gname[g], bit = nm.startsWith('a_') ? 2 : nm.startsWith('b_') ? 4 : 0;
      if (bit) { m.geom_contype[g] = bit; m.geom_conaffinity[g] = 0xFFFF & ~bit; } else { m.geom_contype[g] = 1; m.geom_conaffinity[g] = 0xFFFF; }
    }
    this.act = n => m.actuator(n).id;
    this.ctrl = [{ l: 0, r: 0, w: 0 }, { l: 0, r: 0, w: 0 }];
    this.t = 0; this.score = [0, 0]; this.out = [false, false]; this.flipT = [0, 0];
    this.chId = ['a_', 'b_'].map(p => m.body(p + 'ch').id);
    this.wdof = R.map(r => r.weaponJoint ? m.jnt_dofadr[m.jnt(r.weaponJoint).id] : -1);
    this.openedPits = false;
    mj.mj_forward(m, this.data);
  }
  setInput(i, c) { this.ctrl[i] = c; }
  _applyCtrl() {
    const d = this.data;
    for (let i = 0; i < 2; i++) {
      const r = this.R[i], c = this.ctrl[i], doc = this.docs[i];
      for (const w of r.wheelsInfo) d.ctrl[this.act(w.act)] = w.roll * (w.side > 0 ? c.l : c.r) * doc.drive.max_rad_s;
      if (r.weaponAct) d.ctrl[this.act(r.weaponAct)] = c.w ? doc.weapon.omega : 0;
      if (r.liftAct) d.ctrl[this.act(r.liftAct)] = c.w ? doc.lifter.up_rad : doc.lifter.down_rad;
    }
  }
  step(n = 1) {
    const mj = this.mj, d = this.data, m = this.model;
    for (let k = 0; k < n * SUB; k++) { this._applyCtrl(); mj.mj_step(m, d); this._hits(); }
    this.t += n * SUB * DT; this._rules(n * SUB * DT);
  }
  _hits() {  // damage score: weapon parts touching the other robot, weighted by weapon speed
    const d = this.data, cs = d.contact;
    for (let i = 0, nc = d.ncon; i < nc; i++) {
      const c = cs.get(i); if (c.dist > 0) continue;
      const a = this.gname[c.geom1], b = this.gname[c.geom2];
      if (!a || !b || a[0] === b[0]) continue;
      for (const [x, y] of [[a, b], [b, a]]) {
        if (x[0] in { a: 1, b: 1 } && /^[ab]_[wx]/.test(x) && y[1] === '_') {
          const who = x[0] === 'a' ? 0 : 1, r = this.R[who];
          const om = r.weaponJoint ? Math.abs(d.qvel[this.wdof[who]]) : 0;
          this.score[who] += 1e-4 * (om > 5 ? om / 20 : 8);
        }
      }
    }
  }
  pos(i) { const p = this.data.xpos, b = this.chId[i] * 3; return [p[b], p[b + 1], p[b + 2]]; }
  quat(i) { const q = this.data.xquat, b = this.chId[i] * 4; return [q[b], q[b + 1], q[b + 2], q[b + 3]]; }
  yaw(i) { const [w, x, y, z] = this.quat(i); return Math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z)) + this.R[i].hd; }  // world heading of the robot's forward axis
  upZ(i) { const [, x, y] = this.quat(i); return 1 - 2 * (x * x + y * y); }
  _rules(dt) {
    for (let i = 0; i < 2; i++) {
      if (this.pos(i)[2] < OUT_Z) this.out[i] = true;
      this.flipT[i] = this.upZ(i) < -0.3 && !this.docs[i].can_run_inverted ? this.flipT[i] + dt : 0;
    }
    for (const p of this.A.pits) if (this.t >= p[4] && p[4] > 0 && !this.openedPits) { this.openedPits = true; this._openPits(); }
  }
  _openPits() {
    const m = this.model;
    this.gname.forEach((n, g) => { if (n.startsWith('cover')) { m.geom_contype[g] = 0; m.geom_conaffinity[g] = 0; m.geom_rgba[g * 4 + 3] = 0; } });
  }
  result(limit = 90) {
    const lose = i => this.out[i] ? 'ring-out' : this.flipT[i] > 4 ? 'stuck upside down' : null;
    const l0 = lose(0), l1 = lose(1);
    if (l0 && l1) return { winner: -1, why: 'double KO' };
    if (l0) return { winner: 1, why: l0 };
    if (l1) return { winner: 0, why: l1 };
    if (this.t >= limit) { const [a, b] = this.score; return { winner: Math.abs(a - b) < 0.05 ? -1 : a > b ? 0 : 1, why: 'judges decision' }; }
    return null;
  }
  snapshot() {
    const o = [];
    for (let i = 0; i < this.model.nbody; i++) o.push(...this.data.xpos.slice(i * 3, i * 3 + 3), ...this.data.xquat.slice(i * 4, i * 4 + 4));
    return { st: this.t, s: this.score, o: this.out, p: o.map(v => +v.toFixed(5)), g: this.openedPits };
  }
}

export function aiInput(sim, me) {
  const o = 1 - me, a = sim.pos(me), b = sim.pos(o), yaw = sim.yaw(me), h = sim.A.half;
  let tx = b[0], ty = b[1], fwd = 1;
  if (Math.max(Math.abs(a[0]), Math.abs(a[1])) > h - 0.07) { tx = 0; ty = 0; }
  let err = Math.atan2(ty - a[1], tx - a[0]) - yaw; err = Math.atan2(Math.sin(err), Math.cos(err));
  if (sim.upZ(me) < 0 && !sim.docs[me].can_run_inverted) return { l: 1, r: -1, w: 0 };
  const turn = Math.max(-1, Math.min(1, err * 2.2));
  if (Math.abs(err) > 1.2) fwd = 0.1;
  const dist = Math.hypot(b[0] - a[0], b[1] - a[1]);
  const lifter = !!sim.docs[me].lifter;
  return { l: Math.max(-1, Math.min(1, fwd - turn)), r: Math.max(-1, Math.min(1, fwd + turn)), w: lifter ? (dist < 0.1 && Math.abs(err) < 0.4 ? 1 : 0) : 1 };
}
