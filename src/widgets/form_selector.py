"""Form selector widget for Pokemon with multiple forms."""
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Select, Static
from textual.message import Message


class FormSelector(Horizontal):
    """Allows selection of Pokemon forms when multiple exist."""

    class FormChanged(Message):
        """Posted when user selects a different form."""
        def __init__(self, form_name: str, form_url: str) -> None:
            super().__init__()
            self.form_name = form_name
            self.form_url = form_url

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._forms: list[tuple[str, str]] = []  # (name, url) tuples

    def compose(self) -> ComposeResult:
        yield Static("Form:", id="form-label")
        yield Select([], id="form-select", allow_blank=False)

    def load_forms(self, forms: list[tuple[str, str]]) -> None:
        """Load available forms into the selector.

        Args:
            forms: List of (form_name, form_url) tuples
        """
        self._forms = forms

        if len(forms) <= 1:
            # Hide selector if only one form
            self.display = False
            return

        self.display = True
        select = self.query_one("#form-select", Select)

        # Create options with readable names
        options = []
        for form_name, form_url in forms:
            # Convert "deoxys-attack" to "Attack"
            # Convert "wormadam-sandy" to "Sandy"
            # Convert "alcremie-vanilla-cream-strawberry-sweet" to "Vanilla Cream Strawberry Sweet"
            display_name = self._format_form_name(form_name)
            options.append((display_name, form_name))

        select.set_options(options)
        if options:
            select.value = options[0][1]  # Select first form by default

    def _format_form_name(self, form_name: str) -> str:
        """Format form name for display."""
        # Remove the base Pokemon name prefix if present
        parts = form_name.split("-", 1)
        if len(parts) > 1:
            # Use everything after the first dash
            display = parts[1].replace("-", " ").title()
        else:
            display = form_name.replace("-", " ").title()

        return display

    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle form selection change."""
        if event.value:
            # Find the URL for the selected form
            for form_name, form_url in self._forms:
                if form_name == event.value:
                    self.post_message(self.FormChanged(form_name, form_url))
                    break
