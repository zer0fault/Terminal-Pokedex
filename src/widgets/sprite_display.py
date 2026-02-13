"""Widget for displaying a Pokemon sprite rendered with rich-pixels."""
from textual.widgets import Static
from rich_pixels import Pixels


class SpriteDisplay(Static):
    """Displays a Pokemon sprite using half-block pixel rendering."""

    DEFAULT_CSS = """
    SpriteDisplay {
        width: 44;
        height: auto;
        padding: 0 1;
    }
    """

    def set_sprite(self, pixels: Pixels | None) -> None:
        if pixels:
            self.update(pixels)
        else:
            self.update("[dim]No sprite available[/dim]")

    def clear_sprite(self) -> None:
        self.update("")
