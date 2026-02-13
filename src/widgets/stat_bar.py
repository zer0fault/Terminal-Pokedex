"""Single stat bar widget with color coding."""
from rich.text import Text
from textual.widgets import Static

from src.constants import (
    STAT_NAMES, STAT_MAX_VALUE,
    STAT_COLOR_LOW, STAT_COLOR_MEDIUM, STAT_COLOR_GOOD,
    STAT_COLOR_HIGH, STAT_COLOR_VERY_HIGH, STAT_COLOR_MAX,
)


def _stat_color(value: int) -> str:
    if value < 50:
        return STAT_COLOR_LOW
    elif value < 80:
        return STAT_COLOR_MEDIUM
    elif value < 100:
        return STAT_COLOR_GOOD
    elif value < 130:
        return STAT_COLOR_HIGH
    elif value < 160:
        return STAT_COLOR_VERY_HIGH
    else:
        return STAT_COLOR_MAX


class StatBar(Static):
    """Displays a single base stat as a labeled colored bar."""

    def __init__(self, stat_name: str, value: int, **kwargs) -> None:
        self._stat_name = stat_name
        self._value = value
        super().__init__(**kwargs)

    def render(self) -> Text:
        abbr = STAT_NAMES.get(self._stat_name, self._stat_name[:3].upper())
        color = _stat_color(self._value)
        bar_width = 20
        filled = int((self._value / STAT_MAX_VALUE) * bar_width)
        empty = bar_width - filled

        text = Text()
        text.append(f" {abbr}: ", style="bold")
        text.append("\u2588" * filled, style=color)
        text.append("\u2591" * empty, style="dim")
        text.append(f" {self._value:>3}", style="bold")
        return text
