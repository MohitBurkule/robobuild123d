# Antweight Arena (browser fight game)
MuJoCo WASM + three.js, fully client-side. Robots are the real CAD exports (see Real robots).

- Local: `cd web/fight && npm i && node server.js` -> http://localhost:8080 (any static server works for local/AI modes).
- Keyboard default: P1 WASD + Space, P2 arrows + Enter. Xbox pads optional (pad 0 -> P1, pad 1 -> P2: left stick, A / RT weapon).
- Online: one player picks "host a room", shares code; the other "join a room". Host runs physics, guest sends inputs (relay in server.js).
  LAN: friends open http://<host-ip>:8080. Internet: run server.js on any public host, or put its URL in the "server" field on the static page.

Live: https://fight.app.scot/ (Cloudflare Pages: branch dev, no build command, output dir `web/fight`).

## Real robots
`web/fight/robots/*.json` are exported from the repo specs with `PYTHONPATH=src:. python -m robot.fight.webexport robots/<name>/spec.json` (true part hulls, masses, inertias, wheel/weapon hinges, drive + weapon motor data; total scaled to 150 g). The game builds MJCF from them (`sim.js`) and uses the arenas of `robot/fight/arenas.py`. Scythe and Ripsaw do not build yet, so they are not in the roster. Each slot is Human or AI.
