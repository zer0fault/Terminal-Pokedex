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
                # Handle transparency first
                if img.mode == "RGBA":
                    background = Image.new("RGB", img.size, SPRITE_BG_COLOR)
                    background.paste(img, mask=img.split()[3])
                    img = background
                elif img.mode != "RGB":
                    img = img.convert("RGB")

                # Scale up 2x with NEAREST for crisp pixel art
                scale = 2
                new_width = img.width * scale
                new_height = img.height * scale
                img = img.resize((new_width, new_height), Image.Resampling.NEAREST)

                # Convert to Pixels for terminal display
                return Pixels.from_image(img)
        except Exception as e:
            # Log error for debugging
            import sys
            print(f"Sprite render error: {e}", file=sys.stderr)
            return None
