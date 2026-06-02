#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
SCANS_DIR = ROOT / "Scans"
INDEX_PATH = ROOT / "WABRO_INDEX.jsonl"
GRAPH_JSON_PATH = ROOT / "WABRO_PROJECT_GRAPH.json"
GRAPH_V1_JSON_PATH = ROOT / "WABRO_PROJECT_GRAPH_V1.json"
GRAPH_V2_JSON_PATH = ROOT / "WABRO_PROJECT_GRAPH_V2.json"
GRAPH_MD_PATH = ROOT / "WABRO_PROJECT_GRAPH.md"
GRAMMAR_MD_PATH = ROOT / "WABRO_GRAMMAR_V1.md"
GRAMMAR_V2_MD_PATH = ROOT / "WABRO_GRAMMAR_V2.md"
ONTOLOGY_V2_MD_PATH = ROOT / "WABRO_CORE_ONTOLOGY_V2.md"
LOG_PATH = ROOT / "WABRO_LOG.jsonl"
STATE_PATH = ROOT / "WABRO_STATE.json"
DEFAULT_PLUGIN_LIST = Path("/Users/lukewabro/Desktop/plugins.txt")
DEFAULT_OWNER = "Luke WABRO"
DEFAULT_LICENCE = "Creative Commons Attribution"

PROJECT_EXTENSIONS = {
    ".bwproject",
    ".als",
    ".amxd",
    ".maxpat",
    ".pd",
    ".toe",
    ".blend",
}

CREATIVE_EXTENSIONS = {
    ".wav",
    ".aif",
    ".aiff",
    ".mp3",
    ".mid",
    ".midi",
    ".bwpreset",
    ".bwclip",
    ".nki",
    ".fxp",
    ".zip",
    ".txt",
    ".md",
    ".docx",
    ".rtf",
    ".rtfd",
}

PRIORITY_WORKS = {
    "gentle whisper": "track_gentle_whisper",
    "carnage": "track_carnage",
    "underground": "track_underground",
    "backwards": "track_backwards",
    "back and fourth": "track_back_and_fourth",
    "backandfourth": "track_back_and_fourth",
    "synchronicity": "track_synchronicity",
    "interpolation": "track_interpolation",
    "snare": "obj_snare_system",
}

KEYWORDS = [
    "wabro",
    "assemblage",
    "backwards",
    "gentle whisper",
    "carnage",
    "underground",
    "back and fourth",
    "synchronicity",
    "interpolation",
    "snare",
    "eeg",
    "muse",
    "bitwig",
    "ableton",
    "touchdesigner",
    "plugdata",
    "osc",
    "fft",
    "spectral",
    "max",
]


@dataclass
class ScanRow:
    modified: str
    size_bytes: int
    ext: str
    path: str
    source: str


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def append_jsonl(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, separators=(",", ":"), ensure_ascii=False) + "\n")


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def stable_id(*parts: str) -> str:
    digest = hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"idx_{digest}"


def fingerprint_for_path(path: str, modified: str = "", size_bytes: int = 0) -> str:
    return hashlib.sha256(f"{path}|{modified}|{size_bytes}".encode("utf-8")).hexdigest()[:24]


def state_hash_for_target(path_value: str) -> str:
    if path_value in {"", "N/A", "NONE", "DYNAMIC", "DISCOVERY_REQUIRED", "ALGORITHMIC_DERIVATIVE"}:
        return path_value or "NONE"
    path = Path(path_value)
    if path.is_dir():
        return "DIR_NODE"
    if path.exists():
        stat = path.stat()
        return fingerprint_for_path(str(path), str(int(stat.st_mtime)), stat.st_size)
    return "DISCOVERY_REQUIRED"


def metadata(
    *,
    version: str = "1.0.0",
    owner: str = DEFAULT_OWNER,
    licence: str = DEFAULT_LICENCE,
    filesystem_root: str = "N/A",
    last_checksum_hash: str | None = None,
) -> dict[str, str]:
    return {
        "version": version,
        "owner": owner,
        "licence": licence,
        "filesystem_root": filesystem_root,
        "last_checksum_hash": last_checksum_hash or state_hash_for_target(filesystem_root),
    }


def ensure_node_metadata(node: dict[str, Any]) -> dict[str, Any]:
    node.setdefault(
        "metadata",
        metadata(
            filesystem_root=node.get("path", "N/A"),
            licence="Private" if node.get("type") in {"FileState", "IndexedAsset"} else DEFAULT_LICENCE,
        ),
    )
    return node


def clean_ext(value: str) -> str:
    if value == "[no extension]":
        return ""
    return value.lower()


def infer_category(path: str, ext: str) -> str:
    lower = path.lower()
    if ext in PROJECT_EXTENSIONS:
        return "project_file"
    if "final project - signals" in lower or "release" in lower or ext in {".wav", ".aif", ".aiff", ".mp3"}:
        return "audio_render_or_sample"
    if "uni" in lower or "essay" in lower or "research" in lower:
        return "university_research"
    if "chat" in lower or "gpt" in lower or "ai" in lower:
        return "ai_context"
    if "touchdesigner" in lower or ext == ".toe":
        return "visual_system"
    if "plugin" in lower or "vst" in lower:
        return "plugin_or_library"
    if ext in CREATIVE_EXTENSIONS:
        return "creative_asset"
    return "archive_file"


def extract_keywords(path: str) -> list[str]:
    lower = path.lower()
    return [keyword for keyword in KEYWORDS if keyword in lower]


def related_work_for(path: str) -> str | None:
    lower = path.lower().replace("_", " ")
    for marker, work_id in PRIORITY_WORKS.items():
        if marker in lower:
            return work_id
    return None


def read_scan_table(path: Path, source: str, limit: int | None = None) -> Iterable[ScanRow]:
    if not path.exists():
        return []
    rows: list[ScanRow] = []
    with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            try:
                size = int(row.get("size_bytes") or 0)
            except ValueError:
                size = 0
            rows.append(
                ScanRow(
                    modified=row.get("modified", ""),
                    size_bytes=size,
                    ext=clean_ext(row.get("ext", "")),
                    path=row.get("path", ""),
                    source=source,
                )
            )
            if limit is not None and len(rows) >= limit:
                break
    return rows


def plugin_names(plugin_list: Path) -> list[str]:
    if not plugin_list.exists():
        return []
    names: list[str] = []
    for line in plugin_list.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip().endswith(".vst3"):
            continue
        names.append(Path(line.strip()).name.removesuffix(".vst3"))
    return sorted(set(names), key=str.lower)


def make_record(row: ScanRow) -> dict[str, Any]:
    ext = row.ext or Path(row.path).suffix.lower()
    return {
        "id": stable_id(row.path),
        "indexed_at": now_iso(),
        "path": row.path,
        "basename": Path(row.path).name,
        "extension": ext,
        "modified_time": row.modified,
        "size_bytes": row.size_bytes,
        "category": infer_category(row.path, ext),
        "keywords": extract_keywords(row.path),
        "related_work": related_work_for(row.path),
        "fingerprint": fingerprint_for_path(row.path, row.modified, row.size_bytes),
        "source_scan": row.source,
        "confidence": "scan_metadata",
    }


def priority_score(record: dict[str, Any]) -> int:
    score = 0
    if record["related_work"]:
        score += 100
    if record["extension"] in PROJECT_EXTENSIONS:
        score += 50
    if record["category"] in {"visual_system", "university_research", "ai_context"}:
        score += 20
    score += min(len(record["keywords"]) * 5, 30)
    return score


def load_graph() -> dict[str, Any]:
    if GRAPH_JSON_PATH.exists():
        return json.loads(GRAPH_JSON_PATH.read_text(encoding="utf-8"))
    return {"graph": {"nodes": [], "edges": []}}


def preserved_watched_graph_items() -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    try:
        graph = load_graph()
    except json.JSONDecodeError:
        return [], []
    nodes = graph.get("graph", {}).get("nodes", [])
    edges = graph.get("graph", {}).get("edges", [])
    watched_ids = {
        node.get("id")
        for node in nodes
        if node.get("source") == "watcher" and node.get("type") in {"Version", "Render", "Stem", "Sample", "Asset"}
    }
    watched_nodes = [node for node in nodes if node.get("id") in watched_ids]
    watched_edges = [
        edge
        for edge in edges
        if edge.get("source") in watched_ids or edge.get("target") in watched_ids
    ]
    return watched_nodes, watched_edges


def ensure_graph_schema(graph: dict[str, Any]) -> None:
    graph["graph_schema"] = {
        "version": "2.0.0",
        "updated": "2026-06-02",
        "ontology": "WABRO Knowledge Architecture V2",
        "metadata_standard": {
            "required_fields": ["id", "type", "label", "metadata"],
            "core_entity_types": [
                "Track",
                "Version",
                "Render",
                "Stem",
                "Sample",
                "PluginChain",
                "MacroMapping",
                "EEGMapping",
                "VisualMapping",
                "Hardware",
                "CoreScript",
                "DataStream",
                "Software",
                "FileState",
                "CreativeObject",
                "SnareLayer",
                "Asset",
            ],
            "metadata_schema": {
                "version": "string",
                "owner": "string",
                "licence": "string",
                "filesystem_root": "string",
                "last_checksum_hash": "string",
            },
        },
    }


def upsert_node(graph: dict[str, Any], node: dict[str, Any]) -> None:
    node = ensure_node_metadata(node)
    nodes = graph.setdefault("graph", {}).setdefault("nodes", [])
    for existing in nodes:
        if existing.get("id") == node["id"]:
            existing.update(node)
            return
    nodes.append(node)


def upsert_edge(graph: dict[str, Any], edge: dict[str, str]) -> None:
    edges = graph.setdefault("graph", {}).setdefault("edges", [])
    key = (edge["source"], edge["target"], edge["relation"])
    for existing in edges:
        if (existing.get("source"), existing.get("target"), existing.get("relation")) == key:
            existing.update(edge)
            return
    edges.append(edge)


def update_graph(_records: list[dict[str, Any]]) -> None:
    watched_nodes, watched_edges = preserved_watched_graph_items()
    graph: dict[str, Any] = {"graph": {"nodes": [], "edges": []}}
    ensure_graph_schema(graph)
    seed_canonical_graph(graph)
    for node in watched_nodes:
        upsert_node(graph, node)
    for edge in watched_edges:
        upsert_edge(graph, edge)

    atomic_write(GRAPH_JSON_PATH, json.dumps(graph, indent=2, ensure_ascii=False) + "\n")
    atomic_write(GRAPH_V1_JSON_PATH, json.dumps(graph, indent=2, ensure_ascii=False) + "\n")
    atomic_write(GRAPH_V2_JSON_PATH, json.dumps(graph, indent=2, ensure_ascii=False) + "\n")
    write_graph_md(graph)
    write_grammar_md()
    write_ontology_v2_md()
    write_grammar_v2_md()


def seed_canonical_graph(graph: dict[str, Any]) -> None:
    canonical_nodes = [
        {"id": "project_wabro", "type": "Project", "label": "WABRO Ecosystem", "metadata": metadata(filesystem_root=str(ROOT))},
        {"id": "layer_1_instrument", "type": "ArchitectureLayer", "label": "Layer 1 - WABRO Instrument", "metadata": metadata(filesystem_root="N/A")},
        {"id": "layer_2_graph", "type": "ArchitectureLayer", "label": "Layer 2 - WABRO Knowledge Graph", "metadata": metadata(filesystem_root="N/A")},
        {"id": "layer_3_platform", "type": "ArchitectureLayer", "label": "Layer 3 - Platform", "metadata": metadata(licence="Proprietary", filesystem_root="N/A")},
        {"id": "track_backwards", "type": "Track", "label": "Backwards", "metadata": metadata(filesystem_root="N/A")},
        {"id": "track_back_and_fourth", "type": "Track", "label": "Back And Fourth", "metadata": metadata(owner="Luke WABRO & Rithy", filesystem_root="N/A")},
        {"id": "track_carnage", "type": "Track", "label": "Carnage", "metadata": metadata(filesystem_root="N/A")},
        {"id": "track_underground", "type": "Track", "label": "Underground", "metadata": metadata(filesystem_root="N/A")},
        {"id": "track_gentle_whisper", "type": "Track", "label": "Gentle Whisper", "metadata": metadata(filesystem_root="N/A")},
        {"id": "track_synchronicity", "type": "Track", "label": "Synchronicity", "metadata": metadata(filesystem_root="N/A")},
        {"id": "track_interpolation", "type": "Track", "label": "Interpolation", "metadata": metadata(filesystem_root="N/A")},
        {"id": "version_backwards_v5", "type": "Version", "label": "Backwards V5", "metadata": metadata(version="5.0.0", filesystem_root="/Volumes/Luke backups/Music Projects/Music/Backwards/Wabro - Backwards V5.bwproject")},
        {"id": "version_back_and_fourth_v6", "type": "Version", "label": "Back And Fourth V6", "metadata": metadata(version="6.0.0", owner="Luke WABRO & Rithy", filesystem_root="/Volumes/Luke backups/Music Projects/Music/Wabro & Rithy - Back And Fourth (V6)")},
        {"id": "version_carnage_unverified", "type": "Version", "label": "Carnage Version - Discovery Required", "metadata": metadata(filesystem_root="DISCOVERY_REQUIRED")},
        {"id": "version_underground_unverified", "type": "Version", "label": "Underground Version - Discovery Required", "metadata": metadata(filesystem_root="DISCOVERY_REQUIRED")},
        {"id": "version_gentle_whisper_unverified", "type": "Version", "label": "Gentle Whisper Version - Discovery Required", "metadata": metadata(filesystem_root="DISCOVERY_REQUIRED")},
        {"id": "version_synchronicity_unverified", "type": "Version", "label": "Synchronicity Version - Discovery Required", "metadata": metadata(filesystem_root="DISCOVERY_REQUIRED")},
        {"id": "version_interpolation_v2", "type": "Version", "label": "Interpolation V2", "metadata": metadata(filesystem_root="/Users/lukewabro/Desktop/WABRO AI/The Analysis of Interpolation V2.docx")},
        {"id": "render_carnage_sf_v2", "type": "Render", "label": "Carnage sf v2 Render", "metadata": metadata(filesystem_root="/Users/lukewabro/Desktop/WABRO AI/4 Harry/1 WABRO - Carnage (sf v2) 24 44100.wav")},
        {"id": "render_underground_sf_v2", "type": "Render", "label": "Underground sf v2 Render", "metadata": metadata(filesystem_root="/Users/lukewabro/Desktop/WABRO AI/4 Harry/3 WABRO - Underground (sf v2) 24 44100.wav")},
        {"id": "render_gentle_whisper_sf_v5", "type": "Render", "label": "Gentle Whisper sf v5 Render", "metadata": metadata(filesystem_root="/Users/lukewabro/Desktop/WABRO AI/4 Harry/2 WABRO - Gentle Whisper (Feat. Ziza Muftic) (sf v5) 24 44100.wav")},
        {"id": "macro_mapping_demo_0_1", "type": "MacroMapping", "label": "Demo 0.1 Eight Macro Mapping", "metadata": metadata(filesystem_root=str(ROOT / "WABRO_MACROS.md"))},
        {"id": "eeg_mapping_muse2_to_hub", "type": "EEGMapping", "label": "Muse 2 to wabro_hub Mapping", "metadata": metadata(filesystem_root=str(ROOT / "tools" / "wabro_hub.py"))},
        {"id": "visual_mapping_snare_geometry", "type": "VisualMapping", "label": "Snare Geometry State Visualiser", "metadata": metadata(filesystem_root=str(ROOT / "dashboard" / "index.html"))},
        {"id": "hw_muse2", "type": "Hardware", "label": "Muse 2 EEG Headset", "metadata": metadata(version="Hardware_v2", licence="Commercial", filesystem_root="N/A")},
        {"id": "script_hub", "type": "CoreScript", "label": "wabro_hub.py", "metadata": metadata(version="0.1.0", licence="MIT", filesystem_root=str(ROOT / "tools" / "wabro_hub.py"))},
        {"id": "script_project_indexer", "type": "CoreScript", "label": "wabro_project_indexer.py", "metadata": metadata(version="0.1.0", licence="MIT", filesystem_root=str(ROOT / "tools" / "wabro_project_indexer.py"))},
        {"id": "script_project_watcher", "type": "CoreScript", "label": "wabro_project_watcher.py", "metadata": metadata(version="0.1.0", licence="MIT", filesystem_root=str(ROOT / "tools" / "wabro_project_watcher.py"))},
        {"id": "sw_bitwig", "type": "Software", "label": "Bitwig Studio", "metadata": metadata(owner="Commercial", licence="Proprietary", filesystem_root="/Applications/Bitwig Studio.app")},
        {"id": "sw_touchdesigner", "type": "Software", "label": "TouchDesigner", "metadata": metadata(owner="Commercial", licence="Proprietary", filesystem_root="/Applications/TouchDesigner.app")},
        {"id": "file_state", "type": "FileState", "label": "WABRO_STATE.json", "metadata": metadata(licence="Private", filesystem_root=str(ROOT / "WABRO_STATE.json"), last_checksum_hash="DYNAMIC")},
        {"id": "data_macro_values", "type": "DataStream", "label": "8 OSC Macro Values", "metadata": metadata(filesystem_root="N/A")},
        {"id": "obj_snare_system", "type": "CreativeObject", "label": "WABRO Snare System", "metadata": metadata(version="20 Year Baseline", filesystem_root="/Users/lukewabro/Desktop/WABRO AI/Snare Theory")},
        {"id": "snare_fundamental", "type": "SnareLayer", "label": "Fundamental Layer", "metadata": metadata(filesystem_root="/Users/lukewabro/Desktop/WABRO AI/Snare Theory/Fundamental.wav")},
        {"id": "snare_harmonic", "type": "SnareLayer", "label": "Harmonic Layer", "metadata": metadata(filesystem_root="/Users/lukewabro/Desktop/WABRO AI/Snare Theory/Harmonic.wav")},
        {"id": "snare_noise_1", "type": "SnareLayer", "label": "Noise Layer 1", "metadata": metadata(filesystem_root="/Users/lukewabro/Desktop/WABRO AI/Snare Theory/Noise.wav")},
        {"id": "snare_noise_2", "type": "SnareLayer", "label": "Noise Layer 2", "metadata": metadata(filesystem_root="/Users/lukewabro/Desktop/WABRO AI/Snare Theory/Noise 2.wav")},
        {"id": "snare_acoustic", "type": "SnareLayer", "label": "Acoustic Layer", "metadata": metadata(filesystem_root="/Users/lukewabro/Desktop/WABRO AI/Snare Theory/Acoustic Snare.wav")},
        {"id": "snare_transient", "type": "SnareLayer", "label": "Transient Layer", "metadata": metadata(filesystem_root="ALGORITHMIC_DERIVATIVE")},
        {"id": "asset_dir_projects", "type": "Asset", "label": "Music Projects Archive", "metadata": metadata(filesystem_root="/Volumes/Luke backups/Music Projects/Music/")},
        {"id": "asset_dir_uni", "type": "Asset", "label": "University Research Papers", "metadata": metadata(licence="Private", filesystem_root="/Users/lukewabro/Desktop/uni essays/year 3/y 3 files")},
        {"id": "asset_file_chats", "type": "Asset", "label": "WABRO_MASTER_TEXT_FOR_CHATGPT.txt", "metadata": metadata(licence="Private", filesystem_root="/Users/lukewabro/Desktop/WABRO AI/WABRO_FULL_PROJECT_EXPORT/WABRO_MASTER_TEXT_FOR_CHATGPT.txt")},
        {"id": "asset_file_plugins", "type": "Asset", "label": "plugins.txt Ledger Base", "metadata": metadata(licence="Private", filesystem_root=str(DEFAULT_PLUGIN_LIST))},
    ]
    canonical_edges = [
        ("project_wabro", "layer_1_instrument", "STRATEGIC_PRIORITY_FIRST"),
        ("layer_1_instrument", "layer_2_graph", "PRE_REQUISITE_FOR"),
        ("layer_2_graph", "layer_3_platform", "PRE_REQUISITE_FOR"),
        ("hw_muse2", "script_hub", "PROVIDES_RAW_TELEMETRY"),
        ("script_hub", "data_macro_values", "COMPUTES_AND_OUTPUTS"),
        ("script_hub", "sw_bitwig", "DRIVES_MACROS_VIA_OSC"),
        ("script_hub", "sw_touchdesigner", "MUTATES_GEOMETRY_VIA_OSC"),
        ("data_macro_values", "sw_bitwig", "DRIVES_MACROS_VIA_OSC"),
        ("data_macro_values", "sw_touchdesigner", "MUTATES_GEOMETRY_VIA_OSC"),
        ("script_hub", "file_state", "RECORDS_STATE_INTO"),
        ("script_project_watcher", "file_state", "AUTOMATICALLY_UPDATES"),
        ("script_project_watcher", "asset_dir_projects", "MONITORS_SAVE_EVENTS"),
        ("track_backwards", "layer_1_instrument", "SERVES_AS_INITIAL_MUTATION_TARGET"),
        ("track_backwards", "version_backwards_v5", "HAS_VERSION"),
        ("track_back_and_fourth", "version_back_and_fourth_v6", "HAS_VERSION"),
        ("track_carnage", "version_carnage_unverified", "HAS_VERSION"),
        ("track_underground", "version_underground_unverified", "HAS_VERSION"),
        ("track_gentle_whisper", "version_gentle_whisper_unverified", "HAS_VERSION"),
        ("track_synchronicity", "version_synchronicity_unverified", "HAS_VERSION"),
        ("track_interpolation", "version_interpolation_v2", "HAS_VERSION"),
        ("version_carnage_unverified", "render_carnage_sf_v2", "GENERATED_RENDER"),
        ("version_underground_unverified", "render_underground_sf_v2", "GENERATED_RENDER"),
        ("version_gentle_whisper_unverified", "render_gentle_whisper_sf_v5", "GENERATED_RENDER"),
        ("version_backwards_v5", "macro_mapping_demo_0_1", "BINDS_MACRO"),
        ("eeg_mapping_muse2_to_hub", "macro_mapping_demo_0_1", "DRIVES_STREAM"),
        ("macro_mapping_demo_0_1", "visual_mapping_snare_geometry", "MUTATES_GEOMETRY"),
        ("version_backwards_v5", "asset_dir_projects", "INSTANTIATED_BY"),
        ("version_back_and_fourth_v6", "asset_dir_projects", "INSTANTIATED_BY"),
        ("version_interpolation_v2", "asset_dir_uni", "INSTANTIATED_BY"),
        ("obj_snare_system", "snare_fundamental", "CONTAINS_SUB_ELEMENT"),
        ("obj_snare_system", "snare_harmonic", "CONTAINS_SUB_ELEMENT"),
        ("obj_snare_system", "snare_noise_1", "CONTAINS_SUB_ELEMENT"),
        ("obj_snare_system", "snare_noise_2", "CONTAINS_SUB_ELEMENT"),
        ("obj_snare_system", "snare_acoustic", "CONTAINS_SUB_ELEMENT"),
        ("obj_snare_system", "snare_transient", "CONTAINS_SUB_ELEMENT"),
        ("data_macro_values", "obj_snare_system", "MODULATES"),
        ("asset_dir_uni", "version_interpolation_v2", "CONTAINS_THEORETICAL_SPEC_FOR"),
        ("asset_file_chats", "layer_2_graph", "MINED_INTO_MEMORY_BY"),
        ("asset_file_plugins", "sw_bitwig", "PROFILES_CAPABILITY_OF"),
    ]
    for node in canonical_nodes:
        upsert_node(graph, node)
    for source, target, relation in canonical_edges:
        upsert_edge(graph, {"source": source, "target": target, "relation": relation})


def write_graph_md(graph: dict[str, Any]) -> None:
    nodes = graph.get("graph", {}).get("nodes", [])
    edges = graph.get("graph", {}).get("edges", [])
    by_type: dict[str, int] = {}
    for node in nodes:
        by_type[node.get("type", "Unknown")] = by_type.get(node.get("type", "Unknown"), 0) + 1
    lines = [
        "# WABRO Project Graph",
        "",
        f"Updated: {now_iso()}",
        "",
        "## Summary",
        "",
        f"- Nodes: {len(nodes)}",
        f"- Edges: {len(edges)}",
        "",
        "## Node Types",
        "",
    ]
    for node_type, count in sorted(by_type.items()):
        lines.append(f"- {node_type}: {count}")
    lines.extend(["", "## Demo 0.1 Links", ""])
    for edge in edges:
        if edge.get("relation") in {"PRE_REQUISITE_FOR", "PROVIDES_RAW_TELEMETRY", "DRIVES_MACROS_VIA_OSC", "RECORDS_STATE_INTO", "CONTAINS_SUB_ELEMENT", "INSTANTIATED_BY", "SERVES_AS_INITIAL_MUTATION_TARGET", "HAS_VERSION", "GENERATED_RENDER", "BINDS_MACRO", "DRIVES_STREAM", "MUTATES_GEOMETRY"}:
            lines.append(f"- `{edge['source']}` -> `{edge['target']}` ({edge['relation']})")
    atomic_write(GRAPH_MD_PATH, "\n".join(lines) + "\n")


def write_grammar_md() -> None:
    lines = [
        "# WABRO GRAMMAR PROTOCOL v1.0",
        "",
        "Machine-readable intent vectors for the Layer 1 WABRO instrument: neurofunk architecture, EEG control, Bitwig macro routing, snare geometry, and persistent state.",
        "",
        "## Production Grammar",
        "",
        "- Mutation target constraint: Backwards V5 is treated as the first open-system DNA template, not a fixed track.",
        "- Eight-macro bus: external telemetry is normalized into exactly eight macro values before touching Bitwig, visuals, or state.",
        "- File-level ledger hook: project saves are indexed through filesystem metadata, plugin references, fingerprints, graph updates, state updates, and log events.",
        "",
        "## Canonical Macro Bus",
        "",
        "| Macro | Current WABRO Name | Role |",
        "| --- | --- | --- |",
        "| 1 | snare_fundamental | Snare body, central polygon scale, low-frequency anchor |",
        "| 2 | snare_noise | High-frequency noise layer, outer particle density |",
        "| 3 | snare_transient_bite | Attack flash, transient edge, visual luminance spike |",
        "| 4 | bass_filter_motion | Bass filter movement and body-density pressure |",
        "| 5 | bass_distortion | Saturation, clipping intensity, internal pressure |",
        "| 6 | spectral_rotation | FFT/spectral mutation, geometric rotation force |",
        "| 7 | space_width | Width, spatial bloom, ring spread |",
        "| 8 | glitch_fill_probability | Fill chance, interruption, mutation probability |",
        "",
        "## Snare Ontology",
        "",
        "- Transient layer: initial attack spike; controls global flash and sharpness.",
        "- Fundamental layer: center-frequency body; controls central polygon side count and scale.",
        "- Harmonic layer: overtone structure; controls orbiting rings and secondary geometry.",
        "- Noise layer 1: bright texture; controls outer particle halo density and velocity.",
        "- Noise layer 2: diffuse granular texture; controls inner cloud and surface instability.",
        "- Acoustic layer: physical shell resonance; controls wireframe shell, thickness, and deformation.",
        "",
        "## Neurofunk Bass Ontology",
        "",
        "- Wavetable phase tracking: bass motion is treated as stateful movement rather than a static riff.",
        "- Resampling loops: distortion and clipping intensity can rise with pressure while filter movement remains bounded.",
        "- Sub-bass split: material below 90 Hz should remain mono and protected from width modulation.",
        "",
        "## Visual Grammar",
        "",
        "- Anti-oscilloscope mandate: the visualiser shows system state, not a literal waveform display.",
        "- Geometric organisms: particles, rings, shells, and polygon cores act as reactive life-form structures.",
        "- Biological interruption maps: EEG pressure and mutation states destabilize symmetry and density.",
        "",
        "## Biological Routing",
        "",
        "- Muse 2 or simulator enters `wabro_hub.py` as raw features.",
        "- `wabro_hub.py` computes normalized macro values.",
        "- The same macro values drive Bitwig, the dashboard/snare visualiser, OSC subscribers, and `WABRO_STATE.json`.",
        "",
        "## Lifecycle Constraint",
        "",
        "Layer 1 comes first. Do not build the social platform until the living creative instrument is reliable.",
    ]
    atomic_write(GRAMMAR_MD_PATH, "\n".join(lines) + "\n")


def write_ontology_v2_md() -> None:
    lines = [
        "# WABRO Core Ontology V2",
        "",
        "This is the lightweight ontology used by the Demo 0.1 graph, watcher, and future mutation engine. It is deliberately small: the full archive belongs in `WABRO_INDEX.jsonl`; the graph tracks only the entities needed to make the instrument work.",
        "",
        "## Entities",
        "",
        "- Track: stable identity of a musical work across versions.",
        "- Version: specific save-state or project iteration, such as a `.bwproject` or `.als` file.",
        "- Render: full bounce/export of a Version.",
        "- Stem: bounced subgroup or isolated layer from a Version.",
        "- Sample: discrete audio component used by a Version.",
        "- PluginChain: ordered software signal path used inside a Version.",
        "- MacroMapping: binding between real-time input slots and host/software controls.",
        "- EEGMapping: rule mapping Muse/brainwave telemetry to macro streams.",
        "- VisualMapping: rule mapping macro streams to geometry, space, and lighting.",
        "",
        "## Relationships",
        "",
        "- HAS_VERSION: Track -> Version.",
        "- GENERATED_RENDER: Version -> Render.",
        "- EXPORTS_STEM: Version -> Stem.",
        "- REFERENCES_SAMPLE: Version -> Sample.",
        "- INSTANTIATES_CHAIN: Version -> PluginChain.",
        "- BINDS_MACRO: Version -> MacroMapping.",
        "- DRIVES_STREAM: EEGMapping -> MacroMapping.",
        "- MUTATES_GEOMETRY: MacroMapping -> VisualMapping.",
        "- INSTANTIATED_BY: Version/Render/Stem/Sample -> Asset.",
        "",
        "## Integrity Rule",
        "",
        "Use `DISCOVERY_REQUIRED` for unverified paths or versions. Do not invent project paths, chain contents, or sample links before the watcher or indexer has observed them.",
    ]
    atomic_write(ONTOLOGY_V2_MD_PATH, "\n".join(lines) + "\n")


def write_grammar_v2_md() -> None:
    lines = [
        "# WABRO Grammar V2",
        "",
        "Demo 0.1 grammar for the living creative instrument.",
        "",
        "## Approved Visual Principle",
        "",
        "Anti-oscilloscope: build a state visualiser / geometric organism. Do not build a waveform viewer.",
        "",
        "## Demo 0.1 Flow",
        "",
        "Backwards V5 + Muse 2 + 8 macros + snare geometry + persistent state.",
        "",
        "```text",
        "Muse 2 or simulator",
        "  -> wabro_hub.py",
        "  -> MacroMapping: Demo 0.1 Eight Macro Mapping",
        "  -> Bitwig + TouchDesigner/dashboard + WABRO_STATE.json",
        "```",
        "",
        "## Eight Macro Bus",
        "",
        "1. snare_fundamental",
        "2. snare_noise",
        "3. snare_transient_bite",
        "4. bass_filter_motion",
        "5. bass_distortion",
        "6. spectral_rotation",
        "7. space_width",
        "8. glitch_fill_probability",
        "",
        "## Snare Ontology",
        "",
        "- Transient",
        "- Fundamental",
        "- Harmonic",
        "- Noise 1",
        "- Noise 2",
        "- Acoustic",
        "",
        "## Build Constraint",
        "",
        "Layer 1 Instrument before Layer 2 Graph before Layer 3 Platform. V2 graph changes must support Demo 0.1 directly.",
    ]
    atomic_write(GRAMMAR_V2_MD_PATH, "\n".join(lines) + "\n")


def update_state(summary: dict[str, Any]) -> None:
    if not STATE_PATH.exists():
        return
    try:
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return
    state["last_index_update"] = summary
    atomic_write(STATE_PATH, json.dumps(state, indent=2, ensure_ascii=False) + "\n")


def build_index(limit_per_table: int | None = None) -> dict[str, Any]:
    tables = [
        (SCANS_DIR / "wabro_scan_project_files.tsv", "full_project_scan"),
        (SCANS_DIR / "wabro_scan_creative_files.tsv", "full_creative_scan"),
        (SCANS_DIR / "wabro_scan_keyword_hits.tsv", "full_keyword_scan"),
        (SCANS_DIR / "wabro_fast_project_files.tsv", "fast_project_scan"),
        (SCANS_DIR / "wabro_fast_keyword_hits.tsv", "fast_keyword_scan"),
    ]
    seen: set[str] = set()
    records: list[dict[str, Any]] = []
    for table, source in tables:
        for row in read_scan_table(table, source, limit=limit_per_table):
            if not row.path or row.path in seen:
                continue
            record = make_record(row)
            if priority_score(record) <= 0:
                continue
            seen.add(row.path)
            records.append(record)

    records.sort(key=priority_score, reverse=True)
    atomic_write(INDEX_PATH, "")
    for record in records:
        append_jsonl(INDEX_PATH, record)

    plugins = plugin_names(DEFAULT_PLUGIN_LIST)
    plugin_summary = {
        "id": "installed_vst3_plugins",
        "indexed_at": now_iso(),
        "path": str(DEFAULT_PLUGIN_LIST),
        "basename": "plugins.txt",
        "category": "installed_plugin_inventory",
        "plugin_count": len(plugins),
        "priority_plugins": [name for name in plugins if name in {"Serum", "Serum2", "Superior Drummer 3", "Kontakt", "Kontakt 8", "Falcon", "Reaktor 6", "Phase Plant", "Vital", "Ozone 11", "Insight 2", "KClip3", "soothe2", "Blackhole", "Oszillos Mega Scope", "MSED"}],
        "confidence": "installed_vst3_path_list",
    }
    append_jsonl(INDEX_PATH, plugin_summary)

    update_graph(records[:250])
    summary = {
        "timestamp": now_iso(),
        "records_written": len(records) + 1,
        "scan_tables": [str(table) for table, _source in tables if table.exists()],
        "index_path": str(INDEX_PATH),
        "graph_path": str(GRAPH_JSON_PATH),
    }
    append_jsonl(LOG_PATH, {"event": "project_index_built", **summary})
    update_state(summary)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Build WABRO_INDEX.jsonl and refresh the project graph from scan outputs.")
    parser.add_argument("--limit-per-table", type=int, default=None, help="Debug limit for each TSV table.")
    args = parser.parse_args()
    summary = build_index(limit_per_table=args.limit_per_table)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
