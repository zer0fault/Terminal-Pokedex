"""Evolution chain tab with visual tree display."""
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Static
from rich.text import Text

from src.models.evolution import EvolutionChain, EvolutionNode


class EvolutionTab(VerticalScroll):
    """Tab content showing the Pokemon's evolution chain."""

    def compose(self) -> ComposeResult:
        yield Static("", id="evo-content")

    def load_chain(self, chain: EvolutionChain, current_pokemon_name: str) -> None:
        content = self.query_one("#evo-content", Static)
        text = self._render_chain(chain.root, current_pokemon_name)
        content.update(text)

    def _render_chain(
        self, node: EvolutionNode, current_name: str, depth: int = 0
    ) -> Text:
        text = Text()
        indent = "    " * depth
        name_display = node.species_name.replace("-", " ").title()

        if node.species_name == current_name:
            text.append(f"{indent}")
            text.append(f">> {name_display} <<", style="bold reverse")
            text.append(f" #{node.species_id}\n", style="dim")
        else:
            text.append(f"{indent}")
            text.append(f"{name_display}", style="bold")
            text.append(f" #{node.species_id}\n", style="dim")

        for child in node.evolves_to:
            trigger_text = ""
            if child.triggers:
                trigger_text = child.triggers[0].display_text()

            arrow_indent = "    " * depth
            text.append(f"{arrow_indent}  |\n")
            text.append(f"{arrow_indent}  +--[{trigger_text}]-->  ", style="dim")
            child_text = self._render_chain(child, current_name, depth + 1)
            text.append_text(child_text)

        return text

    def show_no_evolution(self) -> None:
        content = self.query_one("#evo-content", Static)
        content.update("[dim]This Pokemon does not evolve.[/dim]")
