"""Cache manager orchestrating API calls and database caching."""
from src.api.client import PokeAPIClient
from src.api.endpoints import (
    pokemon_list_url, pokemon_detail_url, species_url,
    evolution_chain_url, ability_url, move_url, type_url,
)
from src.api.parsers import (
    parse_pokemon_list, parse_pokemon_detail, parse_pokemon_species,
    parse_evolution_chain, parse_ability, parse_move, parse_type_effectiveness,
)
from src.cache.database import CacheDatabase
from src.models.pokemon import PokemonSummary, PokemonDetail
from src.models.species import PokemonSpecies
from src.models.evolution import EvolutionChain
from src.models.ability import Ability
from src.models.move import Move
from src.models.type_info import TypeEffectiveness
from src.constants import (
    CACHE_TTL_POKEMON_DETAIL, CACHE_TTL_SPECIES,
    CACHE_TTL_EVOLUTION, CACHE_TTL_ABILITY,
)


class CacheManager:
    """Orchestrates API fetching with SQLite caching.

    All public methods are async. They check the cache first,
    and only hit the API if the cache is stale or missing.
    """

    def __init__(self) -> None:
        self._api = PokeAPIClient()
        self._db = CacheDatabase()
        self._initialized = False

    async def initialize(self) -> None:
        if not self._initialized:
            await self._db.initialize()
            self._initialized = True

    async def get_pokemon_list(self) -> list[PokemonSummary]:
        """Get the full Pokemon list (cached)."""
        await self.initialize()
        cached = await self._db.get_pokemon_list()
        if cached:
            return [
                PokemonSummary(id=p["id"], name=p["name"], url=p["url"])
                for p in cached
            ]
        data = await self._api.get_json(pokemon_list_url(limit=2000))
        summaries = parse_pokemon_list(data)
        await self._db.save_pokemon_list(
            [{"id": s.id, "name": s.name, "url": s.url} for s in summaries]
        )
        return summaries

    async def get_pokemon_detail(self, pokemon_id: int) -> PokemonDetail:
        """Get full Pokemon detail (cached)."""
        await self.initialize()
        cached = await self._db.get_cached_json(
            "pokemon_detail", pokemon_id, CACHE_TTL_POKEMON_DETAIL
        )
        if cached:
            return parse_pokemon_detail(cached)
        data = await self._api.get_json(pokemon_detail_url(pokemon_id))
        await self._db.save_cached_json("pokemon_detail", pokemon_id, data)
        return parse_pokemon_detail(data)

    async def get_species(self, pokemon_id: int) -> PokemonSpecies:
        """Get Pokemon species data (cached)."""
        await self.initialize()
        cached = await self._db.get_cached_json(
            "pokemon_species", pokemon_id, CACHE_TTL_SPECIES
        )
        if cached:
            return parse_pokemon_species(cached)
        data = await self._api.get_json(species_url(pokemon_id))
        await self._db.save_cached_json("pokemon_species", pokemon_id, data)
        return parse_pokemon_species(data)

    async def get_evolution_chain(self, chain_id: int) -> EvolutionChain:
        """Get evolution chain (cached)."""
        await self.initialize()
        cached = await self._db.get_cached_json(
            "evolution_chain", chain_id, CACHE_TTL_EVOLUTION
        )
        if cached:
            return parse_evolution_chain(cached)
        data = await self._api.get_json(evolution_chain_url(chain_id))
        await self._db.save_cached_json("evolution_chain", chain_id, data)
        return parse_evolution_chain(data)

    async def get_ability(self, ability_name: str) -> Ability:
        """Get ability details (cached)."""
        await self.initialize()
        data = await self._api.get_json(ability_url(ability_name))
        ability = parse_ability(data)
        await self._db.save_cached_json(
            "ability", ability.id, data, name=ability_name
        )
        return ability

    async def get_move(self, move_name: str) -> Move:
        """Get move details (cached)."""
        await self.initialize()
        data = await self._api.get_json(move_url(move_name))
        move = parse_move(data)
        await self._db.save_cached_json(
            "move", move.id, data, name=move_name
        )
        return move

    async def get_type(self, type_name: str) -> TypeEffectiveness:
        """Get type effectiveness data (cached)."""
        await self.initialize()
        data = await self._api.get_json(type_url(type_name))
        type_eff = parse_type_effectiveness(data)
        await self._db.save_cached_json(
            "type", type_eff.id, data, name=type_name
        )
        return type_eff

    async def get_pokemon_form(self, form_url: str) -> 'PokemonForm':
        """Get Pokemon form details (cached)."""
        from src.models.form import PokemonForm
        from src.api.parsers import parse_pokemon_form

        await self.initialize()
        data = await self._api.get_json(form_url)
        form = parse_pokemon_form(data)
        await self._db.save_cached_json(
            "form", form.id, data, name=form.name
        )
        return form

    async def close(self) -> None:
        """Clean up resources."""
        await self._api.close()
        await self._db.close()
