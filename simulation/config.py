"""Configuration utilities for loading simulator settings."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_config(path: str | Path) -> dict[str, Any]:
    """Load a JSON configuration file into a dictionary."""
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)
