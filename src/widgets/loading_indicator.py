"""Loading spinner widget."""
from textual.widgets import Static


class LoadingIndicator(Static):
    """Displays a loading message."""

    def __init__(self, message: str = "Loading", **kwargs) -> None:
        super().__init__(f"[dim]{message}...[/dim]", **kwargs)
