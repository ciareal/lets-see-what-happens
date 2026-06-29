# Nazi Zombies: Portable — runnable web build

This repository packages **[Nazi Zombies: Portable](https://github.com/nzp-team/nzportable)**
(a Call of Duty: Zombies de-make built on the **FTEQW** Quake engine) as a
browser-runnable WebAssembly build that you can host yourself.

It plays in a modern browser with WebGL — no install, no plugins.

## What's here

```
web/
├── index.html                  # the normal build — open this
├── ftewebgl.js                 # emscripten engine glue
├── ftewebgl.wasm               # the engine, compiled to WebAssembly (~4.9 MB)
├── default.fmf                 # FTE manifest (declares the "nzp" game)
├── nzportable.ico              # favicon
├── nzp/
│   ├── game.pk3                # all game assets: models, textures, sounds, maps (~89 MB)
│   └── progs.pk3               # compiled QuakeC game logic (~0.5 MB)
└── nzportable-standalone.html  # single-file engine variant (see below)
serve.py                        # tiny static server with correct MIME types
```

## Run it

WebAssembly **must be served over HTTP** — opening the `.html` directly with
`file://` will not work. Any static web server is fine; a helper is included:

```bash
python3 serve.py            # then open http://localhost:8000/index.html
# or, equivalently:
cd web && python3 -m http.server 8000
```

On load it auto-downloads the engine and the two `.pk3` packages, then drops
straight into the game. First load transfers ~95 MB (mostly `game.pk3`).

## The single-file engine HTML

`web/nzportable-standalone.html` is a self-contained **engine** in one file: the
WebAssembly binary and the FTE manifest are base64-embedded directly inside the
HTML, so it carries the whole engine with no `.js`/`.wasm` sidecar files.

It still loads the **game assets** (`nzp/game.pk3`, `nzp/progs.pk3`) from a
sibling `nzp/` folder at runtime. That's deliberate: base64-inlining the ~90 MB
of assets would produce a ~125 MB HTML file that browsers struggle to parse and
cannot stream. So to run the single-file version, keep it next to the `nzp/`
folder and serve it over HTTP:

```bash
cd web && python3 -m http.server 8000
# open http://localhost:8000/nzportable-standalone.html
```

If you genuinely want **one** file with everything inlined (engine *and*
assets), that's possible but impractical for the reasons above — open an issue
and it can be generated.

## Where this came from

These files are the upstream **WebGL build the NZ:P team ships at
[nzp.gay](https://nzp.gay/)** (hosted from
[`nzp-team/nzp-team.github.io`](https://github.com/nzp-team/nzp-team.github.io)),
assembled here into a self-hostable folder. The engine is built from
[`nzp-team/fteqw`](https://github.com/nzp-team/fteqw) (its `make web-rel`
emscripten target), the game logic from
[`nzp-team/quakec`](https://github.com/nzp-team/quakec), and the assets from
[`nzp-team/assets`](https://github.com/nzp-team/assets).

The only change from upstream is removal of an external hit-counter beacon
(`hits.sh`) from `index.html`, so the local build makes no third-party requests.

## Credits & licensing

Nazi Zombies: Portable is a community project by the
[NZ:P Team](https://github.com/nzp-team). FTEQW is by Spike. All game content,
engine code, and trademarks belong to their respective authors — see the
upstream repositories for license terms. This repo only re-packages their
published web build for convenient self-hosting.
