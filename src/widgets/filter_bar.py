"""Generation and type filter dropdowns."""
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Select
from textual.message import Message
from src.constants import TYPE_COLORS, GENERATION_MAP


class FilterBar(Horizontal):
    """Contains generation and type filter Select dropdowns."""

    class FiltersChanged(Message):
        def __init__(self, generation: str | None, type_name: str | None) -> None:
            super().__init__()
            self.generation = generation
            self.type_name = type_name

    def compose(self) -> ComposeResult:
        gen_options = [(display, key) for key, display in GENERATION_MAP.items()]
        yield Select(
            gen_options,
            prompt="All Gens",
            id="gen-filter",
            allow_blank=True,
        )

        type_options = [(name.title(), name) for name in sorted(TYPE_COLORS.keys())]
        yield Select(
            type_options,
            prompt="All Types",
            id="type-filter",
            allow_blank=True,
        )

    def on_select_changed(self, event: Select.Changed) -> None:
        gen_select = self.query_one("#gen-filter", Select)
        type_select = self.query_one("#type-filter", Select)
        self.post_message(self.FiltersChanged(
            generation=gen_select.value if gen_select.value != Select.BLANK else None,
            type_name=type_select.value if type_select.value != Select.BLANK else None,
        ))
