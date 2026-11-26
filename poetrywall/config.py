"""Poetry Wall 2.0 — configuration and visual styles."""
from __future__ import annotations

import os

POLLINATIONS_TEXT_URL = "https://text.pollinations.ai/openai"
POLLINATIONS_IMAGE_URL = "https://image.pollinations.ai/prompt/"
DEFAULT_TEXT_MODEL = "openai"          # GPT-OSS 20B, free anonymous tier
DEFAULT_IMAGE_SIZE = (768, 768)
DEFAULT_LANGUAGE = "es"

# 16 selectable visual styles, carried over from the original installation
# and expanded with a few new ones.
STYLES = [
    "oil painting, warm ochre and deep shadow",
    "black and white woodcut print",
    "surreal collage, torn paper texture",
    "watercolor on rough paper",
    "charcoal drawing, high contrast",
    "neon cyberpunk night scene",
    "1920s expressionist cinema still",
    "flat vector poster, bold shapes",
    "ink wash sumi-e painting",
    "brutalist concrete sculpture",
    "dreamlike magic realism",
    "dirty realism, empty urban interior",
    "art deco screen print",
    "cyanotype photograph",
    "low-poly geometric landscape",
    "hand-painted signage, faded colors",
]

# Prompt guard: avoid the formulaic structures that make LLM text obvious.
ANTI_LLM_RULE = (
    "Do not use 'it is not X, it is Y', rule-of-three lists, or stock AI words "
    "such as delve, tapestry, realm, pivotal, intricate, meticulous, testament, "
    "showcase, or underscore. Plain, specific, uneven language only."
)


def session_dir(base: str, session_id: str) -> str:
    path = os.path.join(base, session_id)
    os.makedirs(path, exist_ok=True)
    return path
