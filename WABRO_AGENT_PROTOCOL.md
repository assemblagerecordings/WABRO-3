# WABRO Agent Protocol

This folder is the shared local project memory for WABRO X ASSEMBLAGE.

Agents do not need to message each other directly. They coordinate through files and the local hub.

## Shared Files

- `WABRO_STATE.json`: current live state and macro values.
- `WABRO_LOG.jsonl`: append-only event/state history.
- `WABRO_COMMANDS.jsonl`: append-only external commands.
- `WABRO_TASKS.md`: current work queue.
- `WABRO_MEMORY.md`: discoveries and project memory.
- `CHATGPT_INBOX.md`: notes or questions for ChatGPT or another reasoning agent.
- `CHATGPT_OUTBOX.md`: responses from ChatGPT or another reasoning agent.
- `CODEX_OUTBOX.md`: updates from Codex for other agents.

## Local API

When the hub is running:

```text
GET  http://127.0.0.1:8765/state
GET  http://127.0.0.1:8765/health
GET  http://127.0.0.1:8765/set?state=Pressure
POST http://127.0.0.1:8765/state
```

## OSC

Default outgoing OSC:

```text
127.0.0.1:9000
```

Default live Muse OSC input:

```text
0.0.0.0:5002
```

## Agent Rules

1. Read `WABRO_STATE.json`, `WABRO_TASKS.md`, and `WABRO_MEMORY.md` before acting.
2. Append discoveries to `WABRO_MEMORY.md`.
3. Append events to `WABRO_LOG.jsonl`.
4. Do not overwrite another agent's work without recording the reason.
5. Treat `WABRO_STATE.json` as volatile live state, not permanent memory.
6. Treat `WABRO_MEMORY.md` as the stable project memory.
7. Keep the first goal focused: make the instrument playable before building the platform.

## Current First Goal

Build the Muse 2 / simulator to Bitwig and TouchDesigner bridge for `Backwards V5`.

```text
Muse 2 or simulator
-> WABRO hub
-> WABRO_STATE.json
-> OSC
-> Bitwig + TouchDesigner
```
