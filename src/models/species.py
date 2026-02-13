"""Pokemon species data model."""
from dataclasses import dataclass, field


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
    shape: str | None
    evolution_chain_id: int
    is_legendary: bool
    is_mythical: bool
    is_baby: bool
    # Breeding info
    egg_groups: list[str] = field(default_factory=list)
    gender_rate: int = -1  # -1 = genderless, 0-8 = female ratio (8 = 100% female)
    hatch_counter: int = 0
    # Training info
    growth_rate: str = ""
    base_happiness: int = 0
    capture_rate: int = 0
    # Forms
    forms_switchable: bool = False
