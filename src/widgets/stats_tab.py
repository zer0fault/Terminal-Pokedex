"""Stats tab showing base stat bars and total."""
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static
from rich.text import Text

from src.models.pokemon import PokemonStat
from src.constants import STAT_NAMES, STAT_MAX_VALUE
from src.constants import (
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


class StatsTab(Vertical):
    """Tab content showing Pokemon base stats as colored bars."""

    def compose(self) -> ComposeResult:
        yield Static("Select a Pokemon to view stats", id="stats-content")

    def load_stats(self, stats: list[PokemonStat]) -> None:
        """Populate the stats display."""
        content = self.query_one("#stats-content", Static)
        text = Text()
        total = 0
        bar_width = 25

        for stat in stats:
            total += stat.base_stat
            abbr = STAT_NAMES.get(stat.name, stat.name[:3].upper())
            color = _stat_color(stat.base_stat)
            filled = int((stat.base_stat / STAT_MAX_VALUE) * bar_width)
            empty = bar_width - filled

            text.append(f"  {abbr}: ", style="bold")
            text.append("\u2588" * filled, style=color)
            text.append("\u2591" * empty, style="dim")
            text.append(f" {stat.base_stat:>3}\n", style="bold")

        text.append(f"\n  {'TOT':>3}: ", style="bold")
        text.append(f"{total}", style="bold underline")

        content.update(text)
