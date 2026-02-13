"""Pokemon list panel with search and scrollable list."""
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, OptionList
from textual.widgets.option_list import Option
from textual.message import Message

from src.widgets.search_bar import SearchBar
from src.widgets.filter_bar import FilterBar
from src.models.pokemon import PokemonSummary
from src.constants import TYPE_ABBREVIATIONS


class PokemonListPanel(Vertical):
    """Left panel: search bar + filter bar + scrollable Pokemon list."""

    class PokemonSelected(Message):
        def __init__(self, pokemon_id: int, pokemon_name: str) -> None:
            super().__init__()
            self.pokemon_id = pokemon_id
            self.pokemon_name = pokemon_name

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._all_pokemon: list[PokemonSummary] = []
        self._filtered_pokemon: list[PokemonSummary] = []
        self._current_search: str = ""
        self._current_gen: str | None = None
        self._current_type: str | None = None
        self._pokemon_types: dict[int, list[str]] = {}
        self._pokemon_gens: dict[int, str] = {}

    def compose(self) -> ComposeResult:
        yield SearchBar()
        yield FilterBar(id="filter-bar")
        yield OptionList(id="pokemon-option-list")
        yield Static("Loading Pokemon...", id="list-status")

    def load_pokemon(self, pokemon_list: list[PokemonSummary]) -> None:
        """Load the full Pokemon list into the panel."""
        self._all_pokemon = pokemon_list
        self._apply_filters()

    def set_type_data(self, pokemon_id: int, types: list[str]) -> None:
        """Update type data for a single Pokemon."""
        self._pokemon_types[pokemon_id] = types

    def set_gen_data(self, pokemon_id: int, generation: str) -> None:
        """Update generation data for a single Pokemon."""
        self._pokemon_gens[pokemon_id] = generation

    def _apply_filters(self) -> None:
        """Filter Pokemon list by search query, generation, and type."""
        filtered = self._all_pokemon

        if self._current_search:
            query = self._current_search.lower()
            filtered = [
                p for p in filtered
                if query in p.name.lower() or query in str(p.id)
            ]

        if self._current_type and self._pokemon_types:
            filtered = [
                p for p in filtered
                if self._current_type in self._pokemon_types.get(p.id, [])
            ]

        if self._current_gen and self._pokemon_gens:
            filtered = [
                p for p in filtered
                if self._pokemon_gens.get(p.id) == self._current_gen
            ]

        self._filtered_pokemon = filtered
        self._update_option_list()

    def _update_option_list(self) -> None:
        """Rebuild the OptionList with filtered Pokemon."""
        option_list = self.query_one("#pokemon-option-list", OptionList)
        option_list.clear_options()

        for pokemon in self._filtered_pokemon:
            label = f"#{pokemon.id:04d} {pokemon.name.title()}"
            option_list.add_option(Option(label, id=str(pokemon.id)))

        status = self.query_one("#list-status", Static)
        total = len(self._all_pokemon)
        shown = len(self._filtered_pokemon)
        if shown == total:
            status.update(f"[dim]{total} Pokemon[/dim]")
        else:
            status.update(f"[dim]{shown} of {total} Pokemon[/dim]")

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option_id is not None:
            pokemon_id = int(event.option_id)
            pokemon = next(
                (p for p in self._filtered_pokemon if p.id == pokemon_id),
                None,
            )
            if pokemon:
                self.post_message(self.PokemonSelected(pokemon.id, pokemon.name))

    def on_search_bar_search_changed(self, event: SearchBar.SearchChanged) -> None:
        self._current_search = event.query
        self._apply_filters()

    def on_filter_bar_filters_changed(self, event: FilterBar.FiltersChanged) -> None:
        self._current_gen = event.generation
        self._current_type = event.type_name
        self._apply_filters()
