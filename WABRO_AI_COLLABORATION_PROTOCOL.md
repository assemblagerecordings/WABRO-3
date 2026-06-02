# WABRO AI Collaboration Protocol

Purpose: make any AI that receives this folder useful to WABRO, while letting ChatGPT on Luke's phone act as the director.

This file applies to WABRO 1, WABRO 2, and WABRO 3. If an AI only receives one folder, it should work on that folder. If it receives multiple WABRO folders, it should compare them and say which one is the most complete current source of truth.

## North Star

WABRO is not just a folder of files. It is Luke WABRO's evolving creative system for:

- electronic music as an open system
- Backwards V5 and priority works
- Muse 2 / EEG state control
- 8 macro performance control
- snare geometry as audio + visual ontology
- Bitwig, Pure Data, Max/MSP, TouchDesigner, and web/dashboard bridges
- project memory, graphing, and AI-readable archive growth

Current build order:

```text
Layer 1: Instrument
Layer 2: Knowledge Graph
Layer 3: Platform
```

Do not design the platform first. Help the instrument become real first.

## Phone Director Role

ChatGPT on Luke's phone is the director. It should:

1. Ask each AI for one focused contribution.
2. Keep the WABRO layer order intact.
3. Reject vague inspiration-only replies.
4. Ask for concrete file edits, schemas, mapping tables, bug reports, or next-step plans.
5. Merge useful replies into a single instruction for Codex or another builder AI.

The phone director should not let every AI reinvent WABRO. It should make each AI add one useful piece to the existing architecture.

## What Every AI Should Read First

Read in this order:

1. `README.md`
2. `WABRO_3_EXPORT_REPORT.md`
3. `WABRO_3_STRUCTURE.txt`
4. Any available core WABRO files:
   - `WABRO_MASTER_CONTEXT.md`
   - `WABRO_MEMORY.md`
   - `WABRO_TASKS.md`
   - `WABRO_MACROS.md`
   - `WABRO_PROJECT_GRAPH.json`
   - `WABRO_PROJECT_GRAPH.md`
   - `WABRO_INDEX.jsonl`
   - `tools/`
5. `WABRO_3_AI_EXPORT.txt` only when the AI cannot browse individual files.

## AI Contribution Format

Every AI should respond in this exact structure:

```text
WABRO AI CONTRIBUTION

AI name/model:
Folder version reviewed: WABRO 1 / WABRO 2 / WABRO 3 / multiple
Role: Architect / Builder / Producer / Snare / Visual / EEG / Archivist / Business / Critic

1. What I read:
- file/path
- file/path

2. Current understanding:
short summary in 5 bullets max

3. Most useful finding:
one important insight, bug, mismatch, or opportunity

4. Concrete recommendation:
specific action tied to files, code, mapping, graph, or docs

5. Proposed patch or artifact:
code, markdown, JSON schema, mapping table, or exact instructions

6. Risk / caution:
what could go wrong or what should not be changed

7. Next question for Luke or Codex:
one question only, if needed
```

If the AI cannot inspect the files, it must say so clearly and work only from `WABRO_3_AI_EXPORT.txt`.

## Role Assignments

Use these lanes to avoid duplicated replies:

| Role | What to focus on | Output |
| --- | --- | --- |
| Architect | Layer order, system boundaries, state flow | architecture corrections |
| Builder | scripts, tools, server, dashboard, launchers | code changes or bug list |
| Producer | Bitwig macro usefulness for Backwards V5 | musical mapping notes |
| Snare AI | snare layers, transient/body/noise ontology | snare geometry refinements |
| Visual AI | TouchDesigner/dashboard/snare organism | OSC visual mapping |
| EEG AI | Muse input, smoothing, state inference | safe EEG mapping |
| Archivist | index, scans, graph, folder hygiene | knowledge graph/index plan |
| Business AI | public demo only after instrument works | release/demo narrative |
| Critic | find contradictions and missing tests | review findings |

## Phone Director Prompt

Luke can paste this into ChatGPT on his phone:

```text
You are the WABRO phone director. I am sending you an AI-readable WABRO folder or export.

Your job is not to reinvent WABRO. Your job is to coordinate useful AI input.

First read WABRO_AI_COLLABORATION_PROTOCOL.md.
Then read README.md, WABRO_3_EXPORT_REPORT.md, WABRO_3_STRUCTURE.txt, and the core WABRO docs.

Ask me which role you should play:
Architect, Builder, Producer, Snare AI, Visual AI, EEG AI, Archivist, Business AI, or Critic.

Then produce your reply using the exact WABRO AI CONTRIBUTION format.

Keep the build order:
Instrument -> Knowledge Graph -> Platform.

Focus first on:
Backwards V5 + Muse 2/simulator + 8 macros + snare geometry + persistent state.
```

## Codex Merge Prompt

When Luke has collected replies from several AIs, paste them to Codex with:

```text
Codex, merge these WABRO AI CONTRIBUTION replies.

Do not follow all of them blindly.
Deduplicate them.
Preserve the WABRO layer order.
Prioritize concrete implementation work.
Update the WABRO folder with only the changes that are useful, safe, and aligned with:
Instrument -> Knowledge Graph -> Platform.

Start with Layer 1:
Backwards V5 + Muse 2/simulator + 8 macros + snare geometry + persistent state.
```

## Current Layer 1 Target

The first working proof should make one state source drive three outputs:

```text
Muse 2 or simulator
-> WABRO hub
-> 8 macro values
-> Bitwig macro controls
-> TouchDesigner / snare visualiser
-> WABRO_STATE.json and WABRO_LOG.jsonl
```

## Important Rules

- Do not delete original WABRO folders.
- Do not replace Luke's artistic identity.
- Do not claim EEG is mind-reading.
- Do not build a social platform before the instrument works.
- Prefer small useful file edits over huge speculative documents.
- Preserve Creative Commons Attribution as a core public stance when discussing releases.
- Treat the snare as both an audio object and a visual/state object.
- Treat the archive as memory, not clutter.
