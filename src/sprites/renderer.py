"""Sprite rendering using Pillow and rich-pixels."""
from pathlib import Path

from PIL import Image
from rich_pixels import Pixels

from src.constants import SPRITE_RENDER_WIDTH, SPRITE_BG_COLOR


class SpriteRenderer:
    """Converts Pokemon sprite PNGs to Rich Pixels renderables."""

    @staticmethod
    def render(sprite_path: Path, width: int = SPRITE_RENDER_WIDTH) -> Pixels | None:
        """Render a sprite file to a Pixels object."""
        try:
            with Image.open(sprite_path) as img:
                # Upscale the image first for better quality (Pokemon sprites are small)
                scale_factor = 3
                upscaled_size = (img.width * scale_factor, img.height * scale_factor)
                img = img.resize(upscaled_size, Image.Resampling.NEAREST)

                if img.mode == "RGBA":
                    background = Image.new("RGBA", img.size, (*SPRITE_BG_COLOR, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background.convert("RGB")
                elif img.mode != "RGB":
                    img = img.convert("RGB")

                # Terminal characters are roughly 2:1 (height:width)
                # 0.5 multiplier maintains proper visual aspect
                aspect = img.height / img.width
                height = int(width * aspect * 0.5)
                img = img.resize((width, height), Image.Resampling.LANCZOS)

                return Pixels.from_image(img)
        except Exception:
            return None
