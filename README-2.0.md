# 🎨 Poetry Wall 2.0

**Illustrate a live poetry reading with AI — no API keys required.**

Poetry Wall listens to a reading, turns it into a short visual excerpt, generates
an illustration and projects it onto a wall. This version replaces the original
2023 OpenAI/DALL·E 2 pipeline with the **Pollinations free tier** and adds several
enhancements while keeping the Raspberry Pi workflow intact.

Original project and 1.0 documentation: [README.md](README.md) ·
[ronibandini/poetrywall](https://github.com/ronibandini/poetrywall).

## ✨ What changed from 1.0

| | 1.0 (2023) | 2.0 |
|---|---|---|
| Text model | `text-davinci-003`, API key | Pollinations free text API, **no key** |
| Images | DALL·E 2, API key | Pollinations free image endpoint, **no key** |
| Input | microphone only | microphone **or** `--text` / `--demo` |
| Styles | 16 selector positions | 16 styles, CLI `--style N` |
| Sessions | UUID wav/txt/jpg only | UUID folder with `session.json` manifest |
| Display | OpenCV only | OpenCV + self-contained HTML slideshow |
| Rate limits | none handled | retry/backoff + **local fallback image** |
| Prompts | plain summary | anti-LLM-tell rules for cleaner prose |
| Tests | none | offline unit tests |

## 🧠 Pipeline

```
voice → WAV → speech-to-text → AI excerpt → image prompt → AI illustration → wall
text input ────────────────────────────────────────────────────┘
```

## 🚀 Quick start

```bash
pip install requests openai Pillow speech_recognition opencv-python

# Built-in sample poem (no mic, no keys)
python wall.py --demo --style 2

# Your own text
python wall.py --text "La señorita del abanico va por el puente..." --style 5

# Live USB microphone reading, Spanish
python wall.py --mic --seconds 12 --language es-ES --style 0

# Project the saved sessions as a slideshow
python gallery.py --sessions sessions --output gallery.html
```

Run `python wall.py --help` for all options. Use `python tests/test_pipeline.py`
for offline checks.

## 🎛️ Styles

`--style N` selects one of 16 visual treatments: oil painting, woodcut, surreal
collage, watercolor, charcoal, cyberpunk, expressionist cinema, vector poster,
sumi-e, brutalist concrete, magic realism, dirty realism, art deco, cyanotype,
low-poly and hand-painted signage.

## 🔑 No credentials

Both Pollinations endpoints used here are free and anonymous. If you do have a
Pollinations key you can set `POLLINATIONS_API_KEY` for higher limits; the code
works without it.

## ⏱️ Rate limits and fallback

The free image tier allows roughly **one image every 45 seconds per IP**. The
client retries with backoff and, if the shared pool is busy, draws a
deterministic abstract illustration locally so the projector never goes dark.
Each session records which source produced the image in `session.json`.

## ✍️ Cleaner excerpts

The excerpt prompt explicitly avoids formulaic LLM prose — negative parallelism
("it is not X, it is Y"), rule-of-three lists and stock AI vocabulary — so the
five-word bridge between poem and image stays concrete.

## 📁 Structure

```
poetrywall/
├── wall.py                 # full pipeline CLI
├── gallery.py              # HTML slideshow generator
├── poetrywall/
│   ├── config.py           # styles, URLs, anti-LLM prompt rule
│   ├── excerpt.py          # Pollinations text API
│   ├── imagegen.py         # Pollinations image API + local fallback
│   ├── record.py           # arecord wrapper
│   └── transcribe.py       # speech recognition
├── tests/test_pipeline.py  # offline tests
└── sessions/               # generated UUID sessions
```

## 📜 License

MIT — see [LICENSE](LICENSE).
