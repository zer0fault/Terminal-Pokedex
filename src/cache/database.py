"""Async SQLite database wrapper for caching."""
import json
import time

import aiosqlite

from src.constants import CACHE_DB, CACHE_TTL_POKEMON_LIST


class CacheDatabase:
    """Provides async SQLite operations for the Pokedex cache."""

    def __init__(self, db_path: str | None = None) -> None:
        self._db_path = str(db_path or CACHE_DB)
        self._db: aiosqlite.Connection | None = None

    async def initialize(self) -> None:
        """Open connection and create tables if needed."""
        self._db = await aiosqlite.connect(self._db_path)
        self._db.row_factory = aiosqlite.Row
        await self._create_tables()

    async def _create_tables(self) -> None:
        assert self._db is not None
        await self._db.executescript("""
            CREATE TABLE IF NOT EXISTS pokemon_list (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                url TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS pokemon_list_meta (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS pokemon_detail (
                id INTEGER PRIMARY KEY,
                data_json TEXT NOT NULL,
                cached_at REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS pokemon_species (
                id INTEGER PRIMARY KEY,
                data_json TEXT NOT NULL,
                cached_at REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS evolution_chain (
                id INTEGER PRIMARY KEY,
                data_json TEXT NOT NULL,
                cached_at REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS ability (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                data_json TEXT NOT NULL,
                cached_at REAL NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_pokemon_list_name
                ON pokemon_list(name);

            CREATE INDEX IF NOT EXISTS idx_ability_name
                ON ability(name);
        """)
        await self._db.commit()

    async def get_pokemon_list(self) -> list[dict] | None:
        """Return cached Pokemon list or None if stale/missing."""
        assert self._db is not None
        async with self._db.execute(
            "SELECT value FROM pokemon_list_meta WHERE key = 'cached_at'"
        ) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return None
            cached_at = float(row["value"])
            if time.time() - cached_at > CACHE_TTL_POKEMON_LIST:
                return None

        async with self._db.execute(
            "SELECT id, name, url FROM pokemon_list ORDER BY id"
        ) as cursor:
            rows = await cursor.fetchall()
            if not rows:
                return None
            return [dict(row) for row in rows]

    async def save_pokemon_list(self, pokemon_list: list[dict]) -> None:
        """Save the full Pokemon list to cache."""
        assert self._db is not None
        await self._db.execute("DELETE FROM pokemon_list")
        await self._db.executemany(
            "INSERT INTO pokemon_list (id, name, url) VALUES (?, ?, ?)",
            [(p["id"], p["name"], p["url"]) for p in pokemon_list],
        )
        await self._db.execute(
            "INSERT OR REPLACE INTO pokemon_list_meta (key, value) VALUES (?, ?)",
            ("cached_at", str(time.time())),
        )
        await self._db.commit()

    async def get_cached_json(
        self, table: str, item_id: int, ttl: float
    ) -> dict | None:
        """Get cached JSON from a table, or None if stale/missing."""
        assert self._db is not None
        async with self._db.execute(
            f"SELECT data_json, cached_at FROM {table} WHERE id = ?",
            (item_id,),
        ) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return None
            if time.time() - row["cached_at"] > ttl:
                return None
            return json.loads(row["data_json"])

    async def save_cached_json(
        self, table: str, item_id: int, data: dict, name: str | None = None
    ) -> None:
        """Save JSON data to a cache table."""
        assert self._db is not None
        if name is not None:
            await self._db.execute(
                f"INSERT OR REPLACE INTO {table} (id, name, data_json, cached_at) "
                f"VALUES (?, ?, ?, ?)",
                (item_id, name, json.dumps(data), time.time()),
            )
        else:
            await self._db.execute(
                f"INSERT OR REPLACE INTO {table} (id, data_json, cached_at) "
                f"VALUES (?, ?, ?)",
                (item_id, json.dumps(data), time.time()),
            )
        await self._db.commit()

    async def close(self) -> None:
        """Close the database connection."""
        if self._db:
            await self._db.close()
            self._db = None
