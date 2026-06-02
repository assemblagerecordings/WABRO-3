# WABRO Local Hub

The WABRO hub is the first local state bus for the project.

It does four things:

1. Updates `WABRO_STATE.json`.
2. Appends history to `WABRO_LOG.jsonl`.
3. Serves the current state over HTTP.
4. Broadcasts the same state and macro values over OSC.

## Run Simulator Mode

Double-click:

```text
/Users/lukewabro/Documents/WABRO/run_wabro_hub_sim.command
```

Simple compatibility launcher:

```text
/Users/lukewabro/Documents/WABRO/run_state_server.command
```

This exposes:

```text
http://localhost:8000/state
```

or run:

```bash
cd /Users/lukewabro/Documents/WABRO
python3 tools/wabro_hub.py --mode sim
```

HTTP state:

```text
http://127.0.0.1:8765/state
```

Compatibility HTTP state:

```text
http://localhost:8000/state
```

Default OSC output:

```text
127.0.0.1:9000
```

## Run Live Muse OSC Mode

Use this when the Muse stream is sending OSC to the Mac.

Double-click:

```text
/Users/lukewabro/Documents/WABRO/run_wabro_hub_live_muse.command
```

or run:

```bash
cd /Users/lukewabro/Documents/WABRO
python3 tools/wabro_hub.py --mode live-osc --eeg-osc-port 5002
```

The hub listens for Muse-style messages on UDP port `5002`, matching the existing `EEG to Midi V2 (.pd` patch.

Useful incoming address endings:

- `jaw_clench`
- `blink`
- `gamma_absolute`
- `beta_absolute`
- `alpha_absolute`
- `theta_absolute`
- `delta_absolute`

## OSC Output Addresses

```text
/wabro/state
/wabro/pressure
/wabro/signal
/wabro/macro/1
/wabro/macro/2
/wabro/macro/3
/wabro/macro/4
/wabro/macro/5
/wabro/macro/6
/wabro/macro/7
/wabro/macro/8
/wabro/macro/snare_fundamental
/wabro/macro/snare_noise
/wabro/macro/snare_transient_bite
/wabro/macro/bass_filter_motion
/wabro/macro/bass_distortion
/wabro/macro/spectral_rotation
/wabro/macro/space_width
/wabro/macro/glitch_fill_probability
```

## Wi-Fi Mode

Only use this when another device or local agent needs to connect over the network:

```bash
python3 tools/wabro_hub.py --mode sim --http-host 0.0.0.0
```

Then another device on the same Wi-Fi can access:

```text
http://YOUR_MAC_IP:8765/state
```

Keep this local/private. Do not expose it to the public internet.

## Manual State Change

```text
http://127.0.0.1:8765/set?state=Signal
http://127.0.0.1:8765/set?state=Pressure
http://127.0.0.1:8765/set?state=Mutation
http://127.0.0.1:8765/set?state=Collapse
```

## First Bitwig Mapping

Map the eight macro values to a Bitwig performance rack:

1. Snare Fundamental
2. Snare Noise
3. Snare Transient Bite
4. Bass Filter Motion
5. Bass Distortion
6. Spectral Rotation
7. Space / Width
8. Glitch / Fill Probability

For the first proof, MIDI CC and OSC can run side by side. OSC is better for TouchDesigner; MIDI CC is safer for quick Bitwig mapping.
