"""PokeAPI endpoint URL builders."""
from src.constants import POKEAPI_BASE_URL, SPRITE_BASE_URL


def pokemon_list_url(limit: int = 2000) -> str:
    return f"{POKEAPI_BASE_URL}/pokemon?limit={limit}"


def pokemon_detail_url(id_or_name: int | str) -> str:
    return f"{POKEAPI_BASE_URL}/pokemon/{id_or_name}"


def species_url(id_or_name: int | str) -> str:
    return f"{POKEAPI_BASE_URL}/pokemon-species/{id_or_name}"


def evolution_chain_url(chain_id: int) -> str:
    return f"{POKEAPI_BASE_URL}/evolution-chain/{chain_id}"


def ability_url(id_or_name: int | str) -> str:
    return f"{POKEAPI_BASE_URL}/ability/{id_or_name}"


def sprite_url(pokemon_id: int) -> str:
    return f"{SPRITE_BASE_URL}/{pokemon_id}.png"


def move_url(id_or_name: int | str) -> str:
    return f"{POKEAPI_BASE_URL}/move/{id_or_name}"


def type_url(id_or_name: int | str) -> str:
    return f"{POKEAPI_BASE_URL}/type/{id_or_name}"
