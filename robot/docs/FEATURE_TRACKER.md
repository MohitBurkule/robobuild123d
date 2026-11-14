# Feature tracker: the 52-item plan

Working branch for the post-roadmap feature blitz. Status: `[x]` done (with tests),
`[~]` partial, `[ ]` not started. Each item lands as its own commit on this branch;
this file is updated as items complete. Numbering follows the review that proposed
the plan (2026-11-14, after the 80-PR merge campaign).

## A. Finish what is half-built

| # | Item | Status | Notes |
|---|------|--------|-------|
| A1 | Wiring harness implementation (channels, netlist, router, solids, checks) | [ ] | #80 shipped the data model only |
| A2 | Elevron Alt (#22) remediation: rebase, `_floor_rounded` fix, module-list conflict | [ ] | needs gen work; tracked separately |
| A3 | Limpet XXT (#81) completion | [ ] | |
| A4 | Promote DFM drafts (#78) to blockers once calibrated | [ ] | |
| A5 | Wire real motor curves into #72 physics + sim | [~] | `physics` group landed closed-form; curves pending |

## B. LLM interface

| # | Item | Status | Notes |
|---|------|--------|-------|
| B1 | Requirements block in design.json (`resolve`, claims, `requirements.*`) | [x] | `requirements.*` check group (robot/checks/requirements.py) + `requirements` spec key |
| B2 | Compact LLM report with iteration delta (`robot llm-report --prev`) | [x] | robot/llm_report.py + test_llm_report.py |
| B3 | Self-repair loop (`robot/gen/repair.py`) | [ ] | |
| B4 | Design patch language (`robot/design_io/patch.py`: apply/diff) | [x] | provenance (`design why`) still open |
| B5 | `robot mcp` stdio server | [x] | robot/mcp_server.py: schema, catalog, validate, explain, diff, guide tools |
| B6 | One error envelope + one JSON schema across both front doors | [x] | Schema.errors/json_schema + test_design_envelope.py |
| B7 | Generated LLM pack (SKILL.md, examples) with drift test | [ ] | |
| B8 | `robot explain <finding-id>` | [x] | robot/checks/explain.py, coverage-tested vs registry + hint table |

## C. Robustness & speed

| # | Item | Status | Notes |
|---|------|--------|-------|
| C1 | Param relation graph with provenance | [ ] | large refactor |
| C2 | Robust geometry ops with blame (`safe_fillet`, selectors) | [ ] | |
| C3 | Insertion-path relations + numeric fixes | [ ] | |
| C4 | Proxy verify tier <1 s + per-part incremental rebuild | [~] | proxy module exists |
| C5 | Single source of truth for choices | [ ] | |
| C6 | Fuzz the hypothesis space (no bare OCP errors) | [ ] | |

## D. Manufacturability

| # | Item | Status | Notes |
|---|------|--------|-------|
| D1 | Printer/filament profiles + capability findings | [x] | robot/mfg_profiles.py (capability model; report wiring pending) |
| D2 | Named fits with process compensation (`robot/fits.py`) | [x] | library + bands; CAD-hole wiring is gen-side |
| D3 | Build-plate export (oriented, packed STL + plates.json) | [x] | robot/plate.py |
| D4 | Purchasable BOM (UK vendors, packs, spares, order CSVs) | [x] | robot/bom_out.py |
| D5 | Slice-based mass & print-time estimate | [ ] | |
| D6 | DXF sheet/turned-part order pack | [ ] | |
| D7 | Assembly instructions (steps doc from disassembly order) | [x] | robot/assembly_doc.py -> build.md |

## E. UX

| # | Item | Status | Notes |
|---|------|--------|-------|
| E1 | HTML report with embedded 3D viewer (GLB) | [x] | robot/report_html.py + robot/glb.py, `robot report -o report.html` |
| E2 | `robot diff A B` (exit 3 on regressions) | [x] | robot/diffcmd.py + test_diffcmd.py |
| E3 | Builder profile check group | [ ] | |
| E4 | Selectable rules profiles (`robot/profiles/*.json`) | [ ] | |
| E5 | Fork hygiene: restrict upstream publish.yml, NOTICE, path guards | [~] | publish.yml upload_pypi gated on upstream repo; NOTICE/path guards deferred |
| E6 | Gallery page | [ ] | |

## F. Physics & verification checks

| # | Item | Status | Notes |
|---|------|--------|-------|
| F1 | Gyro wheel-lift + hit reaction | [x] | `impact.*` group (robot/checks/impact.py): gyro_lift, hop, yaw |
| F2 | Real motor curves in sim + fight scoring | [ ] | |
| F3 | Rest/dead-pose analysis (`rest.*`) | [ ] | |
| F4 | Thermal & brownout budget (`thermal.*`) | [x] | robot/checks/thermal.py: brownout, sag, esc_overcurrent |
| F5 | Load paths beyond the weapon shaft | [ ] | |
| F6 | Serviceability (`service.*`) | [ ] | |

## G. Additional verification checks

| # | Item | Status | Notes |
|---|------|--------|-------|
| G1 | Tolerance stack-up chains across mating parts | [ ] | |
| G2 | Coaxiality of bearing/bore seats across mated parts | [ ] | |
| G3 | Fastener engagement % (length vs clamped stack) | [ ] | |
| G4 | Driver/tool straight-line access to every fastener | [ ] | |
| G5 | Wire chafe, bend radius, connector strain relief | [ ] | |
| G6 | RF placement (receiver/antenna away from noise, exit path) | [ ] | |
| G7 | Weapon full-360° self-sweep vs own body | [ ] | |
| G8 | Ground clearance at rest with tire squash; wedge deflection | [ ] | |
| G9 | COM over drive contact patch (traction/push balance) | [ ] | |
| G10 | Mesh determinism golden-hash regression (tolerance-banded) | [ ] | |

## H. Archetypes

| # | Item | Status | Notes |
|---|------|--------|-------|
| H1 | Declarative weapon-module contract | [ ] | |
| H2 | Belt-driven drum/eggbeater/disc weapons | [ ] | |
| H3 | Weapon sizing solver (energy/tip-speed -> dims) | [x] | robot/gen/weapon_size.py: disc sizing + inverse energy_for(); drum/eggbeater deferred |
| H4 | 4WD for all archetypes; undercutter; linkage family; shuffler; presets | [ ] | |

## I. CI & process

| # | Item | Status | Notes |
|---|------|--------|-------|
| I1 | Coverage ratchet + benchmark trend tracking | [ ] | |
| I2 | Nightly full slow-set run + fuzz job | [ ] | |
| I3 | macos-14 runner fix/replace (cancelled in tests + benchmarks) | [ ] | infra-side |
