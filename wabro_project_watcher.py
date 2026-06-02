#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "WABRO_INDEX.jsonl"
LOG_PATH = ROOT / "WABRO_LOG.jsonl"
STATE_PATH = ROOT / "WABRO_STATE.json"
GRAPH_JSON_PATH = ROOT / "WABRO_PROJECT_GRAPH.json"
GRAPH_V1_JSON_PATH = ROOT / "WABRO_PROJECT_GRAPH_V1.json"
GRAPH_V2_JSON_PATH = ROOT / "WABRO_PROJECT_GRAPH_V2.json"

WATCH_EXTENSIONS = {
    ".bwproject",
    ".als",
    ".amxd",
    ".maxpat",
    ".pd",
    ".toe",
    ".wav",
    ".aif",
    ".aiff",
    ".mid",
    ".txt",
    ".md",
    ".docx",
    ".rtf",
}

DEFAULT_WATCH_PATHS = [
    Path("/Users/lukewabro/Desktop/WABRO AI"),
    Path("/Users/lukewabro/Documents/WABRO"),
]

PLUGIN_MARKERS = [
    "FabFilter",
    "Serum",
    "Serum2",
    "Superior Drummer",
    "Kontakt",
    "Falcon",
    "Reaktor",
    "Phase Plant",
    "Vital",
    "Melda",
    "MTurboReverb",
    "Ozone",
    "Insight",
    "RX 11",
    "KClip",
    "soothe",
    "Valhalla",
    "Blackhole",
    "Oszillos",
    "MSED",
    "plugdata",
]

VERSION_BY_TRACK = {
    "track_backwards": "version_backwards_v5",
    "track_back_and_fourth": "version_back_and_fourth_v6",
    "track_carnage": "version_carnage_unverified",
    "track_underground": "version_underground_unverified",
    "track_gentle_whisper": "version_gentle_whisper_unverified",
    "track_synchronicity": "version_synchronicity_unverified",
    "track_interpolation": "version_interpolation_v2",
}


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def append_jsonl(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, separators=(",", ":"), ensure_ascii=False) + "\n")


def atomic_json(path: Path, data: dict[str, Any]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def fingerprint(path: Path, stat: Any) -> str:
    import hashlib

    return hashlib.sha256(f"{path}|{stat.st_mtime_ns}|{stat.st_size}".encode("utf-8")).hexdigest()[:24]


def infer_related_work(path: Path) -> str | None:
    lower = str(path).lower().replace("_", " ")
    markers = {
        "gentle whisper": "track_gentle_whisper",
        "carnage": "track_carnage",
        "underground": "track_underground",
        "backwards": "track_backwards",
        "back and fourth": "track_back_and_fourth",
        "synchronicity": "track_synchronicity",
        "interpolation": "track_interpolation",
        "snare": "obj_snare_system",
    }
    for marker, work_id in markers.items():
        if marker in lower:
            return work_id
    return None


def classify_entity(path: Path) -> str:
    lower = str(path).lower()
    ext = path.suffix.lower()
    if ext in {".bwproject", ".als"}:
        return "Version"
    if ext in {".wav", ".aif", ".aiff", ".mp3"}:
        if "stem" in lower or "stems" in lower:
            return "Stem"
        if "sample" in lower or "snare theory" in lower or "/samples/" in lower:
            return "Sample"
        return "Render"
    return "Asset"


def relationship_for_entity(entity_type: str) -> str:
    return {
        "Version": "HAS_VERSION",
        "Render": "GENERATED_RENDER",
        "Stem": "EXPORTS_STEM",
        "Sample": "REFERENCES_SAMPLE",
    }.get(entity_type, "INSTANTIATED_BY")


def extract_plugin_references(path: Path) -> list[str]:
    if path.stat().st_size > 20_000_000:
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    return sorted({marker for marker in PLUGIN_MARKERS if marker.lower() in text.lower()})


def scan_once(paths: list[Path]) -> dict[str, tuple[int, int]]:
    snapshot: dict[str, tuple[int, int]] = {}
    for root in paths:
        if not root.exists():
            continue
        if root.is_file():
            candidates = [root]
        else:
            candidates = [p for p in root.rglob("*") if p.is_file()]
        for path in candidates:
            if path.suffix.lower() not in WATCH_EXTENSIONS:
                continue
            try:
                stat = path.stat()
            except OSError:
                continue
            snapshot[str(path)] = (stat.st_mtime_ns, stat.st_size)
    return snapshot


def update_state(event: dict[str, Any]) -> None:
    if not STATE_PATH.exists():
        return
    try:
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return
    state["last_project_save"] = event
    atomic_json(STATE_PATH, state)


def graph_metadata(event: dict[str, Any]) -> dict[str, str]:
    return {
        "version": "1.0.0",
        "owner": "Luke WABRO",
        "licence": "Creative Commons Attribution",
        "filesystem_root": event["path"],
        "last_checksum_hash": event["fingerprint"],
    }


def update_graph(event: dict[str, Any]) -> None:
    if not GRAPH_JSON_PATH.exists():
        return
    try:
        graph = json.loads(GRAPH_JSON_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return
    nodes = graph.setdefault("graph", {}).setdefault("nodes", [])
    edges = graph.setdefault("graph", {}).setdefault("edges", [])
    node_id = event["id"]
    if not any(node.get("id") == node_id for node in nodes):
        nodes.append(
            {
                "id": node_id,
                "type": event["entity_type"],
                "label": event["basename"],
                "path": event["path"],
                "source": "watcher",
                "metadata": graph_metadata(event),
            }
        )
    watcher_edge = {"source": "script_project_watcher", "target": node_id, "relation": "MONITORS_SAVE_EVENTS"}
    if not any(e.get("source") == watcher_edge["source"] and e.get("target") == watcher_edge["target"] and e.get("relation") == watcher_edge["relation"] for e in edges):
        edges.append(watcher_edge)
    related = event.get("related_work")
    if related:
        relation_source = related
        if event["entity_type"] in {"Render", "Stem", "Sample"}:
            relation_source = event.get("related_version") or related
        edge = {"source": relation_source, "target": node_id, "relation": event["graph_relation"]}
        if not any(e.get("source") == edge["source"] and e.get("target") == edge["target"] and e.get("relation") == edge["relation"] for e in edges):
            edges.append(edge)
    atomic_json(GRAPH_JSON_PATH, graph)
    atomic_json(GRAPH_V1_JSON_PATH, graph)
    atomic_json(GRAPH_V2_JSON_PATH, graph)


def handle_change(path_text: str, change_type: str) -> None:
    path = Path(path_text)
    try:
        stat = path.stat()
    except OSError:
        return
    event = {
        "id": f"save_{fingerprint(path, stat)}",
        "event": "project_save_detected",
        "timestamp": now_iso(),
        "change_type": change_type,
        "path": str(path),
        "basename": path.name,
        "extension": path.suffix.lower(),
        "size_bytes": stat.st_size,
        "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
        "fingerprint": fingerprint(path, stat),
        "related_work": infer_related_work(path),
        "entity_type": classify_entity(path),
        "graph_relation": relationship_for_entity(classify_entity(path)),
        "plugin_references": extract_plugin_references(path),
    }
    event["related_version"] = VERSION_BY_TRACK.get(event["related_work"] or "")
    append_jsonl(LOG_PATH, event)
    append_jsonl(INDEX_PATH, {**event, "category": "watched_project_save", "confidence": "watcher_event"})
    update_graph(event)
    update_state(event)
    print(json.dumps(event, indent=2))


def watch(paths: list[Path], interval: float) -> None:
    print("WABRO watcher starting")
    print("Watching:")
    for path in paths:
        print(f"  {path}")
    previous = scan_once(paths)
    print(f"Initial watched files: {len(previous)}")
    while True:
        time.sleep(interval)
        current = scan_once(paths)
        for path, value in current.items():
            if path not in previous:
                handle_change(path, "created")
            elif previous[path] != value:
                handle_change(path, "modified")
        previous = current


def main() -> None:
    parser = argparse.ArgumentParser(description="Poll watched WABRO folders and log project save events.")
    parser.add_argument("--watch", action="append", default=[], help="Folder or file to watch. Repeatable.")
    parser.add_argument("--interval", type=float, default=5.0, help="Polling interval in seconds.")
    parser.add_argument("--once", action="store_true", help="Scan once and print watched file count.")
    args = parser.parse_args()

    paths = [Path(p).expanduser() for p in args.watch] if args.watch else DEFAULT_WATCH_PATHS
    if args.once:
        snapshot = scan_once(paths)
        print(json.dumps({"watched_files": len(snapshot), "paths": [str(p) for p in paths]}, indent=2))
        return
    watch(paths, args.interval)


if __name__ == "__main__":
    main()
