import asyncio
import os

import httpx

_SERP_ENDPOINT = "https://serpapi.com/search"
serp_api_key = os.getenv("SERP_API_KEY")
loop = asyncio.get_event_loop()

class SerpSearchClient:
    def __init__(self, engine: str = "google") -> None:
        self._key = serp_api_key
        self._engine = engine
        self._max_results = 2
        self._client = httpx.AsyncClient(timeout=15.0)

    def search(self, query):
        response = loop.run_until_complete(
            self._client.get(
                _SERP_ENDPOINT,
                params={
                    "api_key": self._key,
                    "q": query,
                    "engine": self._engine,
                    "num": self._max_results,
                },
            )
        )
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("organic_results", []):
            results.append(
                {
                    "url": f"{item.get("link", "")}",
                    "name": f"{item.get("title", "")}",
                    "snippet": f"{item.get("snippet", "")}",
                    "source": f"{item.get("source", "")}",
                }
            )

        return results
