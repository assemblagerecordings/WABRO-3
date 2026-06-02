# WABRO Demo 0.1 Build Brief

Generated: 2026-06-02

Source: ChatGPT / Bobby handoff in `/Users/lukewabro/Desktop/chat to codex 2.rtf`.

## Critical Architectural Correction

WABRO contains three different systems. They should not be built simultaneously.

### Layer 1 - WABRO Instrument

Build this first.

```text
Projects
-> Analysis
-> State
-> Macros
-> EEG
-> Visuals
```

Outputs:

```text
WABRO_STATE.json
WABRO_MEMORY.md
WABRO_INDEX.jsonl
```

If this layer fails, everything else fails.

### Layer 2 - WABRO Knowledge Graph

Build this after the instrument works.

Inputs:

```text
Bitwig Projects
Audio Renders
Snare Versions
Plugin Chains
AI Chats
Research Docs
University Work
Visual Assets
```

Output:

```text
WABRO_PROJECT_GRAPH.json
```

Think:

```text
Obsidian + Notion + Git + AI Memory for music production.
```

### Layer 3 - Platform

Build this only after Layers 1 and 2 work.

Correct path:

```text
WABRO Instrument
-> Artist Tool
-> Creator Network
-> Platform
```

Avoid:

```text
Idea
-> Platform
```

That path is too broad and likely to kill momentum.

## Demo 0.1 Objective

Build:

```text
Backwards V5
+
Muse 2
+
8 Bitwig macros
+
snare geometry
+
persistent state
```

running together as one system.

## Demo 0.1 Flow

Inputs:

```text
Backwards V5 project
Muse 2
WABRO_STATE.json
```

Processing:

```text
Muse EEG
-> wabro_hub.py
-> 8 macro values
-> OSC
-> Bitwig
-> TouchDesigner / visualiser
```

Outputs:

```text
music changes
visuals change
state saved
log updated
```

If this works, WABRO has its first living instrument.

## First Working Demo Success Criteria

The demo succeeds when:

```text
Muse 2
-> wabro_hub.py
-> 8 macro values
```

and those 8 macro values simultaneously drive:

- Bitwig macro controls
- snare visualiser parameters
- `WABRO_STATE.json` updates

If Muse 2 is not ready yet, simulator mode can temporarily replace Muse input, but the routing must be identical.

## Snare Geometry Design

Do not make the first visualiser a literal waveform visualiser.

Make a state visualiser.

Mapping:

| Snare / state layer | Visual geometry |
| --- | --- |
| Transient | central flash |
| Fundamental | core polygon geometry |
| Harmonic | orbiting rings |
| Noise 1 | outer particle halo |
| Noise 2 | inner granular cloud |
| Acoustic layer | physical shell mesh |
| EEG state | mutation force acting on all geometry |

Goal:

```text
The snare becomes a geometric organism, not just an oscilloscope.
```

This better matches the Assemblage / Deleuzian side of WABRO.

## Immediate Deliverables

Create:

```text
tools/wabro_project_indexer.py
tools/wabro_project_watcher.py
WABRO_PROJECT_GRAPH.json
WABRO_PROJECT_GRAPH.md
WABRO_INDEX.jsonl
```

The watcher should implement:

```text
Project Save
-> extract metadata
-> extract plugin references
-> generate project fingerprint
-> update WABRO_INDEX.jsonl
-> update WABRO_PROJECT_GRAPH.json
-> update WABRO_STATE.json
-> append WABRO_LOG.jsonl entry
```

## AI Council Rule

All AI agents should communicate through files.

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

Each AI can read everything.

Each AI should write only inside its own file.

`AI_COUNCIL_SUMMARY.md` merges proposals.

This prevents AI chaos.

## Real North Star

If the project gets blurry, return to this:

```text
A living creative instrument
that learns from Luke's projects,
maps that knowledge into state,
and allows music, visuals, and EEG
to mutate each other in real time.
```

Do not build a SoundCloud-style platform yet.

Do not build a general operating system yet.

Build:

```text
archive
-> state
-> macros
-> EEG
-> visuals
-> knowledge graph
```

## Codex Build Priority

Current build order:

1. `Backwards V5` becomes the first mutation target.
2. Muse 2 -> WABRO Hub -> OSC/MIDI -> Bitwig macros must become reliable.
3. Create a first snare visualiser prototype.
4. Create the project watcher and knowledge graph.
5. Expand AI council workflows.
6. Ignore social-platform features until the instrument is working.

