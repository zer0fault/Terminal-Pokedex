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
class PokemonHeldItem:
    """Item that can be held by wild Pokemon."""
    name: str
    rarity: int


@dataclass(slots=True)
class PokemonSprites:
    """Collection of sprite URLs for a Pokemon."""
    front_default: str | None = None
    front_shiny: str | None = None
    front_female: str | None = None
    front_shiny_female: str | None = None
    back_default: str | None = None
    back_shiny: str | None = None
    back_female: str | None = None
    back_shiny_female: str | None = None


@dataclass(slots=True)
class PokemonFormRef:
    """Reference to a Pokemon form."""
    name: str
    url: str


@dataclass(slots=True)
class PokemonDetail:
    """Full Pokemon data from /pokemon/{id}."""
    id: int
    name: str
    height: int
    weight: int
    base_experience: int | None
    is_default: bool
    order: int
    species_id: int  # The species ID (may differ from pokemon ID for forms)
    sprite_url: str | None
    sprites: PokemonSprites | None = None
    forms: list[PokemonFormRef] = field(default_factory=list)
    stats: list[PokemonStat] = field(default_factory=list)
    types: list[PokemonType] = field(default_factory=list)
    abilities: list[PokemonAbilityRef] = field(default_factory=list)
    moves: list[PokemonMoveRef] = field(default_factory=list)
    held_items: list[PokemonHeldItem] = field(default_factory=list)
