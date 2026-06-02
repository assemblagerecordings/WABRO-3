#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from wabro_hub import WabroHub, HubConfig, parse_targets  # noqa: E402


def main() -> None:
    targets = parse_targets(["127.0.0.1:9000"])
    config = HubConfig(
        mode="sim",
        rate=10.0,
        http_host="127.0.0.1",
        http_port=8000,
        osc_targets=targets,
        eeg_osc_host="0.0.0.0",
        eeg_osc_port=5002,
        log_interval=5.0,
    )
    hub = WabroHub(config)
    print("WABRO state server running: http://localhost:8000/state osc=127.0.0.1:9000")
    print("Use tools/wabro_hub.py --mode live-osc for live Muse input.")
    hub.start()


if __name__ == "__main__":
    main()
