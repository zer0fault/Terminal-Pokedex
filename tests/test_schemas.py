"""Tests for Pydantic schema validation."""
import pytest
from pydantic import ValidationError

from src.schemas.pokemon import PokemonDetailSchema, StatSchema
from src.schemas.species import SpeciesSchema
from src.schemas.ability import AbilitySchema
from src.schemas.move import MoveSchema


class TestPokemonDetailSchema:
    """Test Pokemon detail schema validation."""

    def test_valid_pokemon_passes(self):
        data = {
            "id": 25,
            "name": "pikachu",
            "height": 4,
            "weight": 60,
            "stats": [
                {"base_stat": 35, "effort": 0, "stat": {"name": "hp", "url": "url"}}
            ],
            "types": [{"slot": 1, "type": {"name": "electric", "url": "url"}}],
            "abilities": [],
            "moves": [],
            "sprites": {},
            "forms": [],
            "species": {"name": "pikachu", "url": "url"},
            "is_default": True,
            "order": 1,
        }
        schema = PokemonDetailSchema(**data)
        assert schema.id == 25
        assert schema.name == "pikachu"

    def test_negative_id_rejected(self):
        data = {"id": -1, "name": "test"}
        with pytest.raises(ValidationError):
            PokemonDetailSchema(**data)

    def test_uppercase_name_rejected(self):
        """Pokemon names must be lowercase per API standard."""
        data = {
            "id": 1,
            "name": "PIKACHU",  # Should be lowercase
            "height": 4,
            "weight": 60,
            "stats": [
                {"base_stat": 35, "effort": 0, "stat": {"name": "hp", "url": "url"}}
            ],
            "types": [{"slot": 1, "type": {"name": "electric", "url": "url"}}],
        }
        with pytest.raises(ValidationError, match="lowercase"):
            PokemonDetailSchema(**data)

    def test_missing_required_fields_rejected(self):
        data = {"id": 1}  # Missing name and other required fields
        with pytest.raises(ValidationError):
            PokemonDetailSchema(**data)

    def test_negative_height_rejected(self):
        data = {
            "id": 1,
            "name": "test",
            "height": -5,  # Invalid
            "weight": 60,
            "stats": [
                {"base_stat": 35, "effort": 0, "stat": {"name": "hp", "url": "url"}}
            ],
            "types": [{"slot": 1, "type": {"name": "electric", "url": "url"}}],
        }
        with pytest.raises(ValidationError):
            PokemonDetailSchema(**data)


class TestStatSchema:
    """Test stat schema validation."""

    def test_valid_stat_passes(self):
        data = {"base_stat": 100, "effort": 2, "stat": {"name": "attack", "url": "url"}}
        schema = StatSchema(**data)
        assert schema.base_stat == 100
        assert schema.effort == 2

    def test_negative_base_stat_rejected(self):
        data = {"base_stat": -10, "effort": 0, "stat": {"name": "hp", "url": "url"}}
        with pytest.raises(ValidationError):
            StatSchema(**data)

    def test_excessive_base_stat_rejected(self):
        """Base stats have a reasonable upper bound."""
        data = {"base_stat": 300, "effort": 0, "stat": {"name": "hp", "url": "url"}}
        with pytest.raises(ValidationError):
            StatSchema(**data)


class TestSpeciesSchema:
    """Test species schema validation."""

    def test_valid_species_passes(self):
        data = {
            "id": 25,
            "name": "pikachu",
            "order": 32,
            "gender_rate": 4,
            "capture_rate": 190,
            "base_happiness": 50,
            "is_baby": False,
            "is_legendary": False,
            "is_mythical": False,
            "hatch_counter": 10,
            "has_gender_differences": True,
            "forms_switchable": False,
            "growth_rate": {"name": "medium", "url": "url"},
            "egg_groups": [],
            "generation": {"name": "generation-i", "url": "url"},
            "flavor_text_entries": [],
        }
        schema = SpeciesSchema(**data)
        assert schema.id == 25

    def test_invalid_gender_rate_rejected(self):
        """Gender rate must be -1 (genderless) or 0-8."""
        data = {
            "id": 1,
            "name": "test",
            "order": 1,
            "gender_rate": 10,  # Invalid: must be -1 to 8
            "capture_rate": 50,
            "base_happiness": 50,
            "is_baby": False,
            "is_legendary": False,
            "is_mythical": False,
            "hatch_counter": 10,
            "has_gender_differences": False,
            "forms_switchable": False,
            "growth_rate": {"name": "medium", "url": "url"},
            "egg_groups": [],
            "generation": {"name": "generation-i", "url": "url"},
            "flavor_text_entries": [],
        }
        with pytest.raises(ValidationError):
            SpeciesSchema(**data)

    def test_invalid_capture_rate_rejected(self):
        """Capture rate must be 0-255."""
        data = {
            "id": 1,
            "name": "test",
            "order": 1,
            "gender_rate": 4,
            "capture_rate": 300,  # Invalid: must be 0-255
            "base_happiness": 50,
            "is_baby": False,
            "is_legendary": False,
            "is_mythical": False,
            "hatch_counter": 10,
            "has_gender_differences": False,
            "forms_switchable": False,
            "growth_rate": {"name": "medium", "url": "url"},
            "egg_groups": [],
            "generation": {"name": "generation-i", "url": "url"},
            "flavor_text_entries": [],
        }
        with pytest.raises(ValidationError):
            SpeciesSchema(**data)


class TestAbilitySchema:
    """Test ability schema validation."""

    def test_valid_ability_passes(self):
        data = {
            "id": 9,
            "name": "static",
            "is_main_series": True,
            "generation": {"name": "generation-iii", "url": "url"},
            "effect_entries": [],
            "flavor_text_entries": [],
        }
        schema = AbilitySchema(**data)
        assert schema.name == "static"

    def test_empty_name_rejected(self):
        data = {
            "id": 1,
            "name": "",  # Invalid: must have min_length=1
            "is_main_series": True,
            "generation": {"name": "generation-i", "url": "url"},
            "effect_entries": [],
            "flavor_text_entries": [],
        }
        with pytest.raises(ValidationError):
            AbilitySchema(**data)


class TestMoveSchema:
    """Test move schema validation."""

    def test_valid_move_passes(self):
        data = {
            "id": 84,
            "name": "thunder-shock",
            "accuracy": 100,
            "effect_chance": 10,
            "pp": 30,
            "priority": 0,
            "power": 40,
            "type": {"name": "electric", "url": "url"},
            "damage_class": {"name": "special", "url": "url"},
            "effect_entries": [],
            "target": {"name": "selected-pokemon", "url": "url"},
        }
        schema = MoveSchema(**data)
        assert schema.name == "thunder-shock"

    def test_accuracy_out_of_range_rejected(self):
        """Accuracy must be 0-100 or None."""
        data = {
            "id": 1,
            "name": "test",
            "accuracy": 150,  # Invalid: must be 0-100
            "pp": 10,
            "priority": 0,
            "type": {"name": "normal", "url": "url"},
            "damage_class": {"name": "physical", "url": "url"},
            "effect_entries": [],
            "target": {"name": "selected-pokemon", "url": "url"},
        }
        with pytest.raises(ValidationError):
            MoveSchema(**data)

    def test_priority_out_of_range_rejected(self):
        """Priority must be -8 to 8."""
        data = {
            "id": 1,
            "name": "test",
            "accuracy": 100,
            "pp": 10,
            "priority": 15,  # Invalid: must be -8 to 8
            "type": {"name": "normal", "url": "url"},
            "damage_class": {"name": "physical", "url": "url"},
            "effect_entries": [],
            "target": {"name": "selected-pokemon", "url": "url"},
        }
        with pytest.raises(ValidationError):
            MoveSchema(**data)

    def test_none_accuracy_allowed(self):
        """Some moves have no accuracy (always hit)."""
        data = {
            "id": 1,
            "name": "test",
            "accuracy": None,  # Valid: some moves always hit
            "pp": 10,
            "priority": 0,
            "type": {"name": "normal", "url": "url"},
            "damage_class": {"name": "physical", "url": "url"},
            "effect_entries": [],
            "target": {"name": "selected-pokemon", "url": "url"},
        }
        schema = MoveSchema(**data)
        assert schema.accuracy is None
