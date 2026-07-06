# F1 MCP

An MCP server that lets an LLM (Claude Desktop, Claude Code, or any MCP client) query Formula 1 data: standings, schedules, race and qualifying results, lap times, pit stops, sprints, circuits, drivers, and finish statuses. Data comes from the [Jolpica](https://github.com/jolpica/jolpica-f1) API (the maintained Ergast successor).

Because the tools are composable, the client can answer semantic questions that no single endpoint returns, for example "how did Leclerc's grid vs finish compare across 2023" or "which teams pitted earliest at round 1", by chaining a few calls.

## Install

Requires Python 3.10+.

```bash
git clone https://github.com/devangpratap/F1-MCP.git
cd F1-MCP
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python server.py
```

The server speaks MCP over stdio, so it is meant to be launched by an MCP client rather than used directly.

### Claude Desktop

Add this to `claude_desktop_config.json` (Settings -> Developer -> Edit Config), using absolute paths:

```json
{
  "mcpServers": {
    "f1": {
      "command": "/absolute/path/to/F1-MCP/.venv/bin/python",
      "args": ["/absolute/path/to/F1-MCP/server.py"]
    }
  }
}
```

Restart Claude Desktop and the F1 tools show up in the tools menu.

## Tools

| Tool | What it returns |
| --- | --- |
| `get_driver_standings` | Current driver championship standings |
| `get_constructor_standings` | Current constructor standings |
| `get_season_schedule(season)` | Full race calendar for a season |
| `get_race_results(season, round_number)` | Finishing order for a race |
| `get_qualifying_results(season, round_number)` | Qualifying order with Q1/Q2/Q3 |
| `get_lap_times(season, round_number, lap?)` | Lap times, optionally one lap |
| `get_pit_stops(season, round_number)` | Pit stops for a race |
| `get_sprint_results(season, round_number)` | Sprint race results |
| `get_driver_season_results(season, driver_id)` | A driver's results across a season |
| `get_circuits(season)` | Circuits used in a season |
| `get_drivers(season)` | Drivers in a season |
| `get_finish_statuses` | Finish status codes and counts |

Use `season="current"` for the ongoing season. `round_number` is the round number as a string. `driver_id` is the lowercase Ergast id, e.g. `leclerc`, `max_verstappen`.

Two read-only resources are also exposed: `f1://standings/drivers` and `f1://standings/constructors`.

## Caching

Responses are cached to `cache.json` with per-endpoint TTLs (`cache.py`) so repeat queries do not hammer the API. Historical data (results, laps, pit stops) is cached forever; standings for one hour.

## Files

- `server.py` - MCP tool and resource definitions
- `api.py` - Jolpica API calls and response shaping
- `cache.py` - JSON file cache with TTLs
- `config.py` - base URL and constants

## Tests

`python test_api.py` runs a live smoke test against the API.
