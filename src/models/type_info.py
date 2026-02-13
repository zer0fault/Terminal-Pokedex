"""Type effectiveness data model."""
from dataclasses import dataclass, field


@dataclass(slots=True)
class TypeEffectiveness:
    """Type damage relations from /type/{id}."""
    id: int
    name: str
    # Offensive: This type deals...
    double_damage_to: list[str] = field(default_factory=list)  # 2x damage
    half_damage_to: list[str] = field(default_factory=list)    # 0.5x damage
    no_damage_to: list[str] = field(default_factory=list)      # 0x damage
    # Defensive: This type takes...
    double_damage_from: list[str] = field(default_factory=list)  # Weak to
    half_damage_from: list[str] = field(default_factory=list)    # Resists
    no_damage_from: list[str] = field(default_factory=list)      # Immune to
