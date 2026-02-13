"""Colored type badge widget."""
from textual.widgets import Static
from src.models.types import get_type_color


class TypeBadge(Static):
    """A small colored label displaying a Pokemon type name."""

    def __init__(self, type_name: str, **kwargs) -> None:
        color = get_type_color(type_name)
        content = f"[bold white on {color}] {type_name.upper()} [/]"
        super().__init__(content, **kwargs)
