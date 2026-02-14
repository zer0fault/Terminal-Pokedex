"""Terminal Pokedex - A TUI for browsing Pokemon data."""
import asyncio
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Header, Footer
from textual.binding import Binding

from src.widgets.pokemon_list import PokemonListPanel
from src.screens.detail_panel import DetailPanel
from src.cache.manager import CacheManager
from src.sprites.downloader import SpriteDownloader
from src.sprites.renderer import SpriteRenderer
from src.constants import APP_NAME, APP_VERSION, DATA_DIR, SPRITES_DIR


class PokedexApp(App):
    """Terminal Pokedex TUI application."""

    CSS_PATH = "styles/pokedex.tcss"
    TITLE = f"{APP_NAME} v{APP_VERSION}"

    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("ctrl+c", "quit", "Quit", show=False),
        ("?", "help", "Help"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._cache = CacheManager()
        self._sprite_downloader = SpriteDownloader()
        self._sprite_renderer = SpriteRenderer()

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="main-layout"):
            yield PokemonListPanel()
            yield DetailPanel()
        yield Footer()

    async def on_mount(self) -> None:
        """Initialize the app and load Pokemon list."""
        DATA_DIR.mkdir(exist_ok=True)
        SPRITES_DIR.mkdir(exist_ok=True)

        await self._cache.initialize()
        pokemon_list = await self._cache.get_pokemon_list()

        list_panel = self.query_one(PokemonListPanel)
        list_panel.load_pokemon(pokemon_list)

        self._load_metadata_in_background(pokemon_list)

    def _load_metadata_in_background(self, pokemon_list) -> None:
        """Load type and generation data for all Pokemon in the background."""
        async def load_metadata():
            list_panel = self.query_one(PokemonListPanel)
            failed_count = 0
            total = len(pokemon_list)

            for idx, pokemon in enumerate(pokemon_list, 1):
                try:
                    detail = await self._cache.get_pokemon_detail(pokemon.id)
                    species = await self._cache.get_species(pokemon.id)
                    type_names = [t.name for t in detail.types]
                    list_panel.set_type_data(pokemon.id, type_names)
                    list_panel.set_gen_data(pokemon.id, species.generation)

                    # Update status every 50 Pokemon
                    if idx % 50 == 0:
                        list_panel.update_status(f"Loading metadata... {idx}/{total}")
                except Exception as e:
                    failed_count += 1
                    self.log.warning(f"Failed to load metadata for {pokemon.name} (#{pokemon.id}): {e}")
                    # Continue loading others instead of stopping

            if failed_count > 0:
                self.log.error(f"Failed to load metadata for {failed_count}/{total} Pokemon")

            list_panel.update_status(f"{total} Pokemon")

        asyncio.create_task(load_metadata())

    async def on_pokemon_list_panel_pokemon_selected(
        self, event: PokemonListPanel.PokemonSelected
    ) -> None:
        """Handle Pokemon selection from the list."""
        detail_panel = self.query_one(DetailPanel)

        try:
            detail = await self._cache.get_pokemon_detail(event.pokemon_id)
            species = await self._cache.get_species(event.pokemon_id)

            # Download and render all sprite variants
            sprite_variants = {}
            if detail.sprites:
                sprite_mapping = {
                    "front_default": detail.sprites.front_default,
                    "front_shiny": detail.sprites.front_shiny,
                    "back_default": detail.sprites.back_default,
                    "back_shiny": detail.sprites.back_shiny,
                }

                for variant_name, url in sprite_mapping.items():
                    if url:
                        sprite_path = SPRITES_DIR / f"{event.pokemon_id}_{variant_name}.png"
                        if not sprite_path.exists():
                            await self._sprite_downloader.download_sprite(url, sprite_path)

                        if sprite_path.exists():
                            pixels = self._sprite_renderer.render(sprite_path)
                            sprite_variants[variant_name] = pixels

            detail_panel.load_pokemon(detail, species, sprite_variants)

            chain_id = species.evolution_chain_id
            if chain_id:
                evolution_chain = await self._cache.get_evolution_chain(chain_id)
                detail_panel.load_evolution(evolution_chain, event.pokemon_name)

            ability_details = {}
            ability_failed = 0
            for ability_ref in detail.abilities:
                try:
                    ability = await self._cache.get_ability(ability_ref.name)
                    ability_details[ability_ref.name] = ability
                except Exception as e:
                    ability_failed += 1
                    self.log.warning(f"Failed to load ability {ability_ref.name}: {e}")

            if ability_failed > 0:
                self.log.error(f"Failed to load {ability_failed} abilities for {event.pokemon_name}")

            detail_panel.load_abilities(detail, ability_details)

            # Fetch move details for first 20 moves (to avoid too many API calls)
            move_details = {}
            move_failed = 0
            for move_ref in detail.moves[:20]:
                try:
                    move = await self._cache.get_move(move_ref.name)
                    move_details[move_ref.name] = move
                except Exception as e:
                    move_failed += 1
                    self.log.warning(f"Failed to load move {move_ref.name}: {e}")

            if move_failed > 0:
                self.log.error(f"Failed to load {move_failed} moves for {event.pokemon_name}")

            if move_details:
                detail_panel.load_move_details(detail, move_details)

            # Fetch type effectiveness data
            type_data = {}
            for poke_type in detail.types:
                try:
                    type_info = await self._cache.get_type(poke_type.name)
                    type_data[poke_type.name] = type_info
                except Exception as e:
                    self.log.warning(f"Failed to fetch type {poke_type.name}: {e}")

            if type_data:
                detail_panel.load_type_matchups(detail, type_data)

        except Exception as e:
            self.notify(f"Error loading Pokemon: {e}", severity="error", timeout=5)

    async def on_unmount(self) -> None:
        """Clean up resources."""
        await self._cache.close()

    def action_help(self) -> None:
        """Show help information."""
        self.notify(
            "Use arrow keys to navigate, Enter to select, / to search, q to quit",
            title="Help",
            timeout=5,
        )


def main():
    """Run the Pokedex app."""
    app = PokedexApp()
    app.run()


if __name__ == "__main__":
    main()
