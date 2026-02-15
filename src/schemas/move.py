"""Pydantic schemas for move API responses."""
from typing import Optional
from pydantic import BaseModel, Field


class EffectEntrySchema(BaseModel):
    """Schema for move effect entry."""
    effect: str
    short_effect: str
    language: dict[str, str]


class MoveSchema(BaseModel):
    """Schema for move response from /move/{id}."""
    id: int = Field(ge=1)
    name: str = Field(min_length=1)
    accuracy: Optional[int] = Field(default=None, ge=0, le=100)
    effect_chance: Optional[int] = Field(default=None, ge=0, le=100)
    pp: int = Field(ge=0)
    priority: int = Field(ge=-8, le=8)
    power: Optional[int] = Field(default=None, ge=0)
    type: dict[str, str]
    damage_class: dict[str, str]
    effect_entries: list[EffectEntrySchema]
    target: dict[str, str]
    meta: Optional[dict] = None
