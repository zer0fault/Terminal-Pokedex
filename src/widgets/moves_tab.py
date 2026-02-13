"""Moves tab with a sortable DataTable."""
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import DataTable

from src.models.pokemon import PokemonMoveRef


class MovesTab(Vertical):
    """Tab content showing a Pokemon's move list in a DataTable."""

    def compose(self) -> ComposeResult:
        table = DataTable(id="moves-table", cursor_type="row", zebra_stripes=True)
        yield table

    def on_mount(self) -> None:
        table = self.query_one("#moves-table", DataTable)
        table.add_columns("Move", "Level", "Method")

    def load_moves(self, moves: list[PokemonMoveRef]) -> None:
        """Populate the moves DataTable."""
        table = self.query_one("#moves-table", DataTable)
        table.clear()

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
            table.add_row(name, level, method)
