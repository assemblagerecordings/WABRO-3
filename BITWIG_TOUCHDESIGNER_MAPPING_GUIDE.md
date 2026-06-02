# Bitwig and TouchDesigner Mapping Guide

## Bitwig: First 8 Macros

Map the incoming values to one performance rack for `Backwards V5`.

| Macro | OSC address | Musical target |
| ---: | --- | --- |
| 1 | `/wabro/macro/1` or `/wabro/macro/snare_fundamental` | Snare body / tonal weight |
| 2 | `/wabro/macro/2` or `/wabro/macro/snare_noise` | Snare air / fizz / noise |
| 3 | `/wabro/macro/3` or `/wabro/macro/snare_transient_bite` | Transient shaper / clipper bite |
| 4 | `/wabro/macro/4` or `/wabro/macro/bass_filter_motion` | Bass cutoff / vowel motion |
| 5 | `/wabro/macro/5` or `/wabro/macro/bass_distortion` | Bass drive / saturation |
| 6 | `/wabro/macro/6` or `/wabro/macro/spectral_rotation` | Spectral motion / phasing |
| 7 | `/wabro/macro/7` or `/wabro/macro/space_width` | Width / reverb / delay space |
| 8 | `/wabro/macro/8` or `/wabro/macro/glitch_fill_probability` | Fills / stutters / interruption |

Use the Pure Data bridge in:

```text
patches/wabro_osc_to_midi.pd
```

if Bitwig is easier to control by MIDI CC than OSC.

## TouchDesigner: Snare Geometry

Receive OSC on port `9000`.

| OSC address | Visual target |
| --- | --- |
| `/wabro/snare/transient` | Central flash / impact spike |
| `/wabro/snare/fundamental` | Core polygon size and solidity |
| `/wabro/snare/harmonic` | Orbiting rings / resonance count |
| `/wabro/snare/noise1` | Outer particle halo density |
| `/wabro/snare/noise2` | Inner granular cloud turbulence |
| `/wabro/snare/acoustic` | Shell mesh thickness / asymmetry |
| `/wabro/snare/mutation_force` | Global deformation and drift |

The visual should behave like a state organism, not a waveform display.

