"""Async HTTP client for PokeAPI."""
import httpx
from typing import Any


class PokeAPIClient:
    """Manages httpx.AsyncClient for PokeAPI requests."""

    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(30.0, connect=10.0),
                follow_redirects=True,
                limits=httpx.Limits(
                    max_connections=10,
                    max_keepalive_connections=5,
                ),
            )
        return self._client

    async def get_json(self, url: str) -> dict[str, Any]:
        """Fetch JSON from a URL. Raises on HTTP errors."""
        client = await self._get_client()
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

    async def get_bytes(self, url: str) -> bytes:
        """Fetch raw bytes (for sprite images)."""
        client = await self._get_client()
        response = await client.get(url)
        response.raise_for_status()
        return response.content

    async def close(self) -> None:
        """Close the underlying httpx client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None
