"""Sprite rendering using Pillow and rich-pixels."""
from pathlib import Path

from PIL import Image
from rich_pixels import Pixels

from src.constants import SPRITE_RENDER_WIDTH, SPRITE_BG_COLOR


class SpriteRenderer:
    """Converts Pokemon sprite PNGs to Rich Pixels renderables."""

    @staticmethod
    def render(sprite_path: Path, width: int = SPRITE_RENDER_WIDTH) -> Pixels | None:
        """Render a sprite file to a Pixels object at original size."""
        try:
            with Image.open(sprite_path) as img:
                if img.mode == "RGBA":
                    background = Image.new("RGBA", img.size, (*SPRITE_BG_COLOR, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background.convert("RGB")
                elif img.mode != "RGB":
                    img = img.convert("RGB")

                # Render at original sprite size (96x96 for Pokemon sprites)
                # No resizing - keep pixel-perfect
                return Pixels.from_image(img)
        except Exception:
            return None
