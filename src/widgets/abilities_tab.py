"""Abilities tab showing ability names and descriptions."""
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Static
from rich.text import Text

from src.models.pokemon import PokemonAbilityRef
from src.models.ability import Ability


class AbilitiesTab(VerticalScroll):
    """Tab content showing Pokemon abilities with descriptions."""

    def compose(self) -> ComposeResult:
        yield Static("Select a Pokemon to view abilities", id="abilities-content")

    def load_abilities(
        self,
        ability_refs: list[PokemonAbilityRef],
        ability_details: dict[str, Ability],
    ) -> None:
        content = self.query_one("#abilities-content", Static)
        text = Text()

        for ref in ability_refs:
            name = ref.name.replace("-", " ").title()
            text.append(f"\n  {name}", style="bold")
            if ref.is_hidden:
                text.append(" (Hidden)", style="dim italic")
            text.append("\n")

            detail = ability_details.get(ref.name)
            if detail and detail.short_effect:
                text.append(f"  {detail.short_effect}\n", style="")
            elif detail and detail.flavor_text:
                text.append(f"  {detail.flavor_text}\n", style="")
            else:
                text.append("  No description available.\n", style="dim")
            text.append("\n")

        if not ability_refs:
            text.append("[dim]No abilities found.[/dim]")

        content.update(text)
