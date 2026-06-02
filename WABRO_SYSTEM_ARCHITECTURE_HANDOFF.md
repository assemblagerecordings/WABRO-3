# WABRO System Architecture Handoff

Generated: 2026-06-02

Source: pasted architecture handoff at `/Users/lukewabro/.codex/attachments/2292ee39-8a44-47ca-a2a3-8cf8d37f88f9/pasted-text.txt`.

## Purpose

This document defines the current architectural paradigm for Project WABRO. Future AI agents and developers should use it to preserve the relationships between:

- biological signals / EEG
- DAW state
- visual synthesis
- structural metadata
- archive indexing
- AI council workflow

It reinforces the strict division of concerns:

```text
Layer 1: WABRO Instrument
Layer 2: WABRO Knowledge Graph
Layer 3: Platform
```

## Core Architecture Rule

Do not build all layers simultaneously.

Build the instrument first.

```text
Projects
-> Analysis
-> State
-> Macros
-> EEG
-> Visuals
```

Then build the knowledge graph.

Then build the platform.

## Recurring Production Techniques

### Backwards V5 Baseline

`Backwards V5` is the primary mutation target for real-time instrument and macro manipulation.

It should be treated as the first working template for:

- Bitwig macro mapping
- state-to-sound testing
- snare/bass/fill mutation
- visual synchronisation
- Demo 0.1

### Macro-Driven Automation

WABRO should not initially depend on drawing manual automation curves.

Instead:

```text
incoming state arrays
-> 8 macro controls
-> global track behaviours
```

This keeps the system performable and legible.

### Decoupled Plugin Architecture

WABRO should not depend only on closed DAW project internals.

It should extract and record:

- installed plugin paths
- plugin names
- active project plugin references where readable
- save-event metadata
- project fingerprints

The system already has a confirmed installed plugin list from:

```text
/Users/lukewabro/Desktop/plugins.txt
```

## Philosophical Themes

### Deleuzian Assemblage

WABRO rejects purely linear representations of music.

The project treats sound, biological telemetry, software state, and visual geometry as a temporary but cohesive assemblage.

### Continuous Material Mutation

WABRO should not only produce static arrangements.

It should create loops where:

```text
data
sound
visual state
human state
```

warp each other in real time.

### Self-Growing Epistemology

The archive should become machine-readable.

Twenty years of creative output, research, chats, and files should become a living extension of Luke's creative memory through background indexing and project monitoring.

## Visual Paradigm

The first visual engine should be state-driven.

Avoid literal waveform/oscilloscope thinking for the main visual language.

Use:

- core polygons
- orbiting topology
- particle matrices
- shell meshes
- biological disruption/mutation force

The visual object should feel like a geometric organism.

## WABRO Snare Mapping

| Snare component | Audio attribute | Visual translation |
| --- | --- | --- |
| Transient | initial strike energy / spike | core flash / central illumination explosion |
| Fundamental | core fundamental pitch | central polygon base geometry |
| Harmonic | overtones and harmonics | orbiting rings around the centre |
| Noise 1 | primary noise / snare rattle texture | outer particle halo |
| Noise 2 | secondary granular noise / diffuse decay | inner granular cloud matrix |
| Acoustic | physical drum shell resonance | surrounding physical shell mesh |
| EEG state | human brainwave frequencies | global mutation force warping the structure |

## EEG / State Concepts

Muse 2 telemetry should be ingested through:

```text
Muse 2
-> wabro_hub.py
-> 8 macro values
-> OSC
```

Those macro values should simultaneously drive:

- Bitwig macro controls
- TouchDesigner / snare visualiser parameters
- `WABRO_STATE.json`

The goal is a synchronized loop, not a one-to-one toy mapping.

## Business / Platform Rule

Do not launch the platform first.

Correct progression:

```text
Layer 1: self-contained interactive performance instrument
Layer 2: proprietary machine-readable knowledge graph
Layer 3: creator network / marketplace / platform
```

The platform becomes credible only after the instrument proves value.

## AI Council Governance

The AI Council should use deterministic file-separated governance.

Each AI can read shared context but writes only to its assigned file.

Suggested folder:

```text
AI_COUNCIL/
  PRODUCER_AI.md
  SNARE_AI.md
  VISUAL_AI.md
  EEG_AI.md
  ARCHIVIST_AI.md
  BUSINESS_AI.md
  AI_COUNCIL_SUMMARY.md
```

This prevents conflicting edits and keeps each role accountable.

## Graph Schema

The graph schema is stored separately as:

```text
WABRO_PROJECT_GRAPH.json
```

It defines semantic nodes and relationships for:

- Project WABRO
- architecture layers
- Backwards V5
- Muse 2
- `wabro_hub.py`
- project watcher
- 8 macro values
- Bitwig
- TouchDesigner
- WABRO state files
- AI Council
- snare layers

## Immediate Engineering Implications

Codex should now prioritise:

1. Preserve this architecture in WABRO memory.
2. Seed `WABRO_PROJECT_GRAPH.json`.
3. Create `WABRO_PROJECT_GRAPH.md` as a readable explanation of the JSON graph.
4. Build `tools/wabro_project_indexer.py`.
5. Build `tools/wabro_project_watcher.py`.
6. Build `WABRO_INDEX.jsonl`.
7. Build the AI Council folder/files.
8. Continue toward Demo 0.1: `Backwards V5 + Muse/sim + 8 macros + snare geometry + persistent state`.

