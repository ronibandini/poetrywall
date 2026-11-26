"""Audio capture (arecord) — Poetry Wall 2.0."""
from __future__ import annotations

import os
import subprocess
import uuid


def record_wav(path: str, seconds: int = 10, device: str = "plughw:1,0") -> str:
    """Record a reading to `path` using arecord. Returns the path."""
    cmd = ["arecord", "-D", device, "--duration", str(seconds), path]
    subprocess.run(cmd, check=True, timeout=seconds + 30)
    return path


def new_session_id() -> str:
    return str(uuid.uuid4())
