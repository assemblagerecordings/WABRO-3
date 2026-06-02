# WABRO Technical Next Steps

Generated: 2026-06-02

## Current Working Base

Main local WABRO folder:

```text
/Users/lukewabro/Documents/WABRO
```

Current important files:

```text
WABRO_STATE.json
WABRO_LOG.jsonl
WABRO_TASKS.md
WABRO_MEMORY.md
WABRO_MACROS.md
tools/wabro_hub.py
tools/state_server.py
run_state_server.command
run_wabro_hub_sim.command
run_wabro_hub_live_muse.command
CHATGPT_INBOX.md
CHATGPT_OUTBOX.md
CODEX_OUTBOX.md
WABRO_AGENT_PROTOCOL.md
```

Working endpoints:

```text
http://localhost:8000/state
http://127.0.0.1:8765/state
OSC out: 127.0.0.1:9000
Muse OSC in: 0.0.0.0:5002
```

## Practical Build Goal

Build the first playable WABRO instrument:

```text
WABRO_STATE.json
  -> state server / hub
  -> OSC and/or MIDI bridge
  -> Bitwig macro mappings
  -> WABRO snare / bass / spectral parameters
  -> visualiser
  -> AI-readable logs and memory
```

## Architectural Correction

Do not build all WABRO layers at once.

Build order:

```text
Layer 1: WABRO Instrument
Layer 2: WABRO Knowledge Graph
Layer 3: Platform
```

The platform is only justified after the instrument works.

Immediate objective:

```text
Backwards V5
+
Muse 2 or simulator
+
8 macros
+
snare geometry
+
persistent state
```

running together as one system.

## Priority Works To Analyse First

The first analysis set:

1. Backwards
2. Carnage
3. Underground
4. Gentle Whisper
5. Back And Fourth
6. Synchronicity
7. Interpolation
8. WABRO snare system

For each work, create:

```text
project/renders/stems index
arrangement map
snare notes
bass notes
mix/plugin-chain notes
visual state suggestions
WABRO macro mapping suggestions
public/release/licence status
```

## Step 1 - Consolidate Scan Outputs Into WABRO

Current scan outputs live in:

```text
/Users/lukewabro/Documents/Codex/2026-06-01/how-many-files-can-you-take/outputs/
```

Consolidate into WABRO:

```text
WABRO/Scans/
  wabro_read_only_archive_scan.md
  wabro_fast_creative_scan.md
  wabro_scan_project_files.tsv
  wabro_scan_creative_files.tsv
  wabro_scan_keyword_hits.tsv
```

Purpose:

- Make future AI sessions independent of this Codex workspace.
- Keep the hard-drive/MacBook scan evidence available even when the drive is not mounted.
- Feed the project indexer later.

## Step 2 - Pair Projects With Context

Build a joined map connecting:

- project files
- rendered WAVs
- stems
- samples
- plugins used
- equipment/mix context
- university essays/research
- social/release references
- AI chat/explanation history

Target files:

```text
WABRO_PROJECT_GRAPH.md
WABRO_PROJECT_GRAPH.json
```

Initial priority links:

- `Backwards` -> Bitwig project -> V5 -> snare/bass/groups -> state macros.
- `Carnage` -> released WAV -> stems -> pressure/aggression mapping.
- `Underground` -> released WAV -> stems -> dark/space mapping.
- `Gentle Whisper` -> released WAV/project lineage -> emotional/melodic mapping.
- `Back And Fourth` -> collaboration/version lineage.

## Step 3 - Build Searchable Local Knowledge Graph

Create a local index that future agents can query without rescanning everything.

Minimum fields:

```text
path
basename
extension
modified_time
size
category
project_family
keywords
related_work
source_scan
confidence
```

Preferred outputs:

```text
WABRO_INDEX.sqlite
WABRO_INDEX.jsonl
WABRO_INDEX_SUMMARY.md
```

## Step 4 - Create Project Save Watcher

Build a watcher that detects new/changed project saves.

Watched types:

```text
.bwproject
.als
.amxd
.maxpat
.pd
.toe
.wav
.aif
.mid
.txt
.md
```

Behaviour:

```text
new project save
  -> update index
  -> append WABRO_LOG.jsonl
  -> update project graph
  -> write a short AI-readable summary
```

Do not overwrite or modify original projects.

## Step 5 - Muse 2 / EEG Input Bridge

Current hub already supports simulator mode and live Muse OSC input.

Next work:

- Confirm Muse 2 is sending OSC.
- Confirm incoming addresses.
- Smooth values.
- Convert raw EEG/gesture data into WABRO states.
- Avoid overclaiming emotion detection; call it brain-state / affective-state mapping.

Input candidates:

```text
delta
theta
alpha
beta
gamma
blink
jaw_clench
```

State outputs:

```text
Signal
Pressure
Mutation
Collapse
```

## Step 6 - Bitwig Parameter Mapping

Start with 8 macros.

Current macro set:

1. Snare Fundamental
2. Snare Noise
3. Snare Transient Bite
4. Bass Filter Motion
5. Bass Distortion
6. Spectral Rotation
7. Space / Width
8. Glitch / Fill Probability

Recommended bridge:

```text
WABRO Hub OSC -> Pure Data / Max -> MIDI CC -> Bitwig
```

Alternative:

```text
WABRO Hub OSC -> Bitwig OSC extension / controller script
```

First target:

```text
Backwards V5 test copy
```

Rule:

```text
Control group-level musical parameters first, not every plugin parameter.
```

## Step 7 - First Snare Visualiser Prototype

Build a minimal visualiser for the WABRO snare ontology.

Map:

- Fundamental -> core radius / body mass.
- Harmonic layer -> ring count / harmonic geometry.
- Noise layer 1 -> particle field.
- Noise layer 2 -> secondary grain/noise field.
- Transient bite -> edge flash / sharpness.
- Acoustic layer -> organic asymmetry.
- EEG pressure -> deformation intensity.
- EEG signal -> coherence/clarity.

First implementation options:

- TouchDesigner OSC receiver.
- Browser/WebGL/Three.js dashboard.
- Simple 2D canvas if speed matters.

Pass condition:

```text
The snare's layers are visible and respond to WABRO_STATE.json.
```

## Step 8 - Minimal Web UI / Dashboard

Create a local dashboard showing:

- current WABRO state
- pressure/signal values
- EEG band values
- macro values 1-8
- log tail
- connected outputs
- priority work currently targeted

Preferred:

```text
http://localhost:8000/dashboard
```

or separate static HTML:

```text
WABRO/dashboard/index.html
```

## Step 9 - AI-Readable Output Standard

Keep all outputs readable by humans and AI.

Preferred formats:

- Markdown for summaries and specs.
- JSON for current state.
- JSONL for logs/events.
- TSV/CSV for scan tables.
- SQLite only as an index/cache, not the only source.

Every build step should leave behind:

```text
what changed
why it matters
source files used
next action
```

## Immediate Next Build Tasks

1. Build `WABRO_DEMO_0_1_BUILD_BRIEF.md`.
2. Build `tools/wabro_project_indexer.py`.
3. Build `tools/wabro_project_watcher.py`.
4. Create `WABRO_INDEX.jsonl`.
5. Create `WABRO_PROJECT_GRAPH.json`.
6. Create `WABRO_PROJECT_GRAPH.md`.
7. Build `patches/wabro_osc_to_midi.pd`.
8. Build first `Backwards V5` Bitwig macro mapping guide.
9. Build snare visualiser prototype.
10. Build local dashboard.
