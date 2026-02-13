"""Parse PokeAPI JSON responses into dataclass models."""
import re
from typing import Any

from src.models.pokemon import (
    PokemonSummary, PokemonDetail, PokemonStat,
    PokemonType, PokemonAbilityRef, PokemonMoveRef,
)
from src.models.species import PokemonSpecies
from src.models.evolution import EvolutionChain, EvolutionNode, EvolutionTrigger
from src.models.ability import Ability


def parse_id_from_url(url: str) -> int:
    """Extract numeric ID from a PokeAPI resource URL."""
    parts = url.rstrip("/").split("/")
    return int(parts[-1])


def parse_pokemon_list(data: dict[str, Any]) -> list[PokemonSummary]:
    """Parse /pokemon?limit=N response."""
    results = []
    for item in data.get("results", []):
        pokemon_id = parse_id_from_url(item["url"])
        results.append(PokemonSummary(
            id=pokemon_id,
            name=item["name"],
            url=item["url"],
        ))
    return results


def parse_pokemon_detail(data: dict[str, Any]) -> PokemonDetail:
    """Parse /pokemon/{id} response."""
    stats = [
        PokemonStat(
            name=s["stat"]["name"],
            base_stat=s["base_stat"],
            effort=s["effort"],
        )
        for s in data.get("stats", [])
    ]

    types = [
        PokemonType(slot=t["slot"], name=t["type"]["name"])
        for t in data.get("types", [])
    ]

    abilities = [
        PokemonAbilityRef(
            name=a["ability"]["name"],
            is_hidden=a["is_hidden"],
            slot=a["slot"],
        )
        for a in data.get("abilities", [])
    ]

    seen_moves: set[str] = set()
    moves: list[PokemonMoveRef] = []
    for m in data.get("moves", []):
        move_name = m["move"]["name"]
        if move_name in seen_moves:
            continue
        seen_moves.add(move_name)
        details = m.get("version_group_details", [])
        if details:
            latest = details[-1]
            moves.append(PokemonMoveRef(
                name=move_name,
                level_learned_at=latest.get("level_learned_at", 0),
                learn_method=latest["move_learn_method"]["name"],
                version_group=latest["version_group"]["name"],
            ))

    sprite_url = data.get("sprites", {}).get("front_default")

    return PokemonDetail(
        id=data["id"],
        name=data["name"],
        height=data.get("height", 0),
        weight=data.get("weight", 0),
        base_experience=data.get("base_experience"),
        sprite_url=sprite_url,
        stats=stats,
        types=types,
        abilities=abilities,
        moves=moves,
    )


def _clean_flavor_text(text: str) -> str:
    """Clean flavor text of form-feed characters and extra whitespace."""
    text = text.replace("\f", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_pokemon_species(data: dict[str, Any]) -> PokemonSpecies:
    """Parse /pokemon-species/{id} response."""
    flavor_text = ""
    for entry in reversed(data.get("flavor_text_entries", [])):
        if entry["language"]["name"] == "en":
            flavor_text = _clean_flavor_text(entry["flavor_text"])
            break

    genus = ""
    for entry in data.get("genera", []):
        if entry["language"]["name"] == "en":
            genus = entry["genus"]
            break

    evo_chain_url = data.get("evolution_chain", {}).get("url", "")
    evo_chain_id = parse_id_from_url(evo_chain_url) if evo_chain_url else 0

    return PokemonSpecies(
        id=data["id"],
        name=data["name"],
        flavor_text=flavor_text,
        genus=genus,
        generation=data.get("generation", {}).get("name", ""),
        habitat=(data.get("habitat") or {}).get("name"),
        color=data.get("color", {}).get("name", ""),
        evolution_chain_id=evo_chain_id,
        is_legendary=data.get("is_legendary", False),
        is_mythical=data.get("is_mythical", False),
        is_baby=data.get("is_baby", False),
    )


def _parse_evolution_node(chain_data: dict[str, Any]) -> EvolutionNode:
    """Recursively parse an evolution chain node."""
    species_url = chain_data["species"]["url"]
    species_id = parse_id_from_url(species_url)
    species_name = chain_data["species"]["name"]

    triggers = []
    for detail in chain_data.get("evolution_details", []):
        triggers.append(EvolutionTrigger(
            trigger=detail.get("trigger", {}).get("name", ""),
            min_level=detail.get("min_level"),
            item=(detail.get("item") or {}).get("name"),
            held_item=(detail.get("held_item") or {}).get("name"),
            min_happiness=detail.get("min_happiness"),
            time_of_day=detail.get("time_of_day") or None,
            known_move=(detail.get("known_move") or {}).get("name"),
            location=(detail.get("location") or {}).get("name"),
        ))

    evolves_to = [
        _parse_evolution_node(child)
        for child in chain_data.get("evolves_to", [])
    ]

    return EvolutionNode(
        species_name=species_name,
        species_id=species_id,
        triggers=triggers,
        evolves_to=evolves_to,
    )


def parse_evolution_chain(data: dict[str, Any]) -> EvolutionChain:
    """Parse /evolution-chain/{id} response."""
    return EvolutionChain(
        id=data["id"],
        root=_parse_evolution_node(data["chain"]),
    )


def parse_ability(data: dict[str, Any]) -> Ability:
    """Parse /ability/{id} response."""
    effect = ""
    short_effect = ""
    for entry in data.get("effect_entries", []):
        if entry["language"]["name"] == "en":
            effect = entry.get("effect", "")
            short_effect = entry.get("short_effect", "")
            break

    flavor_text = ""
    for entry in reversed(data.get("flavor_text_entries", [])):
        if entry["language"]["name"] == "en":
            flavor_text = entry["flavor_text"]
            break

    return Ability(
        id=data["id"],
        name=data["name"],
        effect=effect,
        short_effect=short_effect,
        flavor_text=flavor_text,
    )
