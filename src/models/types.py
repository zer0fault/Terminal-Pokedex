"""Pokemon type utilities."""
from src.constants import TYPE_COLORS, TYPE_ABBREVIATIONS


def get_type_color(type_name: str) -> str:
    """Return hex color for a Pokemon type."""
    return TYPE_COLORS.get(type_name.lower(), "#FFFFFF")


def get_type_abbreviation(type_name: str) -> str:
    """Return 3-letter abbreviation for a type."""
    return TYPE_ABBREVIATIONS.get(type_name.lower(), "???")
