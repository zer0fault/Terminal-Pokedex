"""Breeding and training info tab."""
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Static
from rich.text import Text

from src.models.species import PokemonSpecies
from src.models.pokemon import PokemonDetail


class BreedingTab(VerticalScroll):
    """Tab content showing breeding and training information."""

    def compose(self) -> ComposeResult:
        yield Static("Select a Pokemon to view breeding info", id="breeding-content")

    def load_data(self, detail: PokemonDetail, species: PokemonSpecies) -> None:
        """Populate breeding and training information."""
        content = self.query_one("#breeding-content", Static)
        text = Text()

        # Breeding section
        text.append("BREEDING\n", style="bold underline")
        text.append("\n")

        # Egg groups
        if species.egg_groups:
            egg_groups_str = ", ".join(
                eg.replace("-", " ").title() for eg in species.egg_groups
            )
            text.append(f"  Egg Groups: ", style="bold")
            text.append(f"{egg_groups_str}\n")
        else:
            text.append(f"  Egg Groups: ", style="bold")
            text.append("None\n", style="dim")

        # Gender ratio
        text.append(f"  Gender Ratio: ", style="bold")
        if species.gender_rate == -1:
            text.append("Genderless\n", style="dim")
        else:
            female_pct = (species.gender_rate / 8) * 100
            male_pct = 100 - female_pct
            text.append(f"♀ {female_pct:.1f}% / ♂ {male_pct:.1f}%\n")

        # Hatch counter
        text.append(f"  Egg Cycles: ", style="bold")
        text.append(f"{species.hatch_counter}\n")
        steps = species.hatch_counter * 257
        text.append(f"  Steps to Hatch: ", style="bold")
        text.append(f"{steps:,}\n", style="dim")

        text.append("\n")

        # Training section
        text.append("TRAINING\n", style="bold underline")
        text.append("\n")

        # Base happiness
        text.append(f"  Base Happiness: ", style="bold")
        text.append(f"{species.base_happiness}\n")

        # Capture rate
        text.append(f"  Capture Rate: ", style="bold")
        text.append(f"{species.capture_rate}", )
        capture_chance = (species.capture_rate / 255) * 100
        text.append(f" ({capture_chance:.1f}% with full HP Poké Ball)\n", style="dim")

        # Base experience
        text.append(f"  Base Experience: ", style="bold")
        if detail.base_experience:
            text.append(f"{detail.base_experience}\n")
        else:
            text.append("N/A\n", style="dim")

        # Growth rate
        text.append(f"  Growth Rate: ", style="bold")
        growth_display = species.growth_rate.replace("-", " ").title()
        text.append(f"{growth_display}\n")

        text.append("\n")

        # Held items section
        if detail.held_items:
            text.append("HELD ITEMS\n", style="bold underline")
            text.append("\n")
            for held_item in detail.held_items:
                item_name = held_item.name.replace("-", " ").title()
                text.append(f"  • {item_name}", style="bold")
                if held_item.rarity > 0:
                    text.append(f" ({held_item.rarity}% chance)\n", style="dim")
                else:
                    text.append("\n")
        else:
            text.append("HELD ITEMS\n", style="bold underline")
            text.append("\n  ")
            text.append("This Pokemon does not hold items in the wild.\n", style="dim")

        content.update(text)
