"""Sprite rendering using Pillow and rich-pixels."""
from pathlib import Path

from PIL import Image
from rich_pixels import Pixels

from src.constants import SPRITE_RENDER_WIDTH, SPRITE_BG_COLOR


class SpriteRenderer:
    """Converts Pokemon sprite PNGs to Rich Pixels renderables."""

    @staticmethod
    def render(sprite_path: Path, width: int = SPRITE_RENDER_WIDTH) -> Pixels | None:
        """Render a sprite file to Pixels."""
        try:
            img = Image.open(sprite_path)

            # Convert to RGB, handling transparency
            if img.mode == "RGBA":
                rgb_img = Image.new("RGB", img.size, SPRITE_BG_COLOR)
                rgb_img.paste(img, mask=img.split()[3])
                img = rgb_img
            elif img.mode != "RGB":
                img = img.convert("RGB")

            # Return as Pixels (no resizing - use original size)
            pixels = Pixels.from_image(img)
            img.close()
            return pixels
        except Exception as e:
            print(f"Sprite render failed: {e}")
            return None
