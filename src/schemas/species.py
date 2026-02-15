"""Pydantic schemas for Pokemon species API responses."""
from typing import Optional
from pydantic import BaseModel, Field


class FlavorTextEntrySchema(BaseModel):
    """Schema for flavor text entry."""
    flavor_text: str
    language: dict[str, str]
    version: dict[str, str]


class SpeciesSchema(BaseModel):
    """Schema for Pokemon species response from /pokemon-species/{id}."""
    id: int = Field(ge=1)
    name: str = Field(min_length=1)
    order: int
    gender_rate: int = Field(ge=-1, le=8)  # -1 = genderless, 0-8 = female ratio
    capture_rate: int = Field(ge=0, le=255)
    base_happiness: int = Field(ge=0, le=255)
    is_baby: bool
    is_legendary: bool
    is_mythical: bool
    hatch_counter: int = Field(ge=0)
    has_gender_differences: bool
    forms_switchable: bool
    growth_rate: dict[str, str]
    egg_groups: list[dict[str, str]]
    generation: dict[str, str]
    flavor_text_entries: list[FlavorTextEntrySchema]
    evolution_chain: Optional[dict[str, str]] = None
