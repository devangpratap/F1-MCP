Incomplete

# F1 MCP

An MCP server that lets Claude query live Formula 1 data via the Jolpica API.

## Files

- **api.py** — all Jolpica API calls, covers standings, results, qualifying, lap times, pit stops, sprint, circuits, drivers, and status
- **cache.py** — caches responses to a local JSON file with TTLs so we don't hammer the API on repeat queries
- **config.py** — base URL, cache file path, and other constants
