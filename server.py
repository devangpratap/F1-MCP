from mcp.server.fastmcp import FastMCP
import api

mcp = FastMCP("f1-mcp")


@mcp.tool()
def get_driver_standings() -> list:
    """Get the current F1 driver championship standings."""
    return api.get_current_season_standings()


@mcp.tool()
def get_constructor_standings() -> list:
    """Get the current F1 constructor (team) championship standings."""
    return api.get_constructor_standings()


@mcp.tool()
def get_season_schedule(season: str = "current") -> list:
    """Get the full race schedule for a season. Use 'current' for the ongoing season."""
    return api.get_season_schedule(season)


@mcp.tool()
def get_race_results(season: str, round_number: str) -> list:
    """Get race results for a specific round. Use season='current' for the ongoing season."""
    return api.get_race_results(season, round_number)


@mcp.tool()
def get_qualifying_results(season: str, round_number: str) -> list:
    """Get qualifying results for a specific round."""
    return api.get_qualifying_results(season, round_number)


@mcp.tool()
def get_lap_times(season: str, round_number: str, lap: str = None) -> list:
    """Get lap times for a race. Optionally filter to a specific lap number."""
    return api.get_lap_times(season, round_number, lap)


@mcp.tool()
def get_pit_stops(season: str, round_number: str) -> list:
    """Get pit stop data for a specific race."""
    return api.get_pit_stops(season, round_number)


@mcp.tool()
def get_sprint_results(season: str, round_number: str) -> list:
    """Get sprint race results for a specific round."""
    return api.get_sprint_results(season, round_number)


@mcp.tool()
def get_driver_season_results(season: str, driver_id: str) -> list:
    """Get all race results for a driver in a season. driver_id is lowercase e.g. 'leclerc', 'norris'."""
    return api.get_driver_season_results(season, driver_id)


if __name__ == "__main__":
    mcp.run()
