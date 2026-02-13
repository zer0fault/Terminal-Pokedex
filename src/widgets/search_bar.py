"""Search input widget with debounced filtering."""
from textual.widgets import Input
from textual.message import Message


class SearchBar(Input):
    """Search input that emits a SearchChanged message after debounce."""

    class SearchChanged(Message):
        def __init__(self, query: str) -> None:
            super().__init__()
            self.query = query

    def __init__(self, **kwargs) -> None:
        super().__init__(
            placeholder="Search Pokemon...",
            id="search-input",
            **kwargs,
        )
        self._debounce_timer = None

    def on_input_changed(self, event: Input.Changed) -> None:
        if self._debounce_timer:
            self._debounce_timer.stop()
        self._debounce_timer = self.set_timer(
            0.3,
            lambda: self.post_message(self.SearchChanged(event.value)),
        )
