"""Application-wide constants for Terminal Pokedex."""
from pathlib import Path

APP_NAME = "Terminal Pokedex"
APP_VERSION = "1.0.0"

# --- Data directories (relative to project root) ---
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SPRITES_DIR = DATA_DIR / "sprites"
CACHE_DB = DATA_DIR / "pokedex_cache.db"

# --- PokeAPI ---
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"
SPRITE_BASE_URL = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon"

# --- Cache TTL (seconds) ---
CACHE_TTL_POKEMON_LIST = 86400 * 7     # 7 days
CACHE_TTL_POKEMON_DETAIL = 86400 * 30  # 30 days
CACHE_TTL_SPECIES = 86400 * 30
CACHE_TTL_EVOLUTION = 86400 * 30
CACHE_TTL_ABILITY = 86400 * 30

# --- Sprite rendering ---
SPRITE_RENDER_WIDTH = 60  # Increased for better quality
SPRITE_BG_COLOR = (30, 30, 46)

# --- Pokemon type colors (hex) ---
TYPE_COLORS: dict[str, str] = {
    "normal":   "#A8A77A",
    "fire":     "#EE8130",
    "water":    "#6390F0",
    "electric": "#F7D02C",
    "grass":    "#7AC74C",
    "ice":      "#96D9D6",
    "fighting": "#C22E28",
    "poison":   "#A33EA1",
    "ground":   "#E2BF65",
    "flying":   "#A98FF3",
    "psychic":  "#F95587",
    "bug":      "#A6B91A",
    "rock":     "#B6A136",
    "ghost":    "#735797",
    "dragon":   "#6F35FC",
    "dark":     "#705746",
    "steel":    "#B7B7CE",
    "fairy":    "#D685AD",
}

# --- Stat bar colors by value range ---
STAT_COLOR_LOW = "#F44336"
STAT_COLOR_MEDIUM = "#FF9800"
STAT_COLOR_GOOD = "#FFC107"
STAT_COLOR_HIGH = "#8BC34A"
STAT_COLOR_VERY_HIGH = "#4CAF50"
STAT_COLOR_MAX = "#00BCD4"

STAT_MAX_VALUE = 255

# --- Stat abbreviations ---
STAT_NAMES: dict[str, str] = {
    "hp":              "HP ",
    "attack":          "ATK",
    "defense":         "DEF",
    "special-attack":  "SPA",
    "special-defense": "SPD",
    "speed":           "SPE",
}

# --- Generation mapping ---
GENERATION_MAP: dict[str, str] = {
    "generation-i":    "Gen I",
    "generation-ii":   "Gen II",
    "generation-iii":  "Gen III",
    "generation-iv":   "Gen IV",
    "generation-v":    "Gen V",
    "generation-vi":   "Gen VI",
    "generation-vii":  "Gen VII",
    "generation-viii": "Gen VIII",
    "generation-ix":   "Gen IX",
}

# --- Type abbreviations ---
TYPE_ABBREVIATIONS: dict[str, str] = {
    "normal":   "NOR",
    "fire":     "FIR",
    "water":    "WAT",
    "electric": "ELE",
    "grass":    "GRA",
    "ice":      "ICE",
    "fighting": "FIG",
    "poison":   "POI",
    "ground":   "GND",
    "flying":   "FLY",
    "psychic":  "PSY",
    "bug":      "BUG",
    "rock":     "ROK",
    "ghost":    "GHO",
    "dragon":   "DRA",
    "dark":     "DRK",
    "steel":    "STL",
    "fairy":    "FAI",
}

POKEDEX_RED = "#dc0a2d"
