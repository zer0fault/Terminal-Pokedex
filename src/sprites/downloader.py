"""Sprite downloader with disk caching."""
from pathlib import Path

from src.api.client import PokeAPIClient
from src.api.endpoints import sprite_url
from src.constants import SPRITES_DIR


class SpriteDownloader:
    """Downloads and caches Pokemon sprite PNGs to disk."""

    def __init__(self, api_client: PokeAPIClient | None = None) -> None:
        self._api = api_client or PokeAPIClient()
        self._sprites_dir = Path(SPRITES_DIR)
        self._sprites_dir.mkdir(parents=True, exist_ok=True)

    def _sprite_path(self, pokemon_id: int) -> Path:
        return self._sprites_dir / f"{pokemon_id}.png"

    async def get_sprite(self, pokemon_id: int) -> Path | None:
        """Get sprite file path, downloading if necessary."""
        path = self._sprite_path(pokemon_id)
        if path.exists():
            return path
        try:
            image_bytes = await self._api.get_bytes(sprite_url(pokemon_id))
            path.write_bytes(image_bytes)
            return path
        except Exception:
            return None

    async def download_sprite(self, url: str, path: Path) -> None:
        """Download a sprite from a URL to a specific path."""
        try:
            image_bytes = await self._api.get_bytes(url)
            path.write_bytes(image_bytes)
        except Exception:
            pass
