Python 3.14.5 (v3.14.5:5607950ef23, May 10 2026, 07:38:09) [Clang 21.0.0 (clang-2100.0.123.102)] on darwin
Enter "help" below or click "Help" above for more information.
#!/usr/bin/env python3
"""
WABRO AI Council v0.1

Reads:
  CHATGPT_INBOX.md

Writes:
  AI_COUNCIL/CHATGPT_ARCHITECT.md
  AI_COUNCIL/GEMINI_KNOWLEDGE.md
  AI_COUNCIL/CLAUDE_REVIEWER.md
  AI_COUNCIL/DEEPSEEK_CODER.md
  AI_COUNCIL/LLAMA_LOCAL.md
  AI_COUNCIL/COUNCIL_SUMMARY.md

Uses official APIs where available and local Ollama for Llama.
"""

from __future__ import annotations

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

import requests


WABRO_ROOT = Path("/Users/lukewabro/Documents/WABRO")
INBOX = WABRO_ROOT / "CHATGPT_INBOX.md"
COUNCIL_DIR = WABRO_ROOT / "AI_COUNCIL"

FILES_TO_READ = [
    "WABRO_STATE.json",
    "WABRO_MEMORY.md",
    "WABRO_TASKS.md",
    "WABRO_MACROS.md",
    "WABRO_PROJECT_GRAPH.md",
    "WABRO_PROJECT_GRAPH.json",
    "WABRO_INDEX.jsonl",
    "WABRO_DEMO_0_1_BUILD_BRIEF.md",
]

COUNCIL_DIR.mkdir(exist_ok=True)


def read_file(path: Path, max_chars: int = 20000) -> str:
    if not path.exists():
        return f"[MISSING FILE: {path}]"
    text = path.read_text(errors="ignore")
    return text[:max_chars]


def write_file(name: str, content: str) -> None:
    path = COUNCIL_DIR / name
    path.write_text(content, encoding="utf-8")


def build_context() -> str:
    chunks = []

    chunks.append("# WABRO AI Council Context")
    chunks.append(f"Timestamp: {datetime.now().isoformat()}")

    chunks.append("\n# ChatGPT Phone Direction")
    chunks.append(read_file(INBOX))

    for filename in FILES_TO_READ:
        path = WABRO_ROOT / filename
        chunks.append(f"\n# File: {filename}")
        chunks.append(read_file(path))

    return "\n\n".join(chunks)


def role_prompt(role: str, context: str) -> str:
    return f"""
You are part of the WABRO AI Council.

Role:
{role}

Project:
WABRO X ASSEMBLAGE is Luke WABRO's AI-assisted creative operating system for neurofunk, Bitwig, Muse 2 EEG, TouchDesigner, snare geometry, project indexing, and future open-source music mutation.

Current priority:
Do not build the social platform yet.
Focus on Demo 0.1:

Backwards V5
+ Muse 2 or simulator
+ 8 macros
+ Bitwig
+ snare visualiser
+ persistent WABRO_STATE.json

Respond with:
1. What changed or matters
2. Risks or mistakes
3. Concrete next actions for Codex
4. Suggested memory updates
5. What to ignore for now

Context:
{context}
""".strip()


def call_openai(prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "[OPENAI_API_KEY missing]"

    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": os.getenv("OPENAI_MODEL", "gpt-5.1"),
            "input": prompt,
        },
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()

    # Responses API commonly returns text in output blocks.
    try:
        return data["output"][0]["content"][0]["text"]
    except Exception:
        return json.dumps(data, indent=2)[:10000]


def call_gemini(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "[GEMINI_API_KEY missing]"

    model = os.getenv("GEMINI_MODEL", "gemini-2.5-pro")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json={
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        },
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return json.dumps(data, indent=2)[:10000]


def call_claude(prompt: str) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return "[ANTHROPIC_API_KEY missing]"

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        },
        json={
            "model": os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5"),
            "max_tokens": 4000,
            "messages": [
                {"role": "user", "content": prompt}
            ],
        },
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()

    try:
        return data["content"][0]["text"]
    except Exception:
        return json.dumps(data, indent=2)[:10000]


def call_deepseek(prompt: str) -> str:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return "[DEEPSEEK_API_KEY missing]"

    response = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
            "messages": [
                {"role": "user", "content": prompt}
            ],
        },
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()

    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        return json.dumps(data, indent=2)[:10000]


def call_ollama(prompt: str) -> str:
    model = os.getenv("OLLAMA_MODEL", "llama3.2")

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
        },
        timeout=300,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("response", json.dumps(data, indent=2)[:10000])


def make_codex_packet(outputs: dict[str, str]) -> str:
    sections = [
        "# WABRO Codex Packet",
        f"Generated: {datetime.now().isoformat()}",
        "",
        "Codex: read this packet and implement only the concrete next actions that support Demo 0.1.",
        "",
        "Current priority:",
        "Backwards V5 + Muse 2/simulator + 8 macros + Bitwig + snare visualiser + persistent state.",
    ]

    for name, text in outputs.items():
        sections.append(f"\n# {name}")
        sections.append(text)

    sections.append(
        """
# Codex Instruction

Extract the overlapping recommendations.
Ignore architecture drift.
Update WABRO_TASKS.md and implement the next smallest working step.
"""
    )

    return "\n\n".join(sections)


def main() -> None:
    context = build_context()

    agents = {
        "CHATGPT_ARCHITECT.md": (
            "Chief Architect. Keep the project focused on Demo 0.1 and prevent architecture drift.",
            call_openai,
        ),
        "GEMINI_KNOWLEDGE.md": (
            "Knowledge Engineer. Improve graph schema, Luke Grammar, and archive structure.",
            call_gemini,
...         ),
...         "CLAUDE_REVIEWER.md": (
...             "Systems Reviewer. Look for contradictions, risks, unclear instructions, and simplifications.",
...             call_claude,
...         ),
...         "DEEPSEEK_CODER.md": (
...             "Coder. Suggest concrete Python/file-system implementation steps.",
...             call_deepseek,
...         ),
...         "LLAMA_LOCAL.md": (
...             "Local private agent. Review from inside the local WABRO context and suggest safe next steps.",
...             call_ollama,
...         ),
...     }
... 
...     outputs = {}
... 
...     for filename, (role, function) in agents.items():
...         print(f"Running {filename}...")
...         prompt = role_prompt(role, context)
... 
...         try:
...             output = function(prompt)
...         except Exception as exc:
...             output = f"[ERROR running {filename}: {exc}]"
... 
...         write_file(filename, output)
...         outputs[filename] = output
... 
...     summary = make_codex_packet(outputs)
...     write_file("COUNCIL_SUMMARY.md", summary)
... 
...     print("Done.")
...     print(f"Wrote outputs to: {COUNCIL_DIR}")
... 
... 
... if __name__ == "__main__":
