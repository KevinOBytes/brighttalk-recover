"""Test fixtures and configuration."""

import pytest
from pathlib import Path
from bt_recover.config import Config

@pytest.fixture
def temp_config(tmp_path):
    """Provide temporary configuration."""
    config_path = tmp_path / "config.json"
    return Config(config_path)

@pytest.fixture
def sample_m3u8(tmp_path):
    """Create a sample m3u8 file for testing."""
    content = """
    #EXTM3U
    #EXT-X-VERSION:3
    #EXT-X-TARGETDURATION:10
    #EXTINF:9.009,
    http://example.com/segment1.ts
    #EXTINF:9.009,
    http://example.com/segment2.ts
    #EXT-X-ENDLIST
    """
    m3u8_path = tmp_path / "test.m3u8"
    m3u8_path.write_text(content)
    return m3u8_path 