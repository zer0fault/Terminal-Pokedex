"""Widget for displaying a Pokemon sprite rendered with rich-pixels."""
from textual.app import ComposeResult
from textual.widgets import Static
from textual.containers import Vertical, Horizontal
from textual.widgets import Button
from rich_pixels import Pixels
from rich.text import Text


class SpriteDisplay(Vertical):
    """Displays a Pokemon sprite using half-block pixel rendering with variant toggles."""

    # Note: Main styling defined in pokedex.tcss for consistency

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._sprites: dict[str, Pixels | None] = {}
        self._current_variant = "front_default"

    def compose(self) -> ComposeResult:
        with Horizontal(id="sprite-controls"):
            yield Button("Normal", id="btn-normal", variant="primary", classes="sprite-btn")
            yield Button("Shiny", id="btn-shiny", classes="sprite-btn")
            yield Button("Back", id="btn-back", classes="sprite-btn")
        yield Static("", id="sprite-image")

    def set_sprites(self, sprites: dict[str, Pixels | None]) -> None:
        """Set all sprite variants."""
        self._sprites = sprites
        self._update_display()

    def set_sprite(self, pixels: Pixels | None) -> None:
        """Set a single default sprite (backwards compatibility)."""
        self._sprites = {"front_default": pixels}
        self._current_variant = "front_default"
        self._update_display()

    def clear_sprite(self) -> None:
        self._sprites = {}
        self._update_display()

    def _update_display(self) -> None:
        """Update the sprite display based on current variant."""
        sprite_widget = self.query_one("#sprite-image", Static)
        sprite = self._sprites.get(self._current_variant)

        if sprite:
            sprite_widget.update(sprite)
        elif self._sprites:
            # Fallback to front_default if current variant not available
            fallback = self._sprites.get("front_default")
            if fallback:
                sprite_widget.update(fallback)
            else:
                sprite_widget.update("[dim]Sprite variant not available[/dim]")
        else:
            sprite_widget.update("[dim]No sprite available[/dim]")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle sprite variant button presses."""
        btn_id = event.button.id

        # Update button variants
        for btn in self.query(Button):
            btn.variant = "default"
        event.button.variant = "primary"

        # Determine which sprite to show
        is_shiny = self.query_one("#btn-shiny", Button).variant == "primary"
        is_back = self.query_one("#btn-back", Button).variant == "primary"

        if is_back and is_shiny:
            self._current_variant = "back_shiny"
        elif is_back:
            self._current_variant = "back_default"
        elif is_shiny:
            self._current_variant = "front_shiny"
        else:
            self._current_variant = "front_default"

        self._update_display()
