# CODEX OUTBOX

Generated: 2026-06-02

## Current Build Status

The moved AI replies have been folded into a local WABRO Layer 1 workspace at:

```text
/Users/lukewabro/Documents/Wabro 2/WABRO
```

The hub now exposes a `snare_geometry` block alongside `eeg`, `macros`, `pressure`, `signal`, and `state`.

## Implemented From Imported AI Replies

- Consolidated scripts, docs, scans, dashboard, bridge patch, graph, and memory files into `WABRO/`.
- Updated launchers to use the new `Wabro 2/WABRO` path.
- Added `snare_geometry` to `tools/wabro_hub.py`.
- Added OSC output for `/wabro/snare/*` geometry layers.
- Updated the dashboard to consume `snare_geometry`.
- Added the `AI_COUNCIL/` file workflow.

## Snare Geometry Mapping

| Geometry value | Source logic |
| --- | --- |
| `transient` | `snare_transient_bite` plus blink influence |
| `fundamental` | `snare_fundamental` plus delta/body influence |
| `harmonic` | `spectral_rotation`, beta, and snare fundamental |
| `noise1` | `snare_noise` plus gamma pressure |
| `noise2` | `snare_noise`, alpha texture, and glitch probability |
| `acoustic` | space/width, theta, and snare fundamental |
| `mutation_force` | pressure, glitch probability, jaw clench, and gamma |

## Next Test

Run:

```bash
cd "/Users/lukewabro/Documents/Wabro 2/WABRO"
python3 tools/wabro_hub.py --mode sim --rate 10 --http-port 8765 --osc-target 127.0.0.1:9000
```

Then check:

```text
http://127.0.0.1:8765/state
```

Expected result:

- JSON includes `snare_geometry`.
- OSC sends `/wabro/snare/transient`, `/wabro/snare/fundamental`, `/wabro/snare/harmonic`, `/wabro/snare/noise1`, `/wabro/snare/noise2`, `/wabro/snare/acoustic`, and `/wabro/snare/mutation_force`.

