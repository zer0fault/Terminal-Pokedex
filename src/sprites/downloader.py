"""Sprite downloader with disk caching."""
import logging
from pathlib import Path

from src.api.client import PokeAPIClient
from src.api.endpoints import sprite_url
from src.constants import SPRITES_DIR
from src.sprites.lru_cache import SpriteLRUCache

logger = logging.getLogger(__name__)


class SpriteDownloader:
    """Downloads and caches Pokemon sprite PNGs to disk with LRU eviction."""

    def __init__(self, api_client: PokeAPIClient | None = None, max_cache_size: int = 75) -> None:
        self._api = api_client or PokeAPIClient()
        self._sprites_dir = Path(SPRITES_DIR)
        self._sprites_dir.mkdir(parents=True, exist_ok=True)
        self._lru_cache = SpriteLRUCache(self._sprites_dir, max_sprites=max_cache_size)

    def _sprite_path(self, pokemon_id: int) -> Path:
        return self._sprites_dir / f"{pokemon_id}.png"

    async def get_sprite(self, pokemon_id: int) -> Path | None:
        """Get sprite file path, downloading if necessary."""
        path = self._sprite_path(pokemon_id)
        if path.exists():
            # Update access time for LRU tracking
            self._lru_cache.on_sprite_accessed(path)
            return path
        try:
            image_bytes = await self._api.get_bytes(sprite_url(pokemon_id))
            path.write_bytes(image_bytes)
            # Track new sprite download
            self._lru_cache.on_sprite_downloaded(path)
            return path
        except Exception as e:
            logger.error(f"Failed to download sprite for Pokemon #{pokemon_id}: {e}")
            return None

    async def download_sprite(self, url: str, path: Path) -> None:
        """Download a sprite from a URL to a specific path."""
        try:
            # Check if sprite already exists
            if path.exists():
                self._lru_cache.on_sprite_accessed(path)
                return

            image_bytes = await self._api.get_bytes(url)
            path.write_bytes(image_bytes)
            # Track new sprite download
            self._lru_cache.on_sprite_downloaded(path)
        except Exception as e:
            logger.warning(f"Failed to download sprite from {url}: {e}")
