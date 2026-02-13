# Terminal Pokedex

A beautiful terminal user interface (TUI) for browsing Pokemon data using the PokeAPI.

## Features

- 🔍 **Search & Filter**: Find Pokemon by name, ID, generation, or type
- 📊 **Detailed Stats**: View base stats with color-coded bars
- 🎨 **Sprite Display**: High-quality Pokemon sprites rendered in the terminal
- 🔄 **Evolution Chains**: Visual evolution tree with trigger conditions
- ⚡ **Abilities**: Full ability descriptions and effects
- 📝 **Move List**: Sortable table of all learnable moves
- 💾 **Smart Caching**: SQLite database cache for fast offline access
- 🎯 **Type Colors**: Color-coded type badges

## Installation

### Requirements

- Python 3.11+
- pip

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Terminal-Pokedex
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

### Controls

- **Arrow Keys**: Navigate through the Pokemon list
- **Enter**: Select a Pokemon to view details
- **Tab**: Switch between tabs (Stats, Moves, Evolution, Abilities)
- **/**: Focus search bar
- **q**: Quit the application
- **?**: Show help

### Filters

- **Generation Filter**: Filter Pokemon by generation (Gen I - Gen IX)
- **Type Filter**: Filter Pokemon by type (Fire, Water, Grass, etc.)
- **Search**: Search by Pokemon name or ID

## Architecture

```
Terminal-Pokedex/
├── main.py                 # Application entry point
├── src/
│   ├── api/               # PokeAPI client and parsers
│   ├── cache/             # SQLite caching layer
│   ├── models/            # Data models
│   ├── screens/           # Main UI screens
│   ├── sprites/           # Sprite download and rendering
│   ├── widgets/           # Reusable UI widgets
│   ├── utils/             # Utility functions
│   └── constants.py       # App constants and configuration
├── styles/
│   └── pokedex.tcss      # Textual CSS styling
└── data/                  # Cache and sprites (generated)
```

## Technology Stack

- **[Textual](https://textual.textualize.io/)**: Modern TUI framework
- **[Rich](https://rich.readthedocs.io/)**: Terminal text formatting
- **[rich-pixels](https://github.com/darrenburns/rich-pixels)**: Image rendering in terminal
- **[httpx](https://www.python-httpx.org/)**: Async HTTP client
- **[aiosqlite](https://aiosqlite.omnilib.dev/)**: Async SQLite
- **[Pillow](https://python-pillow.org/)**: Image processing
- **[PokeAPI](https://pokeapi.co/)**: Pokemon data source

## License

MIT License

## Credits

- Pokemon data provided by [PokeAPI](https://pokeapi.co/)
- Sprite images from PokeAPI sprites repository
