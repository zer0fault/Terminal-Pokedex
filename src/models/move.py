"""Move data models."""
from dataclasses import dataclass


@dataclass(slots=True)
class Move:
    """Full move data from /move/{id}."""
    id: int
    name: str
    power: int | None
    accuracy: int | None
    pp: int
    priority: int
    type_name: str
    damage_class: str  # physical, special, status
    effect_chance: int | None
    effect: str
    short_effect: str
    target: str
    ailment: str | None
    category: str
