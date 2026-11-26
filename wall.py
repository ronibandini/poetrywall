#!/usr/bin/env python3
"""Poetry Wall 2.0 — full pipeline.

Voice -> WAV -> speech-to-text -> AI excerpt -> AI illustration -> wall.
Now uses the Pollinations free tier for both text and images (no API keys),
with a text-input demo mode and a local image fallback so the wall never
goes dark while the shared image pool is busy.

Examples:
  python wall.py --text "La señorita del abanico va por el puente..." --style 3
  python wall.py --mic --seconds 12 --language es-ES
  python wall.py --demo                      # built-in sample poem
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

from poetrywall.config import STYLES, session_dir
from poetrywall.excerpt import five_word_excerpt, build_image_prompt
from poetrywall.imagegen import generate_image, fallback_image
from poetrywall.record import record_wav, new_session_id

SAMPLE = (
    "La señorita del abanico va por el puente del fresco río. "
    "Los caballeros con sus levitas miran el puente sin barandillas. "
    "Los grillos cantan por el Oeste. La señorita va por lo verde."
)


def project(image_path: str, seconds: int = 15) -> None:
    """Display the image fullscreen. Falls back to printing the path."""
    try:
        import cv2  # type: ignore
        img = cv2.imread(image_path)
        if img is None:
            raise RuntimeError("could not read image")
        cv2.namedWindow("Poetry Wall", cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Poetry Wall", img)
        cv2.waitKey(seconds * 1000)
        cv2.destroyAllWindows()
    except Exception:
        print(f"[wall] projection unavailable; image: {image_path}")
        time.sleep(min(seconds, 2))


def run(text: str, style_index: int, out_base: str, language: str,
        display_seconds: int, retries: int) -> dict:
    sid = new_session_id()
    folder = session_dir(out_base, sid)
    style = STYLES[style_index % len(STYLES)]

    with open(os.path.join(folder, f"{sid}.txt"), "w", encoding="utf-8") as fh:
        fh.write(text)

    excerpt = five_word_excerpt(text, language=language)
    image_prompt = build_image_prompt(excerpt, style)
    with open(os.path.join(folder, "prompt.txt"), "w", encoding="utf-8") as fh:
        fh.write(image_prompt)

    image_path = os.path.join(folder, f"{sid}.jpg")
    meta = generate_image(image_prompt, image_path, retries=retries)

    manifest = {
        "id": sid, "text": text, "excerpt": excerpt,
        "style_index": style_index, "style": style,
        "image_prompt": image_prompt, "image": meta,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    with open(os.path.join(folder, "session.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)

    project(image_path, display_seconds)
    return manifest


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Poetry Wall 2.0 (Pollinations free tier)")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--text", help="poem text to illustrate")
    src.add_argument("--mic", action="store_true", help="record from USB microphone")
    src.add_argument("--demo", action="store_true", help="use the built-in sample poem")
    ap.add_argument("--style", type=int, default=0, help=f"0-{len(STYLES)-1} visual style")
    ap.add_argument("--seconds", type=int, default=10, help="mic recording seconds")
    ap.add_argument("--language", default="es-ES", help="speech recognition locale")
    ap.add_argument("--display", type=int, default=15, help="wall display seconds")
    ap.add_argument("--out", default="sessions", help="session output directory")
    ap.add_argument("--retries", type=int, default=4, help="image API retries")
    args = ap.parse_args(argv)

    text = args.text or (SAMPLE if args.demo else "")
    if args.mic:
        wav = os.path.join(args.out, f"{new_session_id()}.wav")
        os.makedirs(args.out, exist_ok=True)
        record_wav(wav, args.seconds)
        from poetrywall.transcribe import transcribe
        text = transcribe(wav, args.language)

    manifest = run(text, args.style, args.out, args.language, args.display, args.retries)
    print(json.dumps({k: manifest[k] for k in ("id", "excerpt", "style", "image")},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
