"""Ability data model."""
from dataclasses import dataclass


@dataclass(slots=True)
class Ability:
    """Full ability data from /ability/{id}."""
    id: int
    name: str
    effect: str
    short_effect: str
    flavor_text: str
