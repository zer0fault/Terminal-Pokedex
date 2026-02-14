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
            # Phase 1: Fetch core Pokemon data
            detail = await self._cache.get_pokemon_detail(event.pokemon_id)

            # Fetch species using the species_id (handles form variants correctly)
            species = await self._cache.get_species(detail.species_id)

            # Download and render all sprite variants in parallel
            sprite_variants = {}
            if detail.sprites:
                sprite_mapping = {
                    "front_default": detail.sprites.front_default,
                    "front_shiny": detail.sprites.front_shiny,
                    "back_default": detail.sprites.back_default,
                    "back_shiny": detail.sprites.back_shiny,
                }

                # Download all sprites in parallel
                download_tasks = []
                for variant_name, url in sprite_mapping.items():
                    if url:
                        sprite_path = SPRITES_DIR / f"{event.pokemon_id}_{variant_name}.png"
                        if not sprite_path.exists():
                            download_tasks.append(
                                self._sprite_downloader.download_sprite(url, sprite_path)
                            )

                if download_tasks:
                    await asyncio.gather(*download_tasks, return_exceptions=True)

                # Render all sprites (rendering is fast, can be sequential)
                for variant_name, url in sprite_mapping.items():
                    if url:
                        sprite_path = SPRITES_DIR / f"{event.pokemon_id}_{variant_name}.png"
                        if sprite_path.exists():
                            pixels = self._sprite_renderer.render(sprite_path)
                            sprite_variants[variant_name] = pixels

            detail_panel.load_pokemon(detail, species, sprite_variants)

            # Phase 2: Fetch all supplementary data in parallel
            # Build task list for evolution, abilities, moves, and types
            tasks = []
            task_labels = []

            # Evolution chain task
            if species.evolution_chain_id:
                tasks.append(self._cache.get_evolution_chain(species.evolution_chain_id))
                task_labels.append(("evolution", None))
            else:
                tasks.append(None)
                task_labels.append(("evolution", None))

            # Ability tasks
            for ability_ref in detail.abilities:
                tasks.append(self._cache.get_ability(ability_ref.name))
                task_labels.append(("ability", ability_ref.name))

            # Move tasks (first 20)
            for move_ref in detail.moves[:20]:
                tasks.append(self._cache.get_move(move_ref.name))
                task_labels.append(("move", move_ref.name))

            # Type tasks
            for poke_type in detail.types:
                tasks.append(self._cache.get_type(poke_type.name))
                task_labels.append(("type", poke_type.name))

            # Execute all tasks in parallel
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Process results
            evolution_chain = None
            ability_details = {}
            move_details = {}
            type_data = {}
            ability_failed = 0
            move_failed = 0
            type_failed = 0

            for (data_type, name), result in zip(task_labels, results):
                if isinstance(result, Exception):
                    # Log the failure
                    if data_type == "ability":
                        ability_failed += 1
                        self.log.warning(f"Failed to load ability {name}: {result}")
                    elif data_type == "move":
                        move_failed += 1
                        self.log.warning(f"Failed to load move {name}: {result}")
                    elif data_type == "type":
                        type_failed += 1
                        self.log.warning(f"Failed to load type {name}: {result}")
                    elif data_type == "evolution":
                        self.log.warning(f"Failed to load evolution chain: {result}")
                else:
                    # Store the successful result
                    if data_type == "evolution" and result is not None:
                        evolution_chain = result
                    elif data_type == "ability":
                        ability_details[name] = result
                    elif data_type == "move":
                        move_details[name] = result
                    elif data_type == "type":
                        type_data[name] = result

            # Log batch failures
            if ability_failed > 0:
                self.log.error(f"Failed to load {ability_failed} abilities for {event.pokemon_name}")
            if move_failed > 0:
                self.log.error(f"Failed to load {move_failed} moves for {event.pokemon_name}")
            if type_failed > 0:
                self.log.error(f"Failed to load {type_failed} types for {event.pokemon_name}")

            # Load data into detail panel
            if evolution_chain:
                detail_panel.load_evolution(evolution_chain, event.pokemon_name)

            if ability_details:
                detail_panel.load_abilities(detail, ability_details)

            if move_details:
                detail_panel.load_move_details(detail, move_details)

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
