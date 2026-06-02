# WABRO X ASSEMBLAGE

Local working folder for Layer 1 of WABRO: the instrument.

Core objective:

```text
Backwards V5
+ Muse 2 or simulator
+ 8 macros
+ snare geometry
+ persistent state
```

Do not build the platform first. The current build order is:

```text
Instrument -> Knowledge Graph -> Platform
```

## Run

Simulator mode:

```bash
cd "/Users/lukewabro/Documents/Wabro 2/WABRO"
python3 tools/wabro_hub.py --mode sim
```

Live Muse OSC mode:

```bash
cd "/Users/lukewabro/Documents/Wabro 2/WABRO"
python3 tools/wabro_hub.py --mode live-osc --eeg-osc-port 5002
```

State endpoint:

```text
http://127.0.0.1:8765/state
```

Compatibility endpoint:

```bash
python3 tools/state_server.py
```

```text
http://localhost:8000/state
```

Dashboard:

```text
dashboard/index.html
```

Open it in a browser while the hub is running.

## OSC Output

Default target:

```text
127.0.0.1:9000
```

Core addresses:

```text
/wabro/state
/wabro/pressure
/wabro/signal
/wabro/macro/1 ... /wabro/macro/8
/wabro/macro/snare_fundamental
/wabro/macro/snare_noise
/wabro/macro/snare_transient_bite
/wabro/macro/bass_filter_motion
/wabro/macro/bass_distortion
/wabro/macro/spectral_rotation
/wabro/macro/space_width
/wabro/macro/glitch_fill_probability
```

Snare geometry addresses:

```text
/wabro/snare/transient
/wabro/snare/fundamental
/wabro/snare/harmonic
/wabro/snare/noise1
/wabro/snare/noise2
/wabro/snare/acoustic
/wabro/snare/mutation_force
```

## Source Material

Imported AI guidance lives in:

```text
inbox/AIS_REPLY_HANDOFF.txt
```

Distilled project context lives in:

```text
docs/
```

Scan evidence lives in:

```text
Scans/
```

