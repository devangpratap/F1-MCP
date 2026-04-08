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


if __name__ == "__main__":
    mcp.run()
