"""Pydantic schemas for ability API responses."""
from pydantic import BaseModel, Field


class EffectEntrySchema(BaseModel):
    """Schema for effect entry."""
    effect: str
    short_effect: str
    language: dict[str, str]


class FlavorTextSchema(BaseModel):
    """Schema for flavor text."""
    flavor_text: str
    language: dict[str, str]
    version_group: dict[str, str]


class AbilitySchema(BaseModel):
    """Schema for ability response from /ability/{id}."""
    id: int = Field(ge=1)
    name: str = Field(min_length=1)
    is_main_series: bool
    generation: dict[str, str]
    effect_entries: list[EffectEntrySchema]
    flavor_text_entries: list[FlavorTextSchema]
