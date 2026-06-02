#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import random
import socket
import struct
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "WABRO_STATE.json"
LOG_PATH = ROOT / "WABRO_LOG.jsonl"
COMMANDS_PATH = ROOT / "WABRO_COMMANDS.jsonl"

MACRO_NAMES = [
    "snare_fundamental",
    "snare_noise",
    "snare_transient_bite",
    "bass_filter_motion",
    "bass_distortion",
    "spectral_rotation",
    "space_width",
    "glitch_fill_probability",
]

SNARE_GEOMETRY_NAMES = [
    "transient",
    "fundamental",
    "harmonic",
    "noise1",
    "noise2",
    "acoustic",
    "mutation_force",
]

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


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def append_jsonl(path: Path, data: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, separators=(",", ":")) + "\n")


def pad_osc_string(value: str) -> bytes:
    raw = value.encode("utf-8") + b"\0"
    return raw + (b"\0" * ((4 - len(raw) % 4) % 4))


def osc_message(address: str, value: float | int | str) -> bytes:
    if isinstance(value, str):
        return pad_osc_string(address) + pad_osc_string(",s") + pad_osc_string(value)
    if isinstance(value, int):
        return pad_osc_string(address) + pad_osc_string(",i") + struct.pack(">i", value)
    return pad_osc_string(address) + pad_osc_string(",f") + struct.pack(">f", float(value))


def read_osc_string(data: bytes, offset: int) -> tuple[str, int]:
    end = data.index(b"\0", offset)
    value = data[offset:end].decode("utf-8", errors="replace")
    offset = end + 1
    offset += (4 - offset % 4) % 4
    return value, offset


def parse_osc_message(data: bytes) -> tuple[str, list[Any]]:
    address, offset = read_osc_string(data, 0)
    tags, offset = read_osc_string(data, offset)
    values: list[Any] = []
    for tag in tags.lstrip(","):
        if tag == "f":
            values.append(struct.unpack(">f", data[offset : offset + 4])[0])
            offset += 4
        elif tag == "i":
            values.append(struct.unpack(">i", data[offset : offset + 4])[0])
            offset += 4
        elif tag == "s":
            value, offset = read_osc_string(data, offset)
            values.append(value)
    return address, values


@dataclass
class HubConfig:
    mode: str
    rate: float
    http_host: str
    http_port: int
    osc_targets: list[tuple[str, int]]
    eeg_osc_host: str
    eeg_osc_port: int
    log_interval: float


@dataclass
class HubState:
    state: str = "Mutation"
    pressure: float = 0.62
    signal: float = 0.31
    current_goal: str = "Build EEG to Bitwig bridge"
    active_project: str = "Backwards V5"
    source: str = "simulator"
    eeg: dict[str, float] = field(default_factory=dict)
    macros: dict[str, float] = field(default_factory=lambda: {name: sum(MACRO_LIMITS[name]) / 2 for name in MACRO_NAMES})
    snare_geometry: dict[str, float] = field(default_factory=lambda: {name: 0.0 for name in SNARE_GEOMETRY_NAMES})
    manual_state: str | None = None
    updated_at: str = field(default_factory=now_iso)

    def as_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.updated_at,
            "state": self.state,
            "pressure": round(self.pressure, 4),
            "signal": round(self.signal, 4),
            "source": self.source,
            "current_goal": self.current_goal,
            "active_project": self.active_project,
            "eeg": {k: round(v, 6) for k, v in sorted(self.eeg.items())},
            "macros": {k: round(v, 4) for k, v in self.macros.items()},
            "snare_geometry": {k: round(v, 4) for k, v in self.snare_geometry.items()},
        }


class WabroHub:
    def __init__(self, config: HubConfig):
        self.config = config
        self.state = HubState(source=config.mode)
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.osc_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.last_log = 0.0
        self.start_time = time.time()
        self.httpd: ThreadingHTTPServer | None = None

    def log(self, event: str, **data: Any) -> None:
        append_jsonl(LOG_PATH, {"event": event, "timestamp": now_iso(), **data})

    def start(self) -> None:
        self.log("hub_started", mode=self.config.mode, http=f"{self.config.http_host}:{self.config.http_port}", osc_targets=self.config.osc_targets)
        threading.Thread(target=self.run_http, daemon=True).start()
        if self.config.mode == "live-osc":
            threading.Thread(target=self.run_eeg_osc_input, daemon=True).start()
        self.run_loop()

    def run_http(self) -> None:
        hub = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                parsed = urlparse(self.path)
                if parsed.path == "/":
                    self.send_json({"name": "WABRO Hub", "endpoints": ["/state", "/health", "/set?state=Signal"]})
                elif parsed.path == "/health":
                    self.send_json({"ok": True, "timestamp": now_iso()})
                elif parsed.path == "/state":
                    with hub.lock:
                        self.send_json(hub.state.as_dict())
                elif parsed.path == "/set":
                    params = parse_qs(parsed.query)
                    state_name = params.get("state", [None])[0]
                    if state_name not in STATE_TARGETS:
                        self.send_json({"ok": False, "error": "state must be Signal, Pressure, Mutation, or Collapse"}, status=400)
                        return
                    with hub.lock:
                        hub.state.manual_state = state_name
                    hub.log("manual_state_set", state=state_name, source="http")
                    append_jsonl(COMMANDS_PATH, {"timestamp": now_iso(), "command": "set_state", "state": state_name, "source": "http"})
                    self.send_json({"ok": True, "state": state_name})
                else:
                    self.send_json({"ok": False, "error": "not found"}, status=404)

            def do_POST(self) -> None:
                if self.path != "/state":
                    self.send_json({"ok": False, "error": "not found"}, status=404)
                    return
                length = int(self.headers.get("content-length", "0"))
                raw = self.rfile.read(length)
                try:
                    payload = json.loads(raw.decode("utf-8"))
                except json.JSONDecodeError as exc:
                    self.send_json({"ok": False, "error": str(exc)}, status=400)
                    return
                with hub.lock:
                    if payload.get("state") in STATE_TARGETS:
                        hub.state.manual_state = payload["state"]
                    for key in ("pressure", "signal"):
                        if key in payload:
                            setattr(hub.state, key, clamp(float(payload[key]), 0.0, 1.0))
                    if "eeg" in payload and isinstance(payload["eeg"], dict):
                        hub.state.eeg.update({str(k): float(v) for k, v in payload["eeg"].items()})
                hub.log("state_posted", payload=payload)
                append_jsonl(COMMANDS_PATH, {"timestamp": now_iso(), "command": "post_state", "payload": payload, "source": "http"})
                self.send_json({"ok": True})

            def log_message(self, format: str, *args: Any) -> None:
                return

            def send_json(self, data: dict[str, Any], status: int = 200) -> None:
                body = json.dumps(data, indent=2).encode("utf-8")
                self.send_response(status)
                self.send_header("content-type", "application/json")
                self.send_header("access-control-allow-origin", "*")
                self.send_header("content-length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

        self.httpd = ThreadingHTTPServer((self.config.http_host, self.config.http_port), Handler)
        self.httpd.serve_forever()

    def run_eeg_osc_input(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.config.eeg_osc_host, self.config.eeg_osc_port))
        sock.settimeout(0.5)
        self.log("eeg_osc_input_started", host=self.config.eeg_osc_host, port=self.config.eeg_osc_port)
        while not self.stop_event.is_set():
            try:
                data, _addr = sock.recvfrom(4096)
            except socket.timeout:
                continue
            try:
                address, values = parse_osc_message(data)
            except Exception as exc:
                self.log("eeg_osc_parse_error", error=str(exc))
                continue
            self.apply_eeg_message(address, values)

    def apply_eeg_message(self, address: str, values: list[Any]) -> None:
        if not values:
            return
        value = values[0]
        if not isinstance(value, (int, float)):
            return
        key = address.strip("/").split("/")[-1]
        key = key.replace("_absolute", "").replace("-", "_")
        with self.lock:
            self.state.eeg[key] = float(value)
            self.state.source = "live-osc"

    def run_loop(self) -> None:
        interval = 1.0 / self.config.rate
        try:
            while not self.stop_event.is_set():
                self.tick()
                time.sleep(interval)
        except KeyboardInterrupt:
            self.stop_event.set()
        finally:
            self.log("hub_stopped")
            if self.httpd is not None:
                self.httpd.shutdown()

    def tick(self) -> None:
        with self.lock:
            if self.config.mode == "sim":
                self.update_simulated_features()
            else:
                self.update_live_features()
            self.update_state_and_macros()
            payload = self.state.as_dict()
        atomic_write_json(STATE_PATH, payload)
        self.broadcast(payload)
        now = time.time()
        if now - self.last_log >= self.config.log_interval:
            append_jsonl(LOG_PATH, {"event": "hub_state", **payload})
            self.last_log = now

    def update_simulated_features(self) -> None:
        elapsed = time.time() - self.start_time
        pressure = clamp(0.5 + 0.38 * math.sin(elapsed * 0.28) + random.uniform(-0.04, 0.04), 0.0, 1.0)
        signal = clamp(1.0 - pressure + random.uniform(-0.05, 0.05), 0.0, 1.0)
        self.state.pressure = smooth(self.state.pressure, pressure, 0.10)
        self.state.signal = smooth(self.state.signal, signal, 0.10)
        self.state.eeg = {
            "alpha": clamp(signal * 0.45 + random.uniform(0.0, 0.06), 0.0, 1.0),
            "beta": clamp(pressure * 0.40 + random.uniform(0.0, 0.08), 0.0, 1.0),
            "gamma": clamp(pressure * 0.30 + random.uniform(0.0, 0.10), 0.0, 1.0),
            "theta": clamp((1.0 - pressure) * 0.25 + random.uniform(0.0, 0.05), 0.0, 1.0),
            "delta": clamp((1.0 - signal) * 0.18 + random.uniform(0.0, 0.04), 0.0, 1.0),
        }

    def update_live_features(self) -> None:
        eeg = self.state.eeg
        alpha = eeg.get("alpha", eeg.get("alpha_absolute", 0.2))
        beta = eeg.get("beta", eeg.get("beta_absolute", 0.2))
        gamma = eeg.get("gamma", eeg.get("gamma_absolute", 0.1))
        theta = eeg.get("theta", eeg.get("theta_absolute", 0.1))
        jaw = eeg.get("jaw_clench", 0.0)
        blink = eeg.get("blink", 0.0)
        pressure_target = clamp((beta * 1.2 + gamma * 1.5 + jaw * 0.2 + blink * 0.1) / 1.8, 0.0, 1.0)
        signal_target = clamp((alpha * 1.4 + theta * 0.5) / 1.2, 0.0, 1.0)
        self.state.pressure = smooth(self.state.pressure, pressure_target, 0.08)
        self.state.signal = smooth(self.state.signal, signal_target, 0.08)

    def update_state_and_macros(self) -> None:
        if self.state.manual_state:
            state_name = self.state.manual_state
        elif self.state.pressure < 0.42 and self.state.signal > 0.48:
            state_name = "Signal"
        elif self.state.pressure > 0.82:
            state_name = "Collapse"
        elif self.state.pressure > 0.58:
            state_name = "Pressure"
        else:
            state_name = "Mutation"
        self.state.state = state_name
        targets = STATE_TARGETS[state_name]
        for name in MACRO_NAMES:
            lo, hi = MACRO_LIMITS[name]
            pressure_bias = (self.state.pressure - 0.5) * 0.08
            target = clamp(targets[name] + pressure_bias, lo, hi)
            self.state.macros[name] = clamp(smooth(self.state.macros[name], target, 0.08), lo, hi)
        self.update_snare_geometry()
        self.state.updated_at = now_iso()

    def eeg_value(self, *keys: str) -> float:
        for key in keys:
            if key in self.state.eeg:
                return clamp(float(self.state.eeg[key]), 0.0, 1.0)
        return 0.0

    def update_snare_geometry(self) -> None:
        macros = self.state.macros
        alpha = self.eeg_value("alpha", "alpha_absolute")
        beta = self.eeg_value("beta", "beta_absolute")
        gamma = self.eeg_value("gamma", "gamma_absolute")
        theta = self.eeg_value("theta", "theta_absolute")
        delta = self.eeg_value("delta", "delta_absolute")
        jaw = self.eeg_value("jaw_clench")
        blink = self.eeg_value("blink")

        targets = {
            "transient": clamp(macros["snare_transient_bite"] * 0.82 + blink * 0.18, 0.0, 1.0),
            "fundamental": clamp(macros["snare_fundamental"] * 0.88 + delta * 0.12, 0.0, 1.0),
            "harmonic": clamp(macros["spectral_rotation"] * 0.55 + beta * 0.30 + macros["snare_fundamental"] * 0.15, 0.0, 1.0),
            "noise1": clamp(macros["snare_noise"] * 0.72 + gamma * 0.28, 0.0, 1.0),
            "noise2": clamp(macros["snare_noise"] * 0.45 + alpha * 0.35 + macros["glitch_fill_probability"] * 0.20, 0.0, 1.0),
            "acoustic": clamp(macros["space_width"] * 0.36 + theta * 0.34 + macros["snare_fundamental"] * 0.30, 0.0, 1.0),
            "mutation_force": clamp(self.state.pressure * 0.45 + macros["glitch_fill_probability"] * 0.30 + jaw * 0.15 + gamma * 0.10, 0.0, 1.0),
        }
        for name, target in targets.items():
            self.state.snare_geometry[name] = smooth(self.state.snare_geometry.get(name, 0.0), target, 0.14)

    def broadcast(self, payload: dict[str, Any]) -> None:
        if not self.config.osc_targets:
            return
        messages: list[tuple[str, float | int | str]] = [
            ("/wabro/state", payload["state"]),
            ("/wabro/pressure", payload["pressure"]),
            ("/wabro/signal", payload["signal"]),
        ]
        for index, name in enumerate(MACRO_NAMES, start=1):
            value = payload["macros"][name]
            messages.append((f"/wabro/macro/{index}", value))
            messages.append((f"/wabro/macro/{name}", value))
        for name in SNARE_GEOMETRY_NAMES:
            messages.append((f"/wabro/snare/{name}", payload["snare_geometry"][name]))
        for host, port in self.config.osc_targets:
            for address, value in messages:
                self.osc_sock.sendto(osc_message(address, value), (host, port))


def parse_targets(raw_targets: list[str]) -> list[tuple[str, int]]:
    targets: list[tuple[str, int]] = []
    for raw in raw_targets:
        if not raw:
            continue
        if ":" not in raw:
            raise ValueError(f"OSC target must look like host:port, got {raw!r}")
        host, port = raw.rsplit(":", 1)
        targets.append((host, int(port)))
    return targets


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the WABRO local state bus, HTTP API, and OSC broadcaster.")
    parser.add_argument("--mode", choices=["sim", "live-osc"], default="sim", help="Use simulated features or listen for Muse OSC.")
    parser.add_argument("--rate", type=float, default=10.0, help="State updates per second.")
    parser.add_argument("--http-host", default="127.0.0.1", help="HTTP API bind host. Use 0.0.0.0 for Wi-Fi access.")
    parser.add_argument("--http-port", type=int, default=8765, help="HTTP API port.")
    parser.add_argument("--osc-target", action="append", default=["127.0.0.1:9000"], help="OSC output target. Repeat for multiple targets.")
    parser.add_argument("--no-osc", action="store_true", help="Disable OSC output.")
    parser.add_argument("--eeg-osc-host", default="0.0.0.0", help="Muse OSC input bind host for live-osc mode.")
    parser.add_argument("--eeg-osc-port", type=int, default=5002, help="Muse OSC input port for live-osc mode.")
    parser.add_argument("--log-interval", type=float, default=5.0, help="Seconds between state log entries.")
    args = parser.parse_args()

    targets = [] if args.no_osc else parse_targets(args.osc_target)
    config = HubConfig(
        mode=args.mode,
        rate=args.rate,
        http_host=args.http_host,
        http_port=args.http_port,
        osc_targets=targets,
        eeg_osc_host=args.eeg_osc_host,
        eeg_osc_port=args.eeg_osc_port,
        log_interval=args.log_interval,
    )
    hub = WabroHub(config)
    print(f"WABRO hub running: mode={args.mode} http=http://{args.http_host}:{args.http_port}/state osc_targets={targets}")
    hub.start()


if __name__ == "__main__":
    main()
