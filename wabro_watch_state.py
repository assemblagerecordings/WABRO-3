#!/usr/bin/env python3
from __future__ import annotations

import json
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "WABRO_STATE.json"


def main() -> None:
    last = None
    print(f"Watching {STATE_PATH}")
    while True:
        try:
            text = STATE_PATH.read_text(encoding="utf-8")
            if text != last:
                last = text
                state = json.loads(text)
                macros = state.get("macros", {})
                print(
                    f"{state.get('timestamp')} state={state.get('state')} "
                    f"pressure={state.get('pressure')} signal={state.get('signal')} "
                    f"snare_noise={macros.get('snare_noise')} spectral={macros.get('spectral_rotation')}"
                )
        except Exception as exc:
            print(f"watch error: {exc}")
        time.sleep(0.5)


if __name__ == "__main__":
    main()
