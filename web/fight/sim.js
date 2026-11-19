// Shared physics: builds MJCF for 2 robots + arena, steps MuJoCo. Runs in browser and node. Units: m, kg, s.
export const ROBOTS = {
  wedge:   { name: 'Wedge',   desc: 'Low wedge, pushes foes off',       color: '#3a86ff', wpn: null },
  revron:  { name: 'Revron',  desc: 'Vertical disc spinner',            color: '#ff4d4d', wpn: { type: 'disc', omega: 750 } },
  scythe:  { name: 'Scythe',  desc: 'Horizontal bar spinner',           color: '#ffb703', wpn: { type: 'bar', omega: 520 } },
  flipper: { name: 'Flipper', desc: 'Pneumatic-style lifter arm',       color: '#8ac926', wpn: { type: 'flip' } },
};
export const ARENAS = {
  aws2025: { name: 'AWS 2025 (drop-off slot)', half: 0.5, gap: [-0.2, 0.2] },   // gap on +x edge: falling = loss
  closed:  { name: 'Closed box (no way out)',  half: 0.45, gap: null },
};
const DT = 0.0002, SUB = 4; // physics step, steps per sim "tick" (tick = 0.8 ms)

function robotXml(p, kind, x, y, yaw) {
  const w = ROBOTS[kind].wpn, c = ROBOTS[kind].color;
  const rgb = c.match(/\w\w/g).slice(0, 3).map(h => (parseInt(h, 16) / 255).toFixed(2)).join(' ');
  let wpn = '', act = '', exc = '';
  if (w?.type === 'disc') {
    wpn = `<body name="${p}wpn" pos="0.058 0 0.036"><joint name="${p}wj" axis="0 1 0" damping="0.00002"/>
      <geom name="${p}wg" type="cylinder" size="0.034 0.004" euler="90 0 0" mass="0.026" rgba="0.8 0.8 0.85 1" friction="0.8"/>
      <geom name="${p}wt1" type="box" size="0.006 0.005 0.005" pos="0.036 0 0" mass="0.002" rgba="0.9 0.9 0.9 1"/>
      <geom name="${p}wt2" type="box" size="0.006 0.005 0.005" pos="-0.036 0 0" mass="0.002" rgba="0.9 0.9 0.9 1"/></body>`;
    act = `<velocity name="${p}wa" joint="${p}wj" kv="0.00004" forcerange="-0.03 0.03" ctrlrange="-900 900"/>`;
  } else if (w?.type === 'bar') {
    wpn = `<body name="${p}wpn" pos="0 0 0.05"><joint name="${p}wj" axis="0 0 1" damping="0.00002"/>
      <geom name="${p}wg" type="box" size="0.075 0.008 0.003" mass="0.032" rgba="0.8 0.8 0.85 1"/>
      <geom name="${p}wt1" type="box" size="0.006 0.012 0.004" pos="0.07 0 0" mass="0.004" rgba="0.9 0.9 0.9 1"/>
      <geom name="${p}wt2" type="box" size="0.006 0.012 0.004" pos="-0.07 0 0" mass="0.004" rgba="0.9 0.9 0.9 1"/></body>`;
    act = `<velocity name="${p}wa" joint="${p}wj" kv="0.00004" forcerange="-0.03 0.03" ctrlrange="-700 700"/>`;
  } else if (w?.type === 'flip') {
    wpn = `<body name="${p}wpn" pos="0.05 0 0.006"><joint name="${p}wj" axis="0 1 0" range="-1.6 0.05" damping="0.002"/>
      <geom name="${p}wg" type="box" size="0.032 0.042 0.002" pos="0.032 0 0" mass="0.012" rgba="0.8 0.8 0.85 1"/></body>`;
    act = `<position name="${p}wa" joint="${p}wj" kp="0.6" kv="0.01" forcerange="-0.5 0.5" ctrlrange="-1.6 0"/>`;
  }
  const hull = kind === 'wedge' || kind === 'flipper'
    ? `<geom name="${p}hull" type="box" size="0.05 0.047 0.01" pos="0 0 0.016" mass="0.07" rgba="${rgb} 1"/>
       <geom name="${p}wedge" type="box" size="0.04 0.047 0.002" pos="0.05 0 0.014" euler="0 -14 0" mass="0.012" rgba="${rgb} 1"/>`
    : `<geom name="${p}hull" type="box" size="0.05 0.047 0.014" pos="0 0 0.02" mass="0.07" rgba="${rgb} 1"/>`;
  const wheel = (s, n) => `<body name="${p}${n}" pos="-0.012 ${s * 0.058} 0.02"><joint name="${p}${n}j" axis="0 1 0" damping="0.00005"/>
      <geom name="${p}${n}g" type="cylinder" size="0.02 0.008" euler="90 0 0" mass="0.011" friction="1.6 0.01 0.001" rgba="0.1 0.1 0.1 1"/></body>`;
  return `<body name="${p}ch" pos="${x} ${y} 0.0005" euler="0 0 ${yaw}"><freejoint name="${p}free"/>
    ${hull}
    <geom name="${p}skid" type="sphere" size="0.004" pos="0.046 0 0.004" mass="0.001" friction="0.05 0 0"/>
    <geom name="${p}skid2" type="sphere" size="0.004" pos="-0.046 0 0.004" mass="0.001" friction="0.05 0 0"/>
    ${wheel(1, 'wl')}${wheel(-1, 'wr')}${wpn}</body>`
    + '';
}
function mjcf(kinds, arena, inertial) {
  const A = ARENAS[arena], h = A.half;
  let walls = '', k = 0;
  const wall = (n, px, py, sx, sy) => walls += `<geom name="wall${k++}${n}" type="box" size="${sx} ${sy} 0.04" pos="${px} ${py} 0.04" rgba="0.7 0.8 0.9 0.25"/>`;
  const seg = (edge, sign) => {  // wall along an edge with optional gap
    const spans = A.gap && edge === 'e' ? [[-h, A.gap[0]], [A.gap[1], h]] : [[-h, h]];
    for (const [a, b] of spans) {
      const m = (a + b) / 2, L = (b - a) / 2;
      if (edge === 'e' || edge === 'w') wall(edge, sign * (h + 0.005), m, 0.005, L);
      else wall(edge, m, sign * (h + 0.005), L, 0.005);
    }
  };
  seg('e', 1); seg('w', -1); seg('n', 1); seg('s', -1);
  const x0 = 0.28;
  const bodies = kinds.map((kd, i) => robotXml(i ? 'b_' : 'a_', kd, i ? x0 : -x0, 0, i ? 180 : 0)).join('');
  const act = (p, kd) => `<velocity name="${p}al" joint="${p}wlj" kv="0.0012" forcerange="-0.05 0.05" ctrlrange="-90 90"/>
    <velocity name="${p}ar" joint="${p}wrj" kv="0.0012" forcerange="-0.05 0.05" ctrlrange="-90 90"/>`;
  const wa = (kd, p) => {
    const w = ROBOTS[kd].wpn; if (!w) return '';
    return w.type === 'flip' ? `<position name="${p}wa" joint="${p}wj" kp="0.6" kv="0.01" forcerange="-0.5 0.5" ctrlrange="-1.6 0"/>`
      : `<velocity name="${p}wa" joint="${p}wj" kv="0.00004" forcerange="-0.03 0.03" ctrlrange="-900 900"/>`;
  };
  return `<mujoco><option timestep="${DT}" gravity="0 0 -9.81" cone="elliptic" impratio="2"/>
  <default><geom condim="4" solref="0.002 1" solimp="0.95 0.99 0.001" friction="0.9 0.01 0.001"/></default>
  <worldbody><geom name="floor" type="box" size="${h} ${h} 0.01" pos="0 0 -0.01" rgba="0.28 0.3 0.34 1"/>${walls}
  ${bodies}</worldbody>
  <actuator>${act('a_', kinds[0])}${act('b_', kinds[1])}${wa(kinds[0], 'a_')}${wa(kinds[1], 'b_')}</actuator></mujoco>`;
}

export class Sim {
  constructor(mj, kinds, arena = 'aws2025') {
    this.mj = mj; this.kinds = kinds; this.arena = arena; this.A = ARENAS[arena];
    this.model = mj.MjModel.from_xml_string(mjcf(kinds, arena));
    this.data = new mj.MjData(this.model);
    this.t = 0; this.score = [0, 0]; this.out = [false, false]; this.flipT = [0, 0];
    this.ctrl = [{ l: 0, r: 0, w: 0 }, { l: 0, r: 0, w: 0 }];
    this.id = ['a_', 'b_'].map(p => ({
      ch: this.model.body(p + 'ch').id,
      geoms: [...Array(this.model.ngeom).keys()].filter(g => this.model.geom(g).name.startsWith(p)),
    }));
    this.gname = [...Array(this.model.ngeom).keys()].map(g => this.model.geom(g).name);
    this.wdof = ['a_', 'b_'].map(p => ROBOTS[kinds[p === 'a_' ? 0 : 1]].wpn ? this.model.jnt_dofadr[this.model.jnt(p + 'wj').id] : 0);
    mj.mj_forward(this.model, this.data);
  }
  setInput(i, c) { this.ctrl[i] = c; }
  _applyCtrl() {
    const d = this.data, m = this.model;
    for (let i = 0; i < 2; i++) {
      const p = i ? 'b_' : 'a_', c = this.ctrl[i], w = ROBOTS[this.kinds[i]].wpn;
      d.ctrl[m.actuator(p + 'al').id] = c.l * 90;
      d.ctrl[m.actuator(p + 'ar').id] = c.r * 90;
      if (w) {
        const a = m.actuator(p + 'wa').id;
        d.ctrl[a] = w.type === 'flip' ? (c.w ? -1.6 : 0) : (c.w ? w.omega : 0);
      }
    }
  }
  step(n = 1) {  // n ticks of 0.8 ms
    const mj = this.mj, d = this.data, m = this.model;
    for (let k = 0; k < n * SUB; k++) {
      this._applyCtrl();
      mj.mj_step(m, d);
      this._hits();
    }
    this.t += n * SUB * DT;
    this._rules(n * SUB * DT);
  }
  _hits() {  // damage score: weapon geoms touching the other robot, weighted by weapon speed
    const d = this.data, nc = d.ncon, cs = d.contact;
    for (let i = 0; i < nc; i++) {
      const c = cs.get(i); if (c.dist > 0) continue;
      const a = this.gname[c.geom1], b = this.gname[c.geom2];
      for (const [x, y] of [[a, b], [b, a]]) {
        if (/^[ab]_w(g|t\d)$/.test(x) && y[0] !== x[0] && y[1] === '_' && !/^[ab]_w(g|t\d)$/.test(y)) {
          const who = x[0] === 'a' ? 0 : 1, w = ROBOTS[this.kinds[who]].wpn;
          const om = Math.abs(this.data.qvel[this.wdof[who]] || 0);
          this.score[who] += DT * (w.type === 'flip' ? 20 : om / 10);
        }
      }
    }
  }
  pos(i) { const p = this.data.xpos, b = this.id[i].ch * 3; return [p[b], p[b + 1], p[b + 2]]; }
  quat(i) { const q = this.data.xquat, b = this.id[i].ch * 4; return [q[b], q[b + 1], q[b + 2], q[b + 3]]; }
  yaw(i) { const [w, x, y, z] = this.quat(i); return Math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z)); }
  upZ(i) { const [w, x, y] = this.quat(i); return 1 - 2 * (x * x + y * y); }
  _rules(dt) {
    for (let i = 0; i < 2; i++) {
      if (this.pos(i)[2] < -0.03) this.out[i] = true;
      this.flipT[i] = this.upZ(i) < -0.3 ? this.flipT[i] + dt : 0;
    }
  }
  // result: null while running, else {winner: 0|1|-1, why}
  result(limit = 90) {
    const lose = i => this.out[i] ? 'ring-out' : this.flipT[i] > 4 ? 'stuck upside down' : null;
    const l0 = lose(0), l1 = lose(1);
    if (l0 && l1) return { winner: -1, why: 'double KO' };
    if (l0) return { winner: 1, why: l0 };
    if (l1) return { winner: 0, why: l1 };
    if (this.t >= limit) {
      const [a, b] = this.score;
      return { winner: Math.abs(a - b) < 0.05 ? -1 : a > b ? 0 : 1, why: 'judges decision' };
    }
    return null;
  }
  snapshot() {
    const o = [];
    for (let i = 0; i < this.model.nbody; i++) o.push(...this.data.xpos.slice(i * 3, i * 3 + 3), ...this.data.xquat.slice(i * 4, i * 4 + 4));
    return { st: this.t, s: this.score, o: this.out, p: o };
  }
}

// AI: drive at the foe, keep away from the open edge, spin weapon.
export function aiInput(sim, me) {
  const o = 1 - me, a = sim.pos(me), b = sim.pos(o), yaw = sim.yaw(me), h = sim.A.half;
  let tx = b[0], ty = b[1], fwd = 1;
  const nearEdge = Math.max(Math.abs(a[0]), Math.abs(a[1])) > h - 0.07;
  if (nearEdge) { tx = 0; ty = 0; }
  let err = Math.atan2(ty - a[1], tx - a[0]) - yaw;
  err = Math.atan2(Math.sin(err), Math.cos(err));
  if (sim.upZ(me) < 0) return { l: 1, r: -1, w: 0 };
  const turn = Math.max(-1, Math.min(1, err * 2.2));
  if (Math.abs(err) > 1.2) fwd = 0.1;
  const dist = Math.hypot(b[0] - a[0], b[1] - a[1]);
  return { l: Math.max(-1, Math.min(1, fwd - turn)), r: Math.max(-1, Math.min(1, fwd + turn)), w: dist < 0.35 || true ? 1 : 0 };
}
