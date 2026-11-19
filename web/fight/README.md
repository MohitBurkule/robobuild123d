# Antweight Arena (browser fight game)
MuJoCo WASM + three.js, fully client-side. Robots are simplified primitive models (not the CAD exports yet).

- Local: `cd web/fight && npm i && node server.js` -> http://localhost:8080 (any static server works for local/AI modes).
- Keyboard default: P1 WASD + Space, P2 arrows + Enter. Xbox pads optional (pad 0 -> P1, pad 1 -> P2: left stick, A / RT weapon).
- Online: one player picks "host a room", shares code; the other "join a room". Host runs physics, guest sends inputs (relay in server.js).
  LAN: friends open http://<host-ip>:8080. Internet: run server.js on any public host, or put its URL in the "server" field on the static page.

Live: https://robobuild123d.pages.dev/ (Cloudflare Pages: branch dev, no build command, output dir `web/fight`) (GitHub Pages; local + AI modes).
