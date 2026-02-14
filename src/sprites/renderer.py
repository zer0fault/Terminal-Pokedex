"""Sprite rendering using Pillow and rich-pixels."""
import logging
from pathlib import Path

from PIL import Image
from rich_pixels import Pixels

from src.constants import SPRITE_RENDER_WIDTH

logger = logging.getLogger(__name__)


class SpriteRenderer:
    """Converts Pokemon sprite PNGs to Rich Pixels renderables."""

    @staticmethod
    def render(sprite_path: Path, width: int = SPRITE_RENDER_WIDTH) -> Pixels | None:
        """Render a sprite file to Pixels.

        Uses NEAREST neighbor resampling to preserve pixel art sharpness,
        and keeps RGBA transparency so the terminal background shows through.
        """
        try:
            img = Image.open(sprite_path)

            # Convert to RGBA to preserve transparency
            if img.mode != "RGBA":
                img = img.convert("RGBA")

            # Resize to fit terminal, maintaining aspect ratio
            # NEAREST keeps pixel art sharp (no blurring)
            ratio = width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((width, new_height), Image.NEAREST)

            pixels = Pixels.from_image(img)
            img.close()
            return pixels
        except Exception as e:
            logger.error(f"Sprite render failed for {sprite_path}: {e}")
            return None
