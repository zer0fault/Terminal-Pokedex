"""Pokemon species data model."""
from dataclasses import dataclass


@dataclass(slots=True)
class PokemonSpecies:
    """Species data from /pokemon-species/{id}."""
    id: int
    name: str
    flavor_text: str
    genus: str
    generation: str
    habitat: str | None
    color: str
    evolution_chain_id: int
    is_legendary: bool
    is_mythical: bool
    is_baby: bool
