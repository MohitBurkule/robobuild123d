// Static file server + WebSocket room relay. `node server.js [port]`  -> http://<your-ip>:8080
// LAN: friends open http://<your-ip>:8080. Internet: run on any host (Fly/Render/VPS) or tunnel; page uses wss:// automatically on https.
import http from 'http'; import fs from 'fs'; import path from 'path'; import { fileURLToPath } from 'url';
import { WebSocketServer } from 'ws';
const root = path.dirname(fileURLToPath(import.meta.url)), port = +process.argv[2] || process.env.PORT || 8080;
const types = { '.html': 'text/html', '.js': 'text/javascript', '.wasm': 'application/wasm', '.json': 'application/json', '.css': 'text/css' };
const srv = http.createServer((q, r) => {
  let p = decodeURIComponent(q.url.split('?')[0]); if (p === '/') p = '/index.html';
  const f = path.join(root, path.normalize(p).replace(/^(\.\.[/\\])+/, ''));
  if (!f.startsWith(root) || f.includes('node_modules')) { r.writeHead(403).end(); return; }
  fs.readFile(f, (e, d) => e ? r.writeHead(404).end('not found') : r.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream' }).end(d));
});
const rooms = new Map(); // code -> {host, guest}
const wss = new WebSocketServer({ server: srv, path: '/ws' });
const code = () => Math.random().toString(36).slice(2, 6).toUpperCase();
wss.on('connection', ws => {
  ws.on('message', raw => {
    let m; try { m = JSON.parse(raw); } catch { return; }
    if (m.t === 'host') {
      let c = code(); while (rooms.has(c)) c = code();
      rooms.set(c, { host: ws, guest: null, cfg: m.cfg }); ws.room = c; ws.role = 'host';
      ws.send(JSON.stringify({ t: 'room', code: c }));
    } else if (m.t === 'join') {
      const R = rooms.get((m.code || '').toUpperCase());
      if (!R || R.guest) return ws.send(JSON.stringify({ t: 'err', msg: R ? 'room full' : 'no such room' }));
      R.guest = ws; ws.room = m.code.toUpperCase(); ws.role = 'guest';
      ws.send(JSON.stringify({ t: 'joined', cfg: R.cfg })); R.host.send(JSON.stringify({ t: 'peer' }));
    } else {  // relay: in/snap/rematch...
      const R = rooms.get(ws.room); if (!R) return;
      const o = ws.role === 'host' ? R.guest : R.host;
      if (o && o.readyState === 1) o.send(raw.toString());
    }
  });
  ws.on('close', () => {
    const R = rooms.get(ws.room); if (!R) return;
    const o = ws.role === 'host' ? R.guest : R.host;
    if (o && o.readyState === 1) o.send(JSON.stringify({ t: 'left' }));
    if (ws.role === 'host') rooms.delete(ws.room); else R.guest = null;
  });
});
srv.listen(port, () => console.log(`fight server on http://localhost:${port}`));
