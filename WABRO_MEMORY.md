# WABRO MEMORY

## Confirmed Context

- Luke Wabro is building WABRO X ASSEMBLAGE.
- The near-term goal is an EEG to Bitwig bridge.
- The active prototype project is `Backwards V5`.
- The strongest strategic rule is: the system must feel playable before it becomes a platform.

## Archive Findings

- Full read-only scan found over 1.3 million files.
- Fast creative scan found over 900k files.
- There are thousands of Bitwig, Ableton, Pure Data, Max, and Max for Live files.
- The archive is strongly audio-first and instrument-first.

## Highest Value Clusters

### EEG / Muse / Bridge

- `EEG to Midi V2 (.pd`
- `touchdesigner.pd`
- Muse Port Max for Live devices
- `Final Submission - Possibilities (with EEG Headset).bwproject`

### Spectral / FFT

- `FFT.maxpat`
- `fftvocoder.maxpat`
- `fft filter.amxd`
- `fftmaxguestlecturer.amxd`
- `hgfilterpfft.maxpat`
- `spectralsynthesis.amxd`
- `max vocoder spectral.amxd`

### Snare

- `Fundamental.wav`
- `Noise.wav`
- `Noise 2.wav`
- `Harmonic.wav`
- `Acoustic Snare.wav`
- `Snare Together.wav`

### Performance

- `Backwards V5`
- `Back And Fourth`
- released `Signals` tracks

## Working Hypothesis

WABRO X ASSEMBLAGE should not be framed as EEG to MIDI alone.

The stronger frame is:

```text
EEG
-> state engine
-> snare layer morphing
-> spectral transformation
-> bass and arrangement pressure
-> shared audiovisual state
```

## Local Hub Build

Created a local WABRO hub design:

```text
WABRO_STATE.json
WABRO_LOG.jsonl
HTTP API on 127.0.0.1:8765
OSC output to 127.0.0.1:9000
Live Muse OSC input on UDP 5002
```

The hub supports two modes:

- `sim`: generates stable simulated EEG-like pressure/signal/macros.
- `live-osc`: listens for Muse OSC and converts band/artifact values into the state engine.

The hub writes the same macro map as the first Build Spec:

1. Snare Fundamental
2. Snare Noise
3. Snare Transient Bite
4. Bass Filter Motion
5. Bass Distortion
6. Spectral Rotation
7. Space / Width
8. Glitch / Fill Probability

The hub has:

- smoothing
- state momentum through gradual macro interpolation
- safety clamps per macro
- HTTP `/state`, `/health`, and `/set?state=...`
- OSC `/wabro/state`, `/wabro/pressure`, `/wabro/signal`, and `/wabro/macro/...`

Next practical routing:

```text
Muse 2 or simulator
-> wabro_hub.py
-> WABRO_STATE.json
-> OSC 127.0.0.1:9000
-> Bitwig / TouchDesigner
```

Compatibility server added:

```text
tools/state_server.py
run_state_server.command
http://localhost:8000/state
```

This is a simple named entrypoint for tools or agents expecting a `state_server.py` process.

## 2026-06-01 First Instrument Assembly Pass

### EEG to MIDI Patch

File:

- `/Users/lukewabro/Desktop/uni essays/year 3/y 3 files/EEG to Midi V2 (.pd`

Confirmed behaviour:

- Receives Muse OSC over UDP with `netreceive -u -b 5002`.
- Parses OSC using `oscparse`, `list trim`, `route muse`, and `route elements eeg`.
- Routes `jaw_clench`, `blink`, `gamma_absolute`, `beta_absolute`, `alpha_absolute`, `theta_absolute`, and `delta_absolute`.
- Converts blink and jaw-clench events into MIDI-note style triggers.
- Clips EEG streams around `0` to `0.5`.
- Scales EEG streams to MIDI range `0` to `127`.
- Outputs MIDI CC values with `ctlout` on channels/CCs including `1` through `12`.
- Contains an existing smoothing object: `smooth2 1000 1000`.

Interpretation:

This is already a prototype bridge from Muse OSC to MIDI control. The next build should not discard it. The next build should abstract its useful idea into a clearer state engine:

```text
Muse OSC
-> band features and artifact events
-> smoothing
-> state/macro values
-> OSC + MIDI outputs
```

### TouchDesigner Patch

File:

- `/Users/lukewabro/Desktop/uni essays/year 3/y 3 files/touchdesigner.pd`

Confirmed behaviour:

- Receives OSC on port `10001` using `osc.receive`.
- Routes hand/gesture-style addresses including `Closed_Fist`, `Thumb_Up`, `Open_Palm`, and `pinch_midpoint:distance`.
- Uses `round`, `change`, `play.file~`, `dac~`, `midiformat`, and `midi.out`.

Interpretation:

This patch is gesture/TouchDesigner-facing rather than Muse-facing, but it proves a second control route:

```text
TouchDesigner / MediaPipe gesture OSC
-> Pure Data
-> audio triggers and MIDI output
```

For WABRO X ASSEMBLAGE, this can become the visual/gesture sibling of the Muse state engine.

### Muse Port Device

File:

- `/Users/lukewabro/Music/Ableton/User Library/Presets/Audio Effects/Max Audio Effect/Imported/Muse Port 1.3.3 [blink and clench toggle].amxd`

Confirmed behaviour from readable strings:

- It is a Max for Live device.
- It contains parsing/slicing logic for OSC-style slash-separated messages.
- It includes blink/clench toggle logic.
- It includes Muse analysis patchers in the wider Max project folder.

Interpretation:

This is likely the cleanest existing Muse/Ableton ingestion route. It should be inspected as a reference for what Muse messages exist and how previous tools parsed them.

### Backwards V5 Project

File:

- `/Volumes/Luke backups/Music Projects/Music/Backwards/Wabro - Backwards V5.bwproject`

Confirmed project structure:

- `Kick Trigger`
- `Snare Trigger`
- `Noise 2`
- `Snare Master`
- `Percussion`
- `Break`
- `Ghost Snare`
- `Cymbal`
- `Hat Open`
- `Shaker`
- `Percussion Master`
- `Bass Trigger`
- `Lead Stab Stretch`
- `Instrument Layer`
- `Textures`
- `Fill 2`
- `Bass FIll`
- `Fills Master`
- `Bass Fill Layer 1`
- `Bass Fill layer 2`
- `Bass Fill Layer 3`
- `Textures 2`
- `Risers 2`
- `Risers`
- `Downlifter`
- `Chords`
- `Strings`
- `SC Master`
- `MTurboReverb`
- `Master`

Confirmed used sample set includes:

- `samples/05 Kick-3-2.wav`
- `samples/Stage 3 CKD Template pack clean 4 V1 2026-02-27 1058.wav`
- `samples/03 Snare 3-3.wav`
- `samples/01 Snare 1.wav`
- `samples/CLAP.wav`
- `samples/01 Snare 1-2.wav`
- `samples/01 Snare 1-2-2.wav`
- `samples/09 Hat 3-4.wav`
- `samples/09 Hat 3-2.wav`
- `samples/11 Hat 5.wav`
- `samples/06 shaker-3.wav`
- `samples/DOWNLIFTER.wav`
- `samples/Downlifter-2.wav`
- `samples/KULTURE_LIQDNB1_KULTURE_LIQDNB1_IMPACT_11.wav`

Confirmed plugin/device evidence:

- FabFilter Pro-Q 3
- Oszillos Mega Scope
- Newfangled Saturate
- MTurboReverb

Interpretation:

`Backwards V5` is a good first performance target because it already exposes snare, percussion, bass, texture, fill, riser, sidechain, reverb, and master subsystems. The first macro map should target group-level controls instead of trying to control hundreds of internal plugin parameters.

## 2026-06-02 Studio, Plugin, Priority Works Update

Luke confirmed the current high-value studio equipment:

- ATC SCM50 ASL Pro
- Trinnov NOVA
- RME Fireface UFX III
- 3x Pioneer CDJ-3000
- Pioneer DJM-A9
- Barefoot Footprint 02

Luke provided `/Users/lukewabro/Desktop/plugins.txt`, an installed VST3 list with 381 plugin entries. Major families include MeldaProduction, Plugin Alliance / Brainworx, Kilohearts, iZotope, FabFilter, Native Instruments, Sonnox, Universal Audio, Valhalla, Soundtheory / Gullfoss, Xfer Serum/Serum2, Scaler, and Waves.

Luke explicitly marked these as the main works to focus on:

- Gentle Whisper
- Carnage
- Underground
- Backwards
- Back And Fourth

Interpretation:

The project should treat these five works as the first WABRO reference set and use them to extract "Luke Grammar" for snare, bass, mix, emotional pressure, arrangement, and visual/state mapping. `Backwards` remains Prototype Piece 001 because it is the strongest Bitwig mutation target. `Carnage` and `Underground` are strong public/stem references. `Gentle Whisper` broadens the emotional range. `Back And Fourth` captures collaboration and version lineage.

Luke also confirmed that `/Users/lukewabro/Desktop/WABRO AI` is the main Desktop staging folder for previous attempts to communicate WABRO to AI. It contains reference docs, exports, prior chat documents, Backwards upload files, social/project exports, priority audio references, and Snare Theory.

## 2026-06-02 ChatGPT Handoff Integrated

Canonical project identity:

`WABRO = Electronic Music as an Open System.`

WABRO OS / WABRO X ASSEMBLAGE is an AI-assisted creative operating system for Luke/WABRO's neurofunk, experimental drum and bass, EEG, visualiser, Bitwig, TouchDesigner, Muse 2, snare design, archive scanning, and open-source music ecosystem.

Luke confirmed the Creative Commons position:

- WABRO music is licensed under Creative Commons Attribution.
- People can mutate/remix/rebuild it as long as they credit WABRO.

The priority works have expanded to:

- Gentle Whisper
- Carnage
- Underground
- Backwards
- Back And Fourth
- Synchronicity
- Interpolation
- WABRO snare system

The WABRO snare should be understood as both an audio object and visual/algorithmic object, combining acoustic Superior Drummer-style snare microphone routing, synth reinforcement, fundamental layer, harmonic layer, and two noise layers. The long-term aim is a geometric visualiser that emulates the snare waveform/structure and allows Muse 2 / EEG state to modulate both music and visuals.

## 2026-06-02 ChatGPT / Bobby Build Correction

ChatGPT/Bobby clarified that WABRO has three build layers that should not be built simultaneously:

1. WABRO Instrument
2. WABRO Knowledge Graph
3. Platform

The immediate target is Demo 0.1:

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

Important correction:

- Do not build a SoundCloud-style platform yet.
- Do not build a general operating system yet.
- Build the living creative instrument first.

Snare visualiser should be a state visualiser, not a literal waveform visualiser:

- Transient -> central flash
- Fundamental -> core polygon geometry
- Harmonic -> orbiting rings
- Noise 1 -> outer particle halo
- Noise 2 -> inner granular cloud
- Acoustic layer -> physical shell mesh
- EEG state -> mutation force

AI Council improvement:

Each AI should read shared context but write only to its own file under `AI_COUNCIL/`. A merged `AI_COUNCIL_SUMMARY.md` prevents AI chaos.

## 2026-06-02 System Architecture Handoff

Integrated a system architecture handoff that defines WABRO as a strict layered architecture:

1. WABRO Instrument
2. WABRO Knowledge Graph
3. Platform

The handoff adds a formal semantic graph with nodes for Project WABRO, architecture layers, `Backwards V5`, Muse 2, `wabro_hub.py`, `tools/wabro_project_watcher.py`, 8 OSC macro values, Bitwig, TouchDesigner, Deleuzian Assemblage, Geometric Organism, `WABRO_STATE.json`, `WABRO_PROJECT_GRAPH.json`, AI Council workflow, and the main snare layers.

Created graph seed files:

- `WABRO_PROJECT_GRAPH.json`
- `WABRO_PROJECT_GRAPH.md`

Design rule reinforced:

The visualiser should represent internal structural tensions and system states, not a literal waveform. The snare should become a geometric organism.
