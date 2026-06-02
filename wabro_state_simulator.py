#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import random
import socket
import struct
import time
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "WABRO_STATE.json"
LOG_PATH = ROOT / "WABRO_LOG.jsonl"

MACRO_LIMITS = {
    "snare_fundamental": (0.15, 0.95),
    "snare_noise": (0.05, 0.85),
    "snare_transient_bite": (0.10, 0.80),
    "bass_filter_motion": (0.05, 0.90),
    "bass_distortion": (0.05, 0.70),
    "spectral_rotation": (0.00, 0.85),
    "space_width": (0.10, 0.90),
    "glitch_fill_probability": (0.00, 0.40),
}

STATE_TARGETS = {
    "Signal": {
        "snare_fundamental": 0.82,
        "snare_noise": 0.18,
        "snare_transient_bite": 0.30,
        "bass_filter_motion": 0.24,
        "bass_distortion": 0.20,
        "spectral_rotation": 0.12,
        "space_width": 0.78,
        "glitch_fill_probability": 0.05,
    },
    "Pressure": {
        "snare_fundamental": 0.55,
        "snare_noise": 0.68,
        "snare_transient_bite": 0.66,
        "bass_filter_motion": 0.54,
        "bass_distortion": 0.56,
        "spectral_rotation": 0.34,
        "space_width": 0.46,
        "glitch_fill_probability": 0.22,
    },
    "Mutation": {
        "snare_fundamental": 0.46,
        "snare_noise": 0.58,
        "snare_transient_bite": 0.50,
        "bass_filter_motion": 0.76,
        "bass_distortion": 0.48,
        "spectral_rotation": 0.76,
        "space_width": 0.66,
        "glitch_fill_probability": 0.34,
    },
    "Collapse": {
        "snare_fundamental": 0.28,
        "snare_noise": 0.80,
        "snare_transient_bite": 0.74,
        "bass_filter_motion": 0.84,
        "bass_distortion": 0.70,
        "spectral_rotation": 0.85,
        "space_width": 0.30,
        "glitch_fill_probability": 0.40,
    },
}


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def smooth(previous: float, target: float, amount: float) -> float:
    return previous + (target - previous) * amount


def pad_osc_string(value: str) -> bytes:
    raw = value.encode("utf-8") + b"\0"
    return raw + (b"\0" * ((4 - len(raw) % 4) % 4))


def osc_message(address: str, value: float | int | str) -> bytes:
    if isinstance(value, str):
        return pad_osc_string(address) + pad_osc_string(",s") + pad_osc_string(value)
    if isinstance(value, int):
        return pad_osc_string(address) + pad_osc_string(",i") + struct.pack(">i", value)
    return pad_osc_string(address) + pad_osc_string(",f") + struct.pack(">f", float(value))


def pick_state(t: float) -> str:
    cycle = (math.sin(t * 0.12) + 1.0) / 2.0
    agitation = (math.sin(t * 0.37 + 1.4) + 1.0) / 2.0
    if cycle < 0.25:
        return "Signal"
    if cycle < 0.52:
        return "Pressure"
    if agitation > 0.86:
        return "Collapse"
    return "Mutation"


def write_json(path: Path, data: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def append_log(data: dict) -> None:
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, separators=(",", ":")) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate WABRO EEG state and macro output.")
    parser.add_argument("--duration", type=float, default=60.0, help="Run duration in seconds.")
    parser.add_argument("--rate", type=float, default=10.0, help="Updates per second.")
    parser.add_argument("--osc-host", default="127.0.0.1", help="OSC target host.")
    parser.add_argument("--osc-port", type=int, default=9000, help="OSC target port.")
    parser.add_argument("--no-osc", action="store_true", help="Only write JSON/log; do not send OSC UDP.")
    args = parser.parse_args()

    sock = None if args.no_osc else socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    macros = {name: sum(limit) / 2.0 for name, limit in MACRO_LIMITS.items()}
    start = time.time()
    next_log = 0.0

    while True:
        now = time.time()
        elapsed = now - start
        if elapsed > args.duration:
            break

        state = pick_state(elapsed)
        pressure = clamp(0.5 + 0.38 * math.sin(elapsed * 0.28) + random.uniform(-0.04, 0.04), 0.0, 1.0)
        signal = clamp(1.0 - pressure + random.uniform(-0.05, 0.05), 0.0, 1.0)

        targets = STATE_TARGETS[state]
        for name, target in targets.items():
            lo, hi = MACRO_LIMITS[name]
            noisy_target = clamp(target + random.uniform(-0.03, 0.03), lo, hi)
            macros[name] = clamp(smooth(macros[name], noisy_target, 0.08), lo, hi)

        payload = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "state": state,
            "pressure": round(pressure, 4),
            "signal": round(signal, 4),
            "current_goal": "Build EEG to Bitwig bridge",
            "active_project": "Backwards V5",
            "macros": {name: round(value, 4) for name, value in macros.items()},
        }
        write_json(STATE_PATH, payload)

        if sock is not None:
            sock.sendto(osc_message("/wabro/state", state), (args.osc_host, args.osc_port))
            sock.sendto(osc_message("/wabro/pressure", pressure), (args.osc_host, args.osc_port))
            sock.sendto(osc_message("/wabro/signal", signal), (args.osc_host, args.osc_port))
            for index, (name, value) in enumerate(macros.items(), start=1):
                sock.sendto(osc_message(f"/wabro/macro/{index}", value), (args.osc_host, args.osc_port))
                sock.sendto(osc_message(f"/wabro/macro/{name}", value), (args.osc_host, args.osc_port))

        if elapsed >= next_log:
            append_log({"event": "sim_state", **payload})
            next_log = elapsed + 5.0

        time.sleep(1.0 / args.rate)

    append_log({"event": "simulator_finished", "duration": args.duration})


if __name__ == "__main__":
    main()
