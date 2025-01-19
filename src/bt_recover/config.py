"""Configuration management for BrightTalk-Recover."""

from typing import Dict, Any, Optional
from pathlib import Path
import json

DEFAULT_CONFIG = {
    "ffmpeg_path": None,
    "output_dir": "output",
    "default_format": "mp4",
    "timeout": 30,
    "retry_attempts": 3,
}


class Config:
    """Manages application configuration."""

    def __init__(self, config_path: Optional[Path] = None) -> None:
        self.config_path = config_path or Path.home() / ".bt-recover.json"
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or return defaults."""
        if self.config_path.exists():
            with open(self.config_path) as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        return DEFAULT_CONFIG.copy()
