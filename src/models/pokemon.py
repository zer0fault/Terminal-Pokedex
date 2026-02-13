"""Pokemon data models."""
from dataclasses import dataclass, field


@dataclass(slots=True)
class PokemonSummary:
    """Lightweight Pokemon for the list view."""
    id: int
    name: str
    url: str


@dataclass(slots=True)
class PokemonStat:
    """A single base stat."""
    name: str
    base_stat: int
    effort: int


@dataclass(slots=True)
class PokemonType:
    """A Pokemon's type slot."""
    slot: int
    name: str


@dataclass(slots=True)
class PokemonAbilityRef:
    """Reference to an ability on a Pokemon."""
    name: str
    is_hidden: bool
    slot: int


@dataclass(slots=True)
class PokemonMoveRef:
    """Reference to a move learned by a Pokemon."""
    name: str
    level_learned_at: int
    learn_method: str
    version_group: str


@dataclass(slots=True)
class PokemonDetail:
    """Full Pokemon data from /pokemon/{id}."""
    id: int
    name: str
    height: int
    weight: int
    base_experience: int | None
    sprite_url: str | None
    stats: list[PokemonStat] = field(default_factory=list)
    types: list[PokemonType] = field(default_factory=list)
    abilities: list[PokemonAbilityRef] = field(default_factory=list)
    moves: list[PokemonMoveRef] = field(default_factory=list)
