"""Moves tab showing move list as a Rich Table."""
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Static
from rich.table import Table
from rich.text import Text

from src.models.pokemon import PokemonMoveRef
from src.models.move import Move


class MovesTab(VerticalScroll):
    """Tab content showing a Pokemon's move list."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._move_details: dict[str, Move] = {}

    def compose(self) -> ComposeResult:
        yield Static("Select a Pokemon to view moves", id="moves-content")

    def load_moves(
        self,
        moves: list[PokemonMoveRef],
        move_details: dict[str, Move] | None = None,
    ) -> None:
        """Populate the moves table."""
        content = self.query_one("#moves-content", Static)
        self._move_details = move_details or {}

        if not moves:
            content.update("[dim]No moves found.[/dim]")
            return

        table = Table(
            title=None,
            show_header=True,
            header_style="bold white on #dc0a2d",
            border_style="#45475a",
            row_styles=["on #1e1e2e", "on #181825"],
            expand=True,
            pad_edge=False,
        )

        table.add_column("Move", style="bold", min_width=16)
        table.add_column("Type", min_width=8)
        table.add_column("Power", justify="right", min_width=5)
        table.add_column("Acc", justify="right", min_width=5)
        table.add_column("PP", justify="right", min_width=4)
        table.add_column("Lvl", justify="right", min_width=4)
        table.add_column("Method", min_width=10)

        level_up = sorted(
            [m for m in moves if m.learn_method == "level-up"],
            key=lambda m: m.level_learned_at,
        )
        others = sorted(
            [m for m in moves if m.learn_method != "level-up"],
            key=lambda m: (m.learn_method, m.name),
        )

        for move in level_up + others:
            name = move.name.replace("-", " ").title()
            level = str(move.level_learned_at) if move.level_learned_at > 0 else "-"
            method = move.learn_method.replace("-", " ").title()

            detail = self._move_details.get(move.name)
            if detail:
                move_type = detail.type_name.title()
                power = str(detail.power) if detail.power else "-"
                accuracy = str(detail.accuracy) if detail.accuracy else "-"
                pp = str(detail.pp)
            else:
                move_type = "-"
                power = "-"
                accuracy = "-"
                pp = "-"

            table.add_row(name, move_type, power, accuracy, pp, level, method)

        content.update(table)
