# Codex Outbox

## 2026-06-01

Codex has created the first local WABRO state bus.

Installed folder:

```text
/Users/lukewabro/Documents/WABRO
```

Working components:

- shared state file: `WABRO_STATE.json`
- log file: `WABRO_LOG.jsonl`
- task list: `WABRO_TASKS.md`
- memory file: `WABRO_MEMORY.md`
- macro map: `WABRO_MACROS.md`
- local hub: `tools/wabro_hub.py`
- simulator launcher: `run_wabro_hub_sim.command`
- live Muse launcher: `run_wabro_hub_live_muse.command`

Verified:

- hub writes `WABRO_STATE.json`
- hub serves `GET /state` on `http://127.0.0.1:8765/state`
- hub accepts manual state changes
- hub can broadcast OSC macro values

Next:

- connect Bitwig to `/wabro/macro/1` through `/wabro/macro/8`
- connect TouchDesigner to `/wabro/state`, `/wabro/pressure`, `/wabro/signal`, and macro values
- switch from simulator to Muse OSC input once the headset stream is working
