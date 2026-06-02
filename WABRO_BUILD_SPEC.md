# WABRO X ASSEMBLAGE BUILD SPEC

## Current Build Goal

Build the first playable EEG to Bitwig bridge for `Backwards V5`.

The first proof is a 5-minute performance where EEG-derived state data controls snare architecture, spectral movement, bass aggression, and visuals without destabilising the mix.

## Architecture

```text
Muse 2
-> feature extraction
-> state smoothing
-> state momentum
-> state engine
-> safety layer
-> OSC / MIDI output
-> Bitwig + visuals
```

## State Model

### Signal

Stable, clear, controlled.

Audio:
- stronger snare fundamental
- lower noise emphasis
- cleaner bass
- wider but stable image

Visuals:
- clean geometry
- smoother motion

### Pressure

Rising intensity and anticipation.

Audio:
- increased transient force
- snare noise rises
- bass drive increases
- modulation depth rises

Visuals:
- sharper movement
- brighter contrast

### Mutation

Exploration and instability.

Audio:
- spectral rotation increases
- FM / wavetable motion increases
- glitch probability rises within safety limits

Visuals:
- deformation
- shape mutation

### Collapse

Controlled overload.

Audio:
- buffer disruption
- fragmentation
- heavy processing, time-limited

Visuals:
- breakup
- noise fields

## Safety Rules

- Python clamps all outgoing macro values.
- Bitwig macro ranges provide a second safety layer.
- Master chain uses conservative limiting.
- Collapse cannot persist indefinitely.
- If EEG stream fails, system falls back to Signal or manual control.

## First Macro Set

1. Snare Fundamental
2. Snare Noise
3. Snare Transient Bite
4. Bass Filter Motion
5. Bass Distortion
6. Spectral Rotation
7. Space / Width
8. Glitch / Fill Probability

## First OSC Address Set

```text
/wabro/state
/wabro/signal
/wabro/pressure
/wabro/mutation
/wabro/collapse
/wabro/macro/1
/wabro/macro/2
/wabro/macro/3
/wabro/macro/4
/wabro/macro/5
/wabro/macro/6
/wabro/macro/7
/wabro/macro/8
```

## First Files To Inspect

- `/Users/lukewabro/Desktop/uni essays/year 3/y 3 files/EEG to Midi V2 (.pd`
- `/Users/lukewabro/Desktop/uni essays/year 3/y 3 files/touchdesigner.pd`
- `/Users/lukewabro/Desktop/uni essays/year 3/y 3 files/FFT.maxpat`
- `/Users/lukewabro/Desktop/uni essays/year 3/y 3 files/fftvocoder.maxpat`
- `/Users/lukewabro/Desktop/uni essays/year 3/y 3 files/spectralsynthesis.amxd`
- `/Users/lukewabro/Desktop/Snare Theory/Snare Layers Bounce/Fundamental.wav`
- `/Users/lukewabro/Desktop/Snare Theory/Snare Layers Bounce/Noise.wav`
- `/Users/lukewabro/Desktop/Snare Theory/Snare Layers Bounce/Noise 2.wav`
- `/Users/lukewabro/Desktop/Snare Theory/Snare Layers Bounce/Harmonic.wav`
- `/Users/lukewabro/Desktop/Snare Theory/main bounce/Snare Together.wav`
- `/Volumes/Luke backups/Music Projects/Music/Backwards/Wabro - Backwards V5.bwproject`

## Rule

The system must feel playable before it becomes a platform.
