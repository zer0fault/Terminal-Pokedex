"""Tests for API response parsers."""
import json
from pathlib import Path

import pytest

from src.api.parsers import (
    parse_id_from_url,
    parse_pokemon_detail,
    parse_pokemon_species,
    parse_ability,
    parse_move,
)


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(filename: str) -> dict:
    """Load JSON fixture file."""
    with open(FIXTURES_DIR / filename) as f:
        return json.load(f)


class TestParseIdFromUrl:
    """Test URL ID extraction."""

    def test_pokemon_url(self):
        url = "https://pokeapi.co/api/v2/pokemon/25/"
        assert parse_id_from_url(url) == 25

    def test_species_url(self):
        url = "https://pokeapi.co/api/v2/pokemon-species/150/"
        assert parse_id_from_url(url) == 150

    def test_url_without_trailing_slash(self):
        url = "https://pokeapi.co/api/v2/pokemon/1"
        assert parse_id_from_url(url) == 1

    def test_form_variant_url(self):
        url = "https://pokeapi.co/api/v2/pokemon/10001/"
        assert parse_id_from_url(url) == 10001


class TestParsePokemonDetail:
    """Test Pokemon detail parsing."""

    def test_parse_valid_pokemon(self):
        data = load_fixture("pokemon_detail.json")
        result = parse_pokemon_detail(data)

        assert result.id == 25
        assert result.name == "pikachu"
        assert result.height == 4
        assert result.weight == 60
        assert result.species_id == 25

    def test_stats_parsed_correctly(self):
        data = load_fixture("pokemon_detail.json")
        result = parse_pokemon_detail(data)

        assert len(result.stats) == 3
        assert result.stats[0].name == "hp"
        assert result.stats[0].base_stat == 35
        assert result.stats[2].name == "speed"
        assert result.stats[2].base_stat == 90

    def test_types_parsed_correctly(self):
        data = load_fixture("pokemon_detail.json")
        result = parse_pokemon_detail(data)

        assert len(result.types) == 1
        assert result.types[0].name == "electric"
        assert result.types[0].slot == 1

    def test_abilities_include_hidden(self):
        data = load_fixture("pokemon_detail.json")
        result = parse_pokemon_detail(data)

        assert len(result.abilities) == 2
        assert not result.abilities[0].is_hidden
        assert result.abilities[1].is_hidden
        assert result.abilities[1].name == "lightning-rod"

    def test_sprites_prefer_official_artwork(self):
        data = load_fixture("pokemon_detail.json")
        result = parse_pokemon_detail(data)

        # Should use official artwork (higher quality)
        assert "official-artwork" in result.sprite_url
        assert result.sprites.front_default is not None
        assert result.sprites.front_shiny is not None

    def test_species_id_extracted_from_url(self):
        """Test that species_id is extracted from species URL, not pokemon ID."""
        data = load_fixture("pokemon_detail.json")
        # Simulate a form variant by changing the pokemon ID
        data["id"] = 10001
        result = parse_pokemon_detail(data)

        # species_id should still be 25 from the URL, not 10001
        assert result.species_id == 25
        assert result.id == 10001

    def test_invalid_schema_raises_error(self):
        """Test that invalid data raises a clear error."""
        data = {"id": "not-a-number", "name": "invalid"}

        with pytest.raises(ValueError, match="Invalid Pokemon detail response"):
            parse_pokemon_detail(data)


class TestParsePokemonSpecies:
    """Test Pokemon species parsing."""

    def test_parse_valid_species(self):
        data = load_fixture("pokemon_species.json")
        result = parse_pokemon_species(data)

        assert result.id == 25
        assert result.name == "pikachu"
        assert "Mouse" in result.genus and "mon" in result.genus
        assert result.generation == "generation-i"

    def test_flavor_text_cleaned(self):
        """Test that flavor text has form feeds and newlines removed."""
        data = load_fixture("pokemon_species.json")
        result = parse_pokemon_species(data)

        # Should have whitespace normalized
        assert "\f" not in result.flavor_text
        assert "\n" not in result.flavor_text
        assert "  " not in result.flavor_text  # No double spaces

    def test_evolution_chain_id_extracted(self):
        data = load_fixture("pokemon_species.json")
        result = parse_pokemon_species(data)

        assert result.evolution_chain_id == 10

    def test_egg_groups_parsed(self):
        data = load_fixture("pokemon_species.json")
        result = parse_pokemon_species(data)

        assert len(result.egg_groups) == 2
        assert "field" in result.egg_groups
        assert "fairy" in result.egg_groups

    def test_legendary_flags(self):
        data = load_fixture("pokemon_species.json")
        result = parse_pokemon_species(data)

        assert not result.is_legendary
        assert not result.is_mythical
        assert not result.is_baby


class TestParseAbility:
    """Test ability parsing."""

    def test_parse_valid_ability(self):
        data = load_fixture("ability.json")
        result = parse_ability(data)

        assert result.id == 9
        assert result.name == "static"
        assert "30% chance" in result.short_effect
        assert len(result.effect) > len(result.short_effect)

    def test_flavor_text_extracted(self):
        data = load_fixture("ability.json")
        result = parse_ability(data)

        assert result.flavor_text == "May paralyze on contact."


class TestParseMove:
    """Test move parsing."""

    def test_parse_valid_move(self):
        data = load_fixture("move.json")
        result = parse_move(data)

        assert result.id == 84
        assert result.name == "thunder-shock"
        assert result.power == 40
        assert result.accuracy == 100
        assert result.pp == 30

    def test_move_type_and_class(self):
        data = load_fixture("move.json")
        result = parse_move(data)

        assert result.type_name == "electric"
        assert result.damage_class == "special"

    def test_effect_entries_parsed(self):
        data = load_fixture("move.json")
        result = parse_move(data)

        assert "paralyze" in result.short_effect.lower()
        assert result.effect_chance == 10

    def test_move_meta_parsed(self):
        data = load_fixture("move.json")
        result = parse_move(data)

        assert result.ailment == "paralysis"
        assert result.category == "damage+ailment"
