# WABRO X ASSEMBLAGE Master Spec

## Purpose

This document is the central briefing file for WABRO X ASSEMBLAGE. It exists so Codex, ChatGPT, collaborators, academic supervisors, visual artists, engineers, and future platform contributors can understand the same project without needing the entire archive in their heads.

The project combines neurofunk production, brain/body data, Bitwig performance control, generative visuals, collaborative release culture, education, and platform design into one open-system artistic practice.

## Core Positioning

WABRO is a neurofunk and experimental drum and bass project treating electronic music as an open system.

Assemblage Recordings is the mutation network around that work: stems, MIDI, production fragments, visuals, documentation, and remixes become source material that others can rebuild, mutate, and extend.

The next stage connects this open-source release ecology to brainwave-controlled performance, Bitwig automation, OSC/MIDI routing, and audiovisual mutation.

## Strong Public Sentence

WABRO turns neurofunk tracks into shared source material, letting producers mutate stems, rebuild sound-objects, and create new versions inside an evolving audiovisual network.

## Project Thesis

The project asks:

How can human emotion, brainwave data, and gesture enter an extreme neurofunk production system without weakening its technical intensity?

The answer is not to map raw brainwaves directly to every parameter. The answer is to build a musical control model:

raw sensor data -> cleaned sensor stream -> features -> performance state -> macro controls -> Bitwig, plugdata, visuals, and platform outputs

## System Stack

- ChatGPT Project: project brain, theory, mapping, planning, documentation, review.
- Codex: code worker for Python bridges, OSC/MIDI routing, Bitwig controller scripts, simulators, tests, and repo maintenance.
- GitHub repo: source of truth for specs, code, schemas, patch notes, tests, and release docs.
- Python: sensor ingestion, smoothing, normalization, feature extraction, macro mapping, OSC/MIDI output.
- OSC: internal communication between systems.
- MIDI CC: DAW-safe control layer.
- Bitwig: primary music host and macro performance environment.
- plugdata / Pure Data / Max: patching, prototyping, and experimental control/audio devices.
- TouchDesigner / Unity: real-time visual performance layer.
- Blender: rendered assets, geometry, animation studies, artwork, and visual identity.

## Sensor Model

Initial sensor source: Muse 2 or simulator.

Do not block development on physical EEG. Build the whole pipeline first with simulated values:

- alpha: 0.0 to 1.0
- beta: 0.0 to 1.0
- gamma: 0.0 to 1.0
- theta: 0.0 to 1.0
- gyro_x: -1.0 to 1.0
- gyro_y: -1.0 to 1.0
- gyro_z: -1.0 to 1.0
- signal_quality: 0.0 to 1.0

Suggested feature layer:

- alpha -> relaxation / openness
- beta -> focus / pressure
- gamma -> detail / intensity
- theta -> drift / memory / tail behaviour
- theta-beta ratio -> cognitive drift
- gyro energy -> gesture movement
- signal_quality -> confidence gate and freeze control

## Bitwig Macro Layer

First target: one fixed Bitwig macro rack. Avoid controlling hundreds of individual parameters until the prototype is stable.

Suggested eight macros:

1. Neuro Energy
2. Focus
3. Tension
4. Movement
5. Darkness
6. Filter Spin
7. Bass Mutation
8. Visual Sync

Protected parameters should stay mostly fixed:

- fundamental snare tuning core
- harmonic semitone/fine-tune identity
- main fader balance
- final clipping ceiling
- master surgical EQ frequencies

Safe parameters for Muse/body modulation:

- drive amount in small ranges
- noise level and filtering
- white-air brightness and width
- room/ghost layer amount
- harmonic level and brightness in small ranges
- master shaping in tiny ranges

## Snare Ontology

The snare system is a model for the wider WABRO sound ontology.

- Fundamental: centred body and punch.
- Harmonic: pitch identity and resonant thread.
- Noise 2: centred skin, crack, grain, friction.
- Noise: stereo air halo and width field.
- Acoustic Snare: physical ghost, human trace, room-body memory.
- Snare Together: master-shaped hybrid object.

Do not use Muse 2 to randomise the snare. Use Muse 2 to perform the relationships between body, identity, skin, air, and ghost.

## Visual Engine Model

The visual system should not be a simple waveform visualiser. It should represent sound objects, control states, and scene logic.

Snare visual model:

- 0 ms: Fundamental ignites as central square/body pulse.
- 8 ms: skin and air begin.
- 12 ms: harmonic thread locks.
- 17 ms: acoustic ghost arrives.
- 20 ms onward: stereo air opens outward.

Layer mapping:

- Fundamental -> central square-body pulse.
- Harmonic -> glowing pitch thread around the identity band.
- Noise 2 -> centred grain skin around the body.
- Noise -> wide white particle halo.
- Acoustic Snare -> ghost mesh / real drum trace.
- Snare Together -> bounded audiovisual object.

Film-sound logic should inform the visuals:

- spotting lists
- atmosphere layers
- transition FX
- dimension filtering
- generative score behaviour
- visual/audio morphing

## Collaboration Framework

The project already contains a collaboration model through Synchronicity and related portfolio work.

Core tension:

How do you let human emotion, voice, or collaborator identity enter an extreme neurofunk machine without weakening the machine?

Future platform role templates:

- Producer
- Vocalist
- Visual artist
- Mixer
- Researcher
- Performer
- Collaborator

The platform should preserve:

- research notes
- mind maps
- asset folders
- collaboration roles
- project evidence
- technical decisions
- reflection/evaluation
- performance exports

## Education Layer

The teaching portfolio turns WABRO into a teachable system.

Possible course/module sequence:

1. Build semi-organic drums.
2. Build synthetic percussion.
3. Build sound-design objects.
4. Add melody and harmony.
5. Finish, clip, sidechain, and perform.
6. Add Muse/brainwave automation.
7. Add visuals.
8. Publish a performance print.

This can become an onboarding path for artists using the future platform.

## Brand Architecture

- WABRO: origin signal.
- Assemblage Recordings: mutation network.
- SIGNAL: first open-system release.
- Stems: source code.
- Remixes: mutations.
- Muse/Bitwig: live mutation engine.
- Visuals: visible sound-object morphology.
- Platform: future rhizome.

Suggested refinement:

Use "WABRO is the origin signal, not the endpoint" instead of "WABRO is not the owner of the sound." This keeps the open-system philosophy while preserving authorship, rights, and licensing clarity.

Artwork system:

- Full-colour artwork: official release identity.
- Two-colour/monochrome treatment: mutation, version, stem, or remix identity.

## GitHub / Release Documents

Immediate repository documents to create:

- README.md
- PROJECT_SPEC.md
- ARCHITECTURE.md
- MAPPING_SCHEMA.json
- SENSOR_SCHEMA.json
- BITWIG_TARGETS.md
- PLUGDATA_PATCH_NOTES.md
- VISUAL_SYSTEM.md
- ROADMAP.md
- SIGNAL_MUTATION_NETWORK_README.md

The most urgent public-facing document is SIGNAL_MUTATION_NETWORK_README.md. It should explain:

- what SIGNAL is
- what people can download
- how to remix/mutate
- how to credit WABRO
- what license applies
- where to upload/send mutations
- what Assemblage Recordings may repost

## Prototype Milestones

### Phase 1: Project OS

Create the repo, schemas, README files, and mapping documents.

### Phase 2: Sensor Simulator

Build simulated EEG/gyro streams so the whole system can be tested without the headset.

### Phase 3: Python Mapping Engine

Implement:

input -> smoothing -> normalization -> feature extraction -> macro mapping -> OSC/MIDI output

### Phase 4: Bitwig Target Rack

Create one fixed macro rack and make it respond musically to the Python bridge.

### Phase 5: plugdata / Visuals

Send the same macro/state values to plugdata and TouchDesigner/Unity.

### Phase 6: Platform Layer

Only after the instrument works, prototype publishing/remix/social features.

## First Demo Target

Build one undeniable performance:

EEG/gyro simulator -> Python smoothing engine -> 8 macro outputs -> Bitwig macro control -> one neurofunk track morphing musically -> visual system showing the mutation.

The first public demo should be understandable in 3 to 5 minutes.

## Questions To Resolve

- What exact headset/device will be used first?
- Is the first system live performance, studio automation, or both?
- What is the first demo track?
- What are the exact 8 to 16 Bitwig parameters that define the WABRO sound?
- Should the first output be MIDI CC only, OSC only, or both?
- What does "spinning song" mean technically?
- What parts of the current Bitwig projects are stable enough to become targets?
- What should be fixed and protected from sensor control?
- What should be allowed to mutate?
- Which collaborator should see the first version of this spec?

## How To Use This Document

Use this file as the briefing layer before asking Codex to build anything.

For Codex:

- Start each coding thread by attaching or referencing this file.
- Ask for one module at a time.
- Keep generated code aligned with the sensor schemas, macro model, and prototype milestones.

For collaborators:

- Share the positioning, system stack, collaboration framework, and first demo target.
- Do not overwhelm collaborators with the full archive until they know their role.

For academic work:

- Use the thesis, sound ontology, education layer, and collaboration framework as the structure for future writing.

For the platform:

- Treat this as the first product requirements document.
- Do not build the social platform until the instrument and performance proof exist.

## Next Archive Reading Pass

Read and inspect sources in this order:

1. Snare Theory screenshots, WAVs, and screen recordings.
2. Year 3 final project, EEG/MIDI, Max/Pure Data/TouchDesigner files.
3. WABRO EPK, brand essence, website, and assets.
4. Year 2 synthesis, mixing, collaboration, and teaching documents.
5. Year 1 production and audio capture documents.

Each pass should update this document with confirmed evidence, not just new ideas.
