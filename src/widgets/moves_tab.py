"""Moves tab with a sortable DataTable."""
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import DataTable

from src.models.pokemon import PokemonMoveRef
from src.models.move import Move


class MovesTab(Vertical):
    """Tab content showing a Pokemon's move list in a DataTable."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._move_details: dict[str, Move] = {}

    def compose(self) -> ComposeResult:
        table = DataTable(id="moves-table", cursor_type="row", zebra_stripes=True)
        yield table

    def on_mount(self) -> None:
        table = self.query_one("#moves-table", DataTable)
        table.add_columns("Move", "Type", "Power", "Acc", "PP", "Level", "Method")

    def load_moves(
        self,
        moves: list[PokemonMoveRef],
        move_details: dict[str, Move] | None = None,
    ) -> None:
        """Populate the moves DataTable."""
        import sys
        print(f"DEBUG: load_moves called with {len(moves)} moves", file=sys.stderr, flush=True)

        table = self.query_one("#moves-table", DataTable)
        print(f"DEBUG: Found table, clearing...", file=sys.stderr, flush=True)
        table.clear()
        self._move_details = move_details or {}

        level_up = sorted(
            [m for m in moves if m.learn_method == "level-up"],
            key=lambda m: m.level_learned_at,
        )
        others = sorted(
            [m for m in moves if m.learn_method != "level-up"],
            key=lambda m: (m.learn_method, m.name),
        )

        rows_added = 0
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

            table.add_row(name, move_type, power, accuracy, pp, level, method)
            rows_added += 1

        print(f"DEBUG: Added {rows_added} rows to table. Row count: {table.row_count}", file=sys.stderr, flush=True)
