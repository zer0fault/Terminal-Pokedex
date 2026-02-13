"""Detail panel showing selected Pokemon information."""
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal, VerticalScroll
from textual.widgets import Static, TabbedContent, TabPane

from src.widgets.sprite_display import SpriteDisplay
from src.widgets.type_badge import TypeBadge
from src.widgets.stats_tab import StatsTab
from src.widgets.moves_tab import MovesTab
from src.widgets.evolution_tab import EvolutionTab
from src.widgets.abilities_tab import AbilitiesTab
from src.models.pokemon import PokemonDetail
from src.models.species import PokemonSpecies
from src.models.evolution import EvolutionChain
from src.models.ability import Ability
from src.constants import GENERATION_MAP


class DetailPanel(Vertical):
    """Right panel showing detailed Pokemon information."""

    def compose(self) -> ComposeResult:
        with Horizontal(id="sprite-and-info"):
            yield SpriteDisplay()
            with Vertical(id="pokemon-info"):
                yield Static("", id="pokemon-name")
                yield Static("", id="pokemon-types")
                yield Static("", id="pokemon-details")
        yield Static("", id="flavor-text")
        with TabbedContent(id="detail-tabs"):
            with TabPane("Stats"):
                yield StatsTab()
            with TabPane("Moves"):
                yield MovesTab()
            with TabPane("Evolution"):
                yield EvolutionTab()
            with TabPane("Abilities"):
                yield AbilitiesTab()

    def on_mount(self) -> None:
        self.show_empty_state()

    def show_empty_state(self) -> None:
        """Show placeholder when no Pokemon is selected."""
        self.query_one("#pokemon-name", Static).update(
            "[dim]Select a Pokemon from the list[/dim]"
        )
        self.query_one("#pokemon-types", Static).update("")
        self.query_one("#pokemon-details", Static).update("")
        self.query_one("#flavor-text", Static).update("")
        self.query_one(SpriteDisplay).clear_sprite()

    def load_pokemon(
        self,
        detail: PokemonDetail,
        species: PokemonSpecies | None = None,
        sprite_pixels=None,
    ) -> None:
        """Load Pokemon detail into the panel."""
        name_widget = self.query_one("#pokemon-name", Static)
        name_widget.update(f"[bold]{detail.name.title()}[/bold] #{detail.id:04d}")

        types_widget = self.query_one("#pokemon-types", Static)
        type_names = [t.name for t in detail.types]
        types_widget.update(" ".join(type_names))

        details_widget = self.query_one("#pokemon-details", Static)
        height_m = detail.height / 10
        weight_kg = detail.weight / 10
        gen_text = ""
        if species:
            gen_text = GENERATION_MAP.get(species.generation, "Unknown")
        details_widget.update(
            f"Height: {height_m:.1f}m  |  Weight: {weight_kg:.1f}kg  |  {gen_text}"
        )

        flavor_widget = self.query_one("#flavor-text", Static)
        if species and species.flavor_text:
            flavor_widget.update(f'"{species.flavor_text}"')
        else:
            flavor_widget.update("")

        sprite_display = self.query_one(SpriteDisplay)
        sprite_display.set_sprite(sprite_pixels)

        stats_tab = self.query_one(StatsTab)
        stats_tab.load_stats(detail.stats)

        moves_tab = self.query_one(MovesTab)
        moves_tab.load_moves(detail.moves)

    def load_evolution(self, chain: EvolutionChain, current_name: str) -> None:
        """Load evolution chain into the Evolution tab."""
        evo_tab = self.query_one(EvolutionTab)
        if chain.root:
            evo_tab.load_chain(chain, current_name)
        else:
            evo_tab.show_no_evolution()

    def load_abilities(
        self,
        detail: PokemonDetail,
        ability_details: dict[str, Ability],
    ) -> None:
        """Load abilities into the Abilities tab."""
        abilities_tab = self.query_one(AbilitiesTab)
        abilities_tab.load_abilities(detail.abilities, ability_details)
