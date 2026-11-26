"""Image generation via Pollinations free tier, with a local fallback image.

The free image endpoint allows roughly one image per 45 seconds per IP and
sometimes returns 503 while the shared pool is busy. `generate_image` retries
with backoff, then falls back to a local PIL illustration so the wall never
goes dark during a reading.
"""
from __future__ import annotations

import hashlib
import time
import urllib.parse
import urllib.request

from PIL import Image, ImageDraw

from .config import POLLINATIONS_IMAGE_URL, DEFAULT_IMAGE_SIZE


class ImageGenerationError(RuntimeError):
    pass


def _fetch_remote(prompt: str, size: tuple[int, int], seed: int,
                  retries: int = 4) -> bytes:
    url = (POLLINATIONS_IMAGE_URL + urllib.parse.quote(prompt) +
           f"?width={size[0]}&height={size[1]}&seed={seed}&nologo=true")
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = resp.read()
            if data[:4] == b"\x89PNG" or data[:2] == b"\xff\xd8":
                return data
            last = RuntimeError("unexpected image payload")
        except Exception as exc:             # noqa: BLE001
            last = exc
        if attempt < retries - 1:
            time.sleep(12 * (attempt + 1))   # free tier: ~1 image / 45s
    raise ImageGenerationError(str(last))


def fallback_image(prompt: str, size: tuple[int, int], path: str) -> str:
    """Draw a deterministic abstract illustration when the API is unavailable."""
    digest = hashlib.sha256(prompt.encode()).digest()
    w, h = size
    img = Image.new("RGB", (w, h), (18, 16, 22))
    d = ImageDraw.Draw(img)
    palette = [(214, 163, 79), (128, 54, 44), (78, 104, 96),
               (196, 186, 168), (90, 70, 110), (168, 96, 60)]
    for i in range(14):
        x0 = digest[i] % w
        y0 = digest[(i + 5) % 32] % h
        r = 40 + digest[(i + 11) % 32] % 160
        col = palette[digest[(i + 19) % 32] % len(palette)]
        if i % 3 == 0:
            d.ellipse([x0 - r, y0 - r, x0 + r, y0 + r], fill=col)
        elif i % 3 == 1:
            d.rectangle([x0 - r // 2, y0 - r, x0 + r // 2, y0 + r], fill=col)
        else:
            d.polygon([(x0, y0 - r), (x0 + r, y0 + r), (x0 - r, y0 + r)], fill=col)
    img.save(path)
    return path


def generate_image(prompt: str, path: str, size: tuple[int, int] = DEFAULT_IMAGE_SIZE,
                   seed: int = 1, retries: int = 4) -> dict:
    """Write an illustration to `path`. Returns metadata about the source."""
    try:
        data = _fetch_remote(prompt, size, seed, retries)
        with open(path, "wb") as fh:
            fh.write(data)
        return {"source": "pollinations", "path": path, "bytes": len(data)}
    except ImageGenerationError as exc:
        fallback_image(prompt, size, path)
        return {"source": "local-fallback", "path": path, "reason": str(exc)[:200]}
