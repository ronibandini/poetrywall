"""AI excerpt generation using the Pollinations free text API (no API key)."""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request

from .config import ANTI_LLM_RULE, DEFAULT_TEXT_MODEL, POLLINATIONS_TEXT_URL


def _call(messages: list[dict], model: str = DEFAULT_TEXT_MODEL,
          max_tokens: int = 120, retries: int = 3) -> str:
    payload = json.dumps({
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.6,
    }).encode()
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                POLLINATIONS_TEXT_URL, data=payload,
                headers={"Content-Type": "application/json",
                         "User-Agent": "poetrywall/2.0"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.load(resp)
            return (data["choices"][0]["message"]["content"] or "").strip()
        except Exception as exc:            # noqa: BLE001 - network layer
            last = exc
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"Pollinations text API failed: {last}")


def five_word_excerpt(transcription: str, language: str = "es") -> str:
    """Condense a reading into a short image-prompt excerpt."""
    prompt = (
        f"You are a literary editor. Read the text below and write a compact "
        f"visual excerpt of about five words that captures its central image. "
        f"Reply with the excerpt only, no explanation. {ANTI_LLM_RULE}\n\n"
        f"Text ({language}):\n{transcription}\n\nExcerpt:"
    )
    result = _call([{"role": "user", "content": prompt}], max_tokens=80)
    # Hard cap: keep it short even if the model rambles.
    words = result.replace("\n", " ").split()[:8]
    return " ".join(words) or transcription[:80]


def build_image_prompt(excerpt: str, style: str) -> str:
    return (
        f"Illustration for a poetry reading. Visual motif: {excerpt}. "
        f"Style: {style}. No text, no letters, no watermark."
    )
