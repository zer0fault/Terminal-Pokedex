"""Pokemon form data model."""
from dataclasses import dataclass


@dataclass(slots=True)
class PokemonFormSprites:
    """Sprites for a specific Pokemon form."""
    front_default: str | None = None
    front_shiny: str | None = None
    back_default: str | None = None
    back_shiny: str | None = None


@dataclass(slots=True)
class PokemonForm:
    """Data for a specific Pokemon form variant."""
    id: int
    name: str
    form_name: str
    is_default: bool
    is_battle_only: bool
    is_mega: bool
    order: int
    sprites: PokemonFormSprites
    types: list[str]  # Type names like ["fairy"]
