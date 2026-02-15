"""LRU cache manager for sprite files."""
import logging
import time
from pathlib import Path
from typing import Dict

logger = logging.getLogger(__name__)


class SpriteLRUCache:
    """Manages sprite cache with LRU eviction policy."""

    def __init__(self, sprites_dir: Path, max_sprites: int = 75) -> None:
        """Initialize LRU cache.

        Args:
            sprites_dir: Directory containing cached sprites
            max_sprites: Maximum number of sprites to keep in cache
        """
        self.sprites_dir = sprites_dir
        self.max_sprites = max_sprites
        self.access_times: Dict[str, float] = {}
        self._load_existing_sprites()

    def _load_existing_sprites(self) -> None:
        """Load existing sprite files and initialize their access times."""
        if not self.sprites_dir.exists():
            return

        sprite_files = list(self.sprites_dir.glob("*.png"))

        # Sort by modification time (oldest first)
        sprite_files.sort(key=lambda p: p.stat().st_mtime)

        # If over limit, delete oldest sprites immediately
        if len(sprite_files) > self.max_sprites:
            sprites_to_delete = len(sprite_files) - self.max_sprites
            for sprite_file in sprite_files[:sprites_to_delete]:
                logger.info(f"LRU cleanup: Removing old sprite {sprite_file.name}")
                sprite_file.unlink()
            # Keep only the newest sprites
            sprite_files = sprite_files[sprites_to_delete:]

        # Initialize access times for remaining sprites based on mtime
        current_time = time.time()
        for idx, sprite_file in enumerate(sprite_files):
            # Use file modification time, or assign sequential times if needed
            self.access_times[str(sprite_file)] = sprite_file.stat().st_mtime

        logger.info(f"LRU cache initialized with {len(self.access_times)} sprites (limit: {self.max_sprites})")

    def on_sprite_accessed(self, sprite_path: Path) -> None:
        """Update access time for a sprite.

        Args:
            sprite_path: Path to the sprite file that was accessed
        """
        sprite_key = str(sprite_path)
        self.access_times[sprite_key] = time.time()

        # Update file modification time to reflect access
        if sprite_path.exists():
            sprite_path.touch()

    def on_sprite_downloaded(self, sprite_path: Path) -> None:
        """Handle new sprite download and enforce cache limit.

        Args:
            sprite_path: Path to the newly downloaded sprite
        """
        sprite_key = str(sprite_path)
        self.access_times[sprite_key] = time.time()

        # Enforce cache size limit
        while len(self.access_times) > self.max_sprites:
            # Find least recently used sprite
            oldest_sprite = min(self.access_times, key=self.access_times.get)
            oldest_path = Path(oldest_sprite)

            # Delete the file
            if oldest_path.exists():
                logger.debug(f"LRU eviction: Removing {oldest_path.name}")
                oldest_path.unlink()

            # Remove from tracking
            del self.access_times[oldest_sprite]

    def get_cache_stats(self) -> dict:
        """Get current cache statistics.

        Returns:
            Dictionary with cache size, limit, and usage percentage
        """
        current_size = len(self.access_times)
        return {
            "current_size": current_size,
            "max_size": self.max_sprites,
            "usage_percent": (current_size / self.max_sprites * 100) if self.max_sprites > 0 else 0,
        }
