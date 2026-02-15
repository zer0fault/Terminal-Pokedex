"""Pydantic schemas for Pokemon API responses."""
from typing import Any, Optional
from pydantic import BaseModel, Field, field_validator


class StatSchema(BaseModel):
    """Schema for Pokemon stat."""
    stat: dict[str, Any]
    base_stat: int = Field(ge=0, le=255)
    effort: int = Field(ge=0)


class TypeSchema(BaseModel):
    """Schema for Pokemon type."""
    slot: int = Field(ge=1)
    type: dict[str, str]


class AbilitySchema(BaseModel):
    """Schema for Pokemon ability reference."""
    ability: dict[str, str]
    is_hidden: bool
    slot: int = Field(ge=1)


class MoveVersionDetailSchema(BaseModel):
    """Schema for move version group details."""
    level_learned_at: int = Field(ge=0)
    move_learn_method: dict[str, str]
    version_group: dict[str, str]


class MoveSchema(BaseModel):
    """Schema for Pokemon move reference."""
    move: dict[str, str]
    version_group_details: list[MoveVersionDetailSchema]


class SpriteSchema(BaseModel):
    """Schema for Pokemon sprites."""
    front_default: Optional[str] = None
    front_shiny: Optional[str] = None
    front_female: Optional[str] = None
    front_shiny_female: Optional[str] = None
    back_default: Optional[str] = None
    back_shiny: Optional[str] = None
    back_female: Optional[str] = None
    back_shiny_female: Optional[str] = None
    other: Optional[dict[str, Any]] = None


class FormRefSchema(BaseModel):
    """Schema for Pokemon form reference."""
    name: str
    url: str


class HeldItemSchema(BaseModel):
    """Schema for held item."""
    item: dict[str, str]
    version_details: list[dict[str, Any]]


class PokemonDetailSchema(BaseModel):
    """Schema for Pokemon detail response from /pokemon/{id}."""
    id: int = Field(ge=1)
    name: str = Field(min_length=1)
    height: int = Field(ge=0)
    weight: int = Field(ge=0)
    base_experience: Optional[int] = Field(default=None, ge=0)
    is_default: bool = True
    order: int
    species: dict[str, str]
    stats: list[StatSchema] = Field(min_length=1)  # Must have at least 1 stat
    types: list[TypeSchema] = Field(min_length=1)  # Must have at least 1 type
    abilities: list[AbilitySchema]
    moves: list[MoveSchema]
    sprites: SpriteSchema
    forms: list[FormRefSchema]
    held_items: list[HeldItemSchema] = Field(default_factory=list)

    @field_validator('name')
    @classmethod
    def name_must_be_lowercase(cls, v: str) -> str:
        """Validate Pokemon name is lowercase."""
        if not v.islower():
            raise ValueError('Pokemon name must be lowercase')
        return v

    @field_validator('species')
    @classmethod
    def species_must_have_url(cls, v: dict[str, str]) -> dict[str, str]:
        """Validate species has URL."""
        if 'url' not in v:
            raise ValueError('Species must have URL field')
        return v
