import * as THREE from './vendor/three.module.js';
import load from './vendor/mujoco.js';
import { Sim, ARENAS, aiInput } from './sim.js';

const $ = id => document.getElementById(id);
const DOCS = {};
for (const id of await (await fetch('./robots/index.json')).json()) DOCS[id] = await (await fetch(`./robots/${id}.json`)).json();
for (const [k, v] of Object.entries(ARENAS)) $('arena').add(new Option(v.name, k));
for (const s of ['r0', 'r1']) for (const [k, v] of Object.entries(DOCS)) $(s).add(new Option(`${v.name} (${v.robot_type.replace('_', ' ')}, ${v.mass_g} g)`, k));
$('r0').value = 'revron'; $('r1').value = 'wedge_2wd';
const modeUI = () => { const m = $('mode').value; $('joinrow').style.display = m === 'local' ? 'none' : 'flex'; $('code').style.display = m === 'join' ? '' : 'none';
  $('c1').disabled = m !== 'local'; if (m !== 'local') $('c1').value = 'human'; $('c0').disabled = m === 'join'; };
$('mode').onchange = modeUI; modeUI();

const mj = await load({ locateFile: f => new URL('./vendor/' + f, import.meta.url).href });

// ---- renderer
const renderer = new THREE.WebGLRenderer({ canvas: $('c'), antialias: true });
const scene = new THREE.Scene(); scene.background = new THREE.Color(0x0b0e14);
const cam = new THREE.PerspectiveCamera(45, 1, 0.01, 10); cam.up.set(0, 0, 1);
scene.add(new THREE.HemisphereLight(0xffffff, 0x334455, 1.1));
const sun = new THREE.DirectionalLight(0xffffff, 1.6); sun.position.set(0.5, -0.8, 1.5); scene.add(sun);
function resize() { renderer.setSize(innerWidth, innerHeight, false); renderer.setPixelRatio(Math.min(devicePixelRatio, 2)); cam.aspect = innerWidth / innerHeight; cam.updateProjectionMatrix(); }
addEventListener('resize', resize); resize();

let sim = null, meshes = [], root = null;
function buildScene() {
  if (root) { scene.remove(root); }
  root = new THREE.Group(); scene.add(root); meshes = [];
  const m = sim.model;
  for (let g = 0; g < m.ngeom; g++) {
    const t = m.geom_type[g], s = m.geom_size.slice(g * 3, g * 3 + 3), c = m.geom_rgba.slice(g * 4, g * 4 + 4);
    let geo;
    if (t === 6) geo = new THREE.BoxGeometry(s[0] * 2, s[1] * 2, s[2] * 2);
    else if (t === 5) { geo = new THREE.CylinderGeometry(s[0], s[0], s[1] * 2, 28); geo.rotateX(Math.PI / 2); }
    else if (t === 2) geo = new THREE.SphereGeometry(s[0], 12, 8);
    else if (t === 7) {  // convex-hull mesh of a real CAD part
      const id = m.geom_dataid[g], va = m.mesh_vertadr[id], vn = m.mesh_vertnum[id], fa = m.mesh_faceadr[id], fn = m.mesh_facenum[id];
      geo = new THREE.BufferGeometry();
      geo.setAttribute('position', new THREE.BufferAttribute(Float32Array.from(m.mesh_vert.slice(va * 3, (va + vn) * 3)), 3));
      geo.setIndex(Array.from(m.mesh_face.slice(fa * 3, (fa + fn) * 3)) .map(v => v)); geo.computeVertexNormals();
    } else continue;
    const mat = new THREE.MeshStandardMaterial({ color: new THREE.Color(c[0], c[1], c[2]), roughness: 0.5, metalness: c[0] > 0.7 && c[1] > 0.7 ? 0.8 : 0.1, transparent: c[3] < 1, opacity: c[3] });
    const mesh = new THREE.Mesh(geo, mat); mesh.matrixAutoUpdate = false; root.add(mesh);
    mesh.name = sim.gname[g]; meshes.push({ mesh, g, body: m.geom_bodyid[g], p: m.geom_pos.slice(g * 3, g * 3 + 3), q: m.geom_quat.slice(g * 4, g * 4 + 4) });
  }
}
const _q = new THREE.Quaternion(), _q2 = new THREE.Quaternion(), _v = new THREE.Vector3(), _one = new THREE.Vector3(1, 1, 1);
function syncScene() {
  const d = sim.data;
  for (const { mesh, body, p, q } of meshes) {
    const bx = d.xpos.slice(body * 3, body * 3 + 3), bq = d.xquat.slice(body * 4, body * 4 + 4);
    _q.set(bq[1], bq[2], bq[3], bq[0]); _v.set(p[0], p[1], p[2]).applyQuaternion(_q).add(new THREE.Vector3(bx[0], bx[1], bx[2]));
    _q2.set(q[1], q[2], q[3], q[0]); _q.multiply(_q2);
    mesh.matrix.compose(_v, _q, _one);
  }
}
function camera(dt) {
  const a = sim.pos(0), b = sim.pos(1), cx = (a[0] + b[0]) / 2, cy = (a[1] + b[1]) / 2;
  const span = Math.max(0.5, Math.hypot(a[0] - b[0], a[1] - b[1]) + 0.35, sim.A.half * 1.2);
  cam.position.lerp(_v.set(cx * 0.5, cy * 0.5 - span * 0.3, span * 1.3), 0.08); cam.lookAt(cx * 0.6, cy * 0.6, 0);
}

// ---- input
const keys = new Set();
addEventListener('keydown', e => { if (e.repeat) return; keys.add(e.code); if (!['Enter'].includes(e.code) || sim) e.preventDefault?.(); if (e.code === 'KeyR' && sim) rematch(); if (e.code === 'Escape') toMenu(); });
addEventListener('keyup', e => keys.delete(e.code));
const KB = [{ f: 'KeyW', b: 'KeyS', l: 'KeyA', r: 'KeyD', w: 'Space' }, { f: 'ArrowUp', b: 'ArrowDown', l: 'ArrowLeft', r: 'ArrowRight', w: 'Enter' }];
const toggled = [false, false], wasDown = [false, false];
function readInput(i, pad) {  // i = player slot 0/1; keyboard default, gamepad optional (pad index = i)
  const k = KB[i], K = c => keys.has(c) ? 1 : 0;
  let thr = K(k.f) - K(k.b), st = K(k.r) - K(k.l), wd = !!K(k.w);
  const gp = navigator.getGamepads?.()[pad ?? i];  // optional controller; keyboard is the default
  if (gp) {
    const ax = (n, dz = 0.25) => Math.abs(gp.axes[n] || 0) > dz ? gp.axes[n] : 0;
    const gt = -ax(1), gs = ax(0);
    if (gt || gs) { thr = gt; st = gs; }
    wd = wd || gp.buttons[0]?.pressed || (gp.buttons[7]?.value > 0.4);
  }
  if (sim.docs[i].lifter) toggled[i] = wd;
  else { if (wd && !wasDown[i]) toggled[i] = !toggled[i]; }
  wasDown[i] = wd;
  const n = Math.max(1, Math.abs(thr) + Math.abs(st));
  return { l: (thr + st) / n * Math.min(1, n), r: (thr - st) / n * Math.min(1, n), w: toggled[i] ? 1 : 0 };
}

// ---- game state / modes
let mode = 'local', net = null, role = 'local', cfg = null, running = false, over = false;
function status(s) { $('status').textContent = s; }
function wsUrl() { const s = $('srv').value.trim(); if (s) return s.replace(/^http/, 'ws').replace(/\/?$/, '/ws').replace(/\/ws\/ws$/, '/ws'); return (location.protocol === 'https:' ? 'wss://' : 'ws://') + location.host + '/ws'; }

$('go').onclick = async () => {
  mode = $('mode').value;
  cfg = { kinds: [$('r0').value, $('r1').value], arena: $('arena').value, ctl: [$('c0').value, $('c1').value] };
  if (mode === 'local') { role = 'local'; start(cfg); return; }
  status('connecting…');
  net = new WebSocket(wsUrl());
  net.onerror = () => status('cannot reach server (run `node server.js` or set the server field)');
  net.onopen = () => net.send(JSON.stringify(mode === 'host' ? { t: 'host', cfg } : { t: 'join', code: $('code').value }));
  net.onmessage = ev => onNet(JSON.parse(ev.data));
  net.onclose = () => { if (running && role !== 'local') { status('connection lost'); toMenu(); } };
};
let lastSnap = null, guestIn = { l: 0, r: 0, w: 0 };
function onNet(m) {
  if (m.t === 'room') status(`Room ${m.code} — tell your friend this code (and your URL). Waiting…`);
  else if (m.t === 'err') status(m.msg);
  else if (m.t === 'peer') { role = 'host'; start(cfg); }
  else if (m.t === 'joined') { role = 'guest'; cfg = m.cfg; start(cfg); }
  else if (m.t === 'in') guestIn = m.c;
  else if (m.t === 'snap') lastSnap = m;
  else if (m.t === 'rematch' && role === 'guest') { over = false; $('end').style.display = 'none'; }
  else if (m.t === 'left') { status('opponent left'); toMenu(); }
}
function start(c) {
  cfg = c; if (sim) { sim.data.delete(); sim.model.delete(); }
  pitsOpen = false; sim = new Sim(mj, c.kinds.map(k => DOCS[k]), c.arena); toggled[0] = toggled[1] = false; over = false; lastSnap = null; guestIn = { l: 0, r: 0, w: 0 };
  buildScene(); cam.position.set(0, -1, 1.2);
  const ctlName = i => role === 'local' ? (c.ctl[i] === 'ai' ? 'AI' : 'Human') : i === 0 ? (role === 'guest' ? 'host' : 'you (host)') : (role === 'guest' ? 'you' : 'remote player');
  for (const i of [0, 1]) { $('n' + i).textContent = `${DOCS[c.kinds[i]].name} (P${i + 1} · ${ctlName(i)})`; $('b' + i).style.background = i ? '#e5534b' : '#3b82f6'; }
  $('menu').style.display = 'none'; $('end').style.display = 'none'; running = true;
  $('help').textContent = role === 'local' ? [0, 1].map(i => c.ctl[i] === 'ai' ? `P${i + 1}: AI` : i === 0 ? 'P1: WASD + Space' : 'P2: arrows + Enter').join(' · ') + ' · R rematch · Esc menu' : 'WASD (or pad) drive · Space weapon · online';
}
function toMenu() { running = false; sim = null; if (net) { net.onclose = null; net.close(); net = null; } $('menu').style.display = 'flex'; $('end').style.display = 'none'; }
function rematch() { if (role === 'guest') return; if (net?.readyState === 1) net.send(JSON.stringify({ t: 'rematch' })); start(cfg); }
$('again').onclick = rematch; $('tomenu').onclick = toMenu;

// ---- main loop
let prev = performance.now(), acc = 0, netT = 0, snapT = 0;
function frame(now) {
  requestAnimationFrame(frame);
  const dt = Math.min(0.05, (now - prev) / 1000); prev = now;
  if (running && sim) {
    if (role === 'guest') {
      const inp = readInput(0, 0);  // guest drives robot B with the "P1" keys
      netT += dt; if (netT > 1 / 40) { netT = 0; net.send(JSON.stringify({ t: 'in', c: inp })); }
      if (lastSnap) applySnap(lastSnap);
    } else {
      if (!over) {
        const in0 = cfg.ctl?.[0] === 'ai' && role === 'local' ? aiInput(sim, 0) : readInput(0, 0);
        const in1 = role === 'host' ? guestIn : cfg.ctl[1] === 'ai' ? aiInput(sim, 1) : readInput(1, 1);
        sim.setInput(0, in0); sim.setInput(1, in1);
        acc += dt; const ticks = Math.min(24, Math.floor(acc / 0.0008)); acc = Math.min(acc - ticks * 0.0008, 0.0008 * 24);
        // step in chunks so AI/inputs stay fresh
        for (let k = 0; k < ticks; k += 10) sim.step(Math.min(10, ticks - k));
        const r = sim.result();
        if (r) finish(r);
      }
      if (role === 'host' && net?.readyState === 1) { snapT += dt; if (snapT > 1 / 30) { snapT = 0; net.send(JSON.stringify({ t: 'snap', ...sim.snapshot(), over, res: over ? lastRes : null })); } }
    }
    if (role !== 'guest' || lastSnap) { syncScene(); camera(dt); }
    hud();
  }
  renderer.render(scene, cam);
}
let lastRes = null, pitsOpen = false;
function finish(r) {
  over = true; lastRes = r; const names = cfg.kinds.map(k => DOCS[k].name);
  $('endtxt').textContent = r.winner < 0 ? `Draw — ${r.why}` : `${names[r.winner]} wins — ${r.why}`;
  $('end').style.display = 'flex'; $('again').style.display = role === 'guest' ? 'none' : '';
}
function applySnap(s) {
  const d = sim.data, p = s.p;
  for (let i = 0; i < sim.model.nbody; i++) { d.xpos.set(p.slice(i * 7, i * 7 + 3), i * 3); d.xquat.set(p.slice(i * 7 + 3, i * 7 + 7), i * 4); }
  sim.t = s.st; sim.score = s.s;
  if (s.g && !pitsOpen) { pitsOpen = true; for (const { mesh } of meshes) if (mesh.name.startsWith('cover')) mesh.visible = false; }
  if (s.over && !over) finish(s.res);
  if (!s.over && over) { over = false; $('end').style.display = 'none'; }
}
function hud() {
  $('tm').textContent = Math.max(0, 90 - sim.t).toFixed(0);
  const mx = Math.max(1, ...sim.score);
  for (const i of [0, 1]) $('b' + i).style.width = Math.min(100, sim.score[i] / 3 * 100) + '%';
}
requestAnimationFrame(frame);
window.__game = { get sim() { return sim; }, start, keys };
