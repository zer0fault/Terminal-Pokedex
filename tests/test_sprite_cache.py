"""Tests for sprite LRU cache."""
import time
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from src.sprites.lru_cache import SpriteLRUCache


class TestSpriteLRUCache:
    """Test LRU cache eviction logic."""

    def test_cache_tracks_access_times(self):
        """Test that cache tracks when sprites are accessed."""
        with TemporaryDirectory() as tmpdir:
            cache = SpriteLRUCache(Path(tmpdir), max_sprites=5)

            sprite1 = Path(tmpdir) / "sprite1.png"
            sprite1.write_bytes(b"fake image")

            cache.on_sprite_accessed(sprite1)

            assert str(sprite1) in cache.access_times
            assert cache.access_times[str(sprite1)] > 0

    def test_cache_evicts_oldest_when_full(self):
        """Test that oldest sprite is removed when cache exceeds limit."""
        with TemporaryDirectory() as tmpdir:
            cache = SpriteLRUCache(Path(tmpdir), max_sprites=3)

            # Create and track 3 sprites
            sprites = []
            for i in range(3):
                sprite = Path(tmpdir) / f"sprite{i}.png"
                sprite.write_bytes(b"fake image")
                cache.on_sprite_downloaded(sprite)
                sprites.append(sprite)
                time.sleep(0.01)  # Ensure different timestamps

            assert len(cache.access_times) == 3
            assert all(s.exists() for s in sprites)

            # Add a 4th sprite - should evict the oldest (sprite0)
            sprite3 = Path(tmpdir) / "sprite3.png"
            sprite3.write_bytes(b"fake image")
            cache.on_sprite_downloaded(sprite3)

            assert len(cache.access_times) == 3
            assert not sprites[0].exists()  # Oldest removed
            assert sprites[1].exists()
            assert sprites[2].exists()
            assert sprite3.exists()

    def test_cache_respects_max_sprites_limit(self):
        """Test that cache never exceeds max_sprites."""
        with TemporaryDirectory() as tmpdir:
            cache = SpriteLRUCache(Path(tmpdir), max_sprites=5)

            # Add 10 sprites
            for i in range(10):
                sprite = Path(tmpdir) / f"sprite{i}.png"
                sprite.write_bytes(b"fake image")
                cache.on_sprite_downloaded(sprite)
                time.sleep(0.01)

            # Should only have 5 sprites tracked
            assert len(cache.access_times) == 5

            # Only the 5 most recent should exist
            existing = [p for p in Path(tmpdir).glob("*.png")]
            assert len(existing) == 5

    def test_accessing_sprite_updates_timestamp(self):
        """Test that accessing a sprite updates its timestamp."""
        with TemporaryDirectory() as tmpdir:
            cache = SpriteLRUCache(Path(tmpdir), max_sprites=3)

            sprite = Path(tmpdir) / "sprite.png"
            sprite.write_bytes(b"fake image")

            cache.on_sprite_accessed(sprite)
            first_time = cache.access_times[str(sprite)]

            time.sleep(0.1)

            cache.on_sprite_accessed(sprite)
            second_time = cache.access_times[str(sprite)]

            assert second_time > first_time

    def test_cache_loads_existing_sprites_on_init(self):
        """Test that cache loads existing sprites from disk on initialization."""
        with TemporaryDirectory() as tmpdir:
            # Create some sprites
            sprite1 = Path(tmpdir) / "sprite1.png"
            sprite2 = Path(tmpdir) / "sprite2.png"
            sprite1.write_bytes(b"fake image 1")
            sprite2.write_bytes(b"fake image 2")

            # Initialize cache - should load existing sprites
            cache = SpriteLRUCache(Path(tmpdir), max_sprites=10)

            assert len(cache.access_times) == 2
            assert str(sprite1) in cache.access_times
            assert str(sprite2) in cache.access_times

    def test_cache_evicts_excess_sprites_on_init(self):
        """Test that cache evicts excess sprites when initialized with more than max_sprites."""
        with TemporaryDirectory() as tmpdir:
            # Create 10 sprites
            sprites = []
            for i in range(10):
                sprite = Path(tmpdir) / f"sprite{i}.png"
                sprite.write_bytes(b"fake image")
                sprites.append(sprite)
                time.sleep(0.01)  # Ensure different mtimes

            # Initialize cache with limit of 5 - should evict 5 oldest
            cache = SpriteLRUCache(Path(tmpdir), max_sprites=5)

            assert len(cache.access_times) == 5

            # First 5 should be removed (oldest by mtime)
            for i in range(5):
                assert not sprites[i].exists()

            # Last 5 should remain
            for i in range(5, 10):
                assert sprites[i].exists()

    def test_empty_cache_directory(self):
        """Test that cache handles empty directory correctly."""
        with TemporaryDirectory() as tmpdir:
            cache = SpriteLRUCache(Path(tmpdir), max_sprites=5)
            assert len(cache.access_times) == 0

    def test_cache_handles_missing_sprite_gracefully(self):
        """Test that cache doesn't crash if sprite file is missing."""
        with TemporaryDirectory() as tmpdir:
            cache = SpriteLRUCache(Path(tmpdir), max_sprites=5)

            # Try to access a sprite that doesn't exist
            missing_sprite = Path(tmpdir) / "missing.png"
            cache.on_sprite_accessed(missing_sprite)

            # Should track it anyway (for future download)
            assert str(missing_sprite) in cache.access_times
