"""Moves tab with a sortable DataTable."""
from textual.widgets import DataTable

from src.models.pokemon import PokemonMoveRef
from src.models.move import Move


class MovesTab(DataTable):
    """Tab content showing a Pokemon's move list in a DataTable."""

    def __init__(self, **kwargs) -> None:
        super().__init__(
            cursor_type="row",
            zebra_stripes=True,
            show_header=True,
            show_row_labels=False,
            **kwargs
        )
        self._move_details: dict[str, Move] = {}

    def on_mount(self) -> None:
        self.add_columns("Move", "Type", "Power", "Acc", "PP", "Level", "Method")
        # Add a test row to verify display works
        self.add_row("TEST", "Fire", "100", "95", "15", "1", "Level Up")

    def load_moves(
        self,
        moves: list[PokemonMoveRef],
        move_details: dict[str, Move] | None = None,
    ) -> None:
        """Populate the moves DataTable."""
        self.app.notify(f"Loading {len(moves)} moves into table", timeout=2)

        # Clear existing rows
        self.clear(columns=False)
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

            # Get move details if available
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

            self.add_row(name, move_type, power, accuracy, pp, level, method)

        self.app.notify(f"✓ Table now has {self.row_count} rows", timeout=2)
