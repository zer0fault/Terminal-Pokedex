"""Moves tab with a sortable DataTable."""
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import DataTable

from src.models.pokemon import PokemonMoveRef
from src.models.move import Move


class MovesTab(VerticalScroll):
    """Tab content showing a Pokemon's move list in a DataTable."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._move_details: dict[str, Move] = {}
        self._table: DataTable | None = None

    def compose(self) -> ComposeResult:
        self._table = DataTable(
            cursor_type="row",
            zebra_stripes=True,
            show_header=True,
        )
        yield self._table

    def on_mount(self) -> None:
        if self._table:
            self._table.add_columns("Move", "Type", "Power", "Acc", "PP", "Level", "Method")
            # Add test row
            self._table.add_row("TEST", "Fire", "100", "95", "15", "1", "Level Up")
            self.app.notify("Test row added to moves table", timeout=3)

    def load_moves(
        self,
        moves: list[PokemonMoveRef],
        move_details: dict[str, Move] | None = None,
    ) -> None:
        """Populate the moves DataTable."""
        if not self._table:
            self.app.notify("ERROR: Table not found!", severity="error", timeout=5)
            return

        self.app.notify(f"Loading {len(moves)} moves", timeout=2)

        # Clear existing rows
        self._table.clear(columns=False)
        self._move_details = move_details or {}

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

            self._table.add_row(name, move_type, power, accuracy, pp, level, method)

        self.app.notify(f"✓ Table has {self._table.row_count} rows", timeout=2)
