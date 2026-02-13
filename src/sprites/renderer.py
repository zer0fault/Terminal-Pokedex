"""Sprite rendering using Pillow and rich-pixels."""
from pathlib import Path

from PIL import Image
from rich_pixels import Pixels

from src.constants import SPRITE_RENDER_WIDTH, SPRITE_BG_COLOR


class SpriteRenderer:
    """Converts Pokemon sprite PNGs to Rich Pixels renderables."""

    @staticmethod
    def render(sprite_path: Path, width: int = SPRITE_RENDER_WIDTH) -> Pixels | None:
        """Render a sprite file with pixel-perfect scaling."""
        try:
            with Image.open(sprite_path) as img:
                # Scale up 2x with NEAREST for crisp pixel art
                scale = 2
                scaled_size = (img.width * scale, img.height * scale)
                img = img.resize(scaled_size, Image.Resampling.NEAREST)

                if img.mode == "RGBA":
                    background = Image.new("RGBA", img.size, (*SPRITE_BG_COLOR, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background.convert("RGB")
                elif img.mode != "RGB":
                    img = img.convert("RGB")

                # Render at 2x size for better visibility while keeping pixel art crisp
                return Pixels.from_image(img)
        except Exception:
            return None
