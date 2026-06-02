# WABRO FIRST MACRO MAP

This is the first playable control surface for `Backwards V5`.

The goal is not to expose every detail of the Bitwig project. The goal is to create 8 reliable musical handles that can survive noisy EEG input.

## Macro 1: Snare Fundamental

Target:

- snare body
- tonal weight
- perceived pitch centre

State behaviour:

- Signal: high
- Pressure: medium
- Mutation: moving
- Collapse: reduced or unstable

## Macro 2: Snare Noise

Target:

- white-noise layer
- stereo fizz
- aggressive air

State behaviour:

- Signal: low
- Pressure: high
- Mutation: animated
- Collapse: high but clamped

## Macro 3: Snare Transient Bite

Target:

- clipper drive
- attack emphasis
- transient shaper or equivalent

State behaviour:

- Signal: clean
- Pressure: sharp
- Mutation: variable
- Collapse: sharp but time-limited

## Macro 4: Bass Filter Motion

Target:

- filter cutoff movement
- vowel movement
- bass articulation

State behaviour:

- Signal: stable
- Pressure: more movement
- Mutation: high motion
- Collapse: abrupt movement, clamped

## Macro 5: Bass Distortion

Target:

- saturation / distortion / drive
- bass aggression

State behaviour:

- Signal: low-medium
- Pressure: medium-high
- Mutation: animated
- Collapse: high but safety-capped

## Macro 6: Spectral Rotation

Target:

- FFT / vocoder / spectral remapping amount
- frequency-space motion
- phasing or rotation illusion

State behaviour:

- Signal: subtle
- Pressure: rising
- Mutation: primary feature
- Collapse: broken/fragmentary but bounded

## Macro 7: Space / Width

Target:

- reverb send
- stereo width
- delay or ambience

State behaviour:

- Signal: wide and clear
- Pressure: tighter
- Mutation: moving
- Collapse: unstable but not washed out

## Macro 8: Glitch / Fill Probability

Target:

- fill density
- buffer/stutter probability
- drum interruption

State behaviour:

- Signal: low
- Pressure: medium
- Mutation: high
- Collapse: high but timeout-limited

## Initial Safety Limits

```json
{
  "snare_fundamental": [0.15, 0.95],
  "snare_noise": [0.05, 0.85],
  "snare_transient_bite": [0.10, 0.80],
  "bass_filter_motion": [0.05, 0.90],
  "bass_distortion": [0.05, 0.70],
  "spectral_rotation": [0.00, 0.85],
  "space_width": [0.10, 0.90],
  "glitch_fill_probability": [0.00, 0.40]
}
```

## Recommended First Output

Send both:

- MIDI CC for Bitwig compatibility.
- OSC for TouchDesigner and future tools.

This keeps the bridge DAW-safe while leaving the visual/state system expressive.
