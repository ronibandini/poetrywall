"""Offline tests: no network or microphone needed."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from poetrywall.config import STYLES
from poetrywall.excerpt import build_image_prompt
from poetrywall.imagegen import fallback_image
from gallery import build as build_gallery


def test_styles():
    assert len(STYLES) == 16
    assert all(isinstance(s, str) and s for s in STYLES)


def test_image_prompt():
    p = build_image_prompt("rain on empty street", STYLES[0])
    assert "rain on empty street" in p and "No text" in p


def test_fallback_image():
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "fallback.jpg")
        fallback_image("a golden typewriter", (120, 120), path)
        assert os.path.getsize(path) > 1000


def test_gallery():
    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, "gallery.html")
        n = build_gallery(d, out)
        assert n == 0 and os.path.exists(out)


if __name__ == "__main__":
    for fn in [test_styles, test_image_prompt, test_fallback_image, test_gallery]:
        fn()
        print("PASS", fn.__name__)
