import requests

BASE_URL = "https://api.jolpi.ca/ergast/f1"


def _get(endpoint: str) -> dict:
    response = requests.get(f"{BASE_URL}{endpoint}.json")
    response.raise_for_status()
    return response.json()


def get_current_season_standings() -> dict:
    """Driver championship standings for the current season."""
    data = _get("/current/driverStandings")
    standings = data["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]
    return [
        {
            "position": s["position"],
            "driver": f"{s['Driver']['givenName']} {s['Driver']['familyName']}",
            "nationality": s["Driver"]["nationality"],
            "team": s["Constructors"][0]["name"],
            "points": s["points"],
            "wins": s["wins"],
        }
        for s in standings
    ]


def get_constructor_standings() -> list:
    """Constructor championship standings for the current season."""
    data = _get("/current/constructorStandings")
    standings = data["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"]
    return [
        {
            "position": s["position"],
            "team": s["Constructor"]["name"],
            "nationality": s["Constructor"]["nationality"],
            "points": s["points"],
            "wins": s["wins"],
        }
        for s in standings
    ]


def get_race_results(season: str, round_number: str) -> list:
    """Results for a specific race."""
    data = _get(f"/{season}/{round_number}/results")
    races = data["MRData"]["RaceTable"]["Races"]
    if not races:
        return []
    results = races[0]["Results"]
    return [
        {
            "position": r["position"],
            "driver": f"{r['Driver']['givenName']} {r['Driver']['familyName']}",
            "team": r["Constructor"]["name"],
            "grid": r["grid"],
            "laps": r["laps"],
            "status": r["status"],
            "points": r["points"],
            "fastest_lap": r.get("FastestLap", {}).get("Time", {}).get("time"),
        }
        for r in results
    ]


def get_season_schedule(season: str = "current") -> list:
    """Full race schedule for a season."""
    data = _get(f"/{season}")
    races = data["MRData"]["RaceTable"]["Races"]
    return [
        {
            "round": r["round"],
            "name": r["raceName"],
            "circuit": r["Circuit"]["circuitName"],
            "country": r["Circuit"]["Location"]["country"],
            "date": r["date"],
            "time": r.get("time", "TBD"),
        }
        for r in races
    ]


def get_driver_season_results(season: str, driver_id: str) -> list:
    """All race results for a specific driver in a season."""
    data = _get(f"/{season}/drivers/{driver_id}/results")
    races = data["MRData"]["RaceTable"]["Races"]
    return [
        {
            "round": r["round"],
            "race": r["raceName"],
            "position": r["Results"][0]["position"],
            "grid": r["Results"][0]["grid"],
            "status": r["Results"][0]["status"],
            "points": r["Results"][0]["points"],
        }
        for r in races
    ]


def get_qualifying_results(season: str, round_number: str) -> list:
    """Qualifying results for a specific race."""
    data = _get(f"/{season}/{round_number}/qualifying")
    races = data["MRData"]["RaceTable"]["Races"]
    if not races:
        return []
    results = races[0]["QualifyingResults"]
    return [
        {
            "position": r["position"],
            "driver": f"{r['Driver']['givenName']} {r['Driver']['familyName']}",
            "team": r["Constructor"]["name"],
            "q1": r.get("Q1"),
            "q2": r.get("Q2"),
            "q3": r.get("Q3"),
        }
        for r in results
    ]


def get_circuits(season: str = "current") -> list:
    """All circuits for a given season."""
    data = _get(f"/{season}/circuits")
    circuits = data["MRData"]["CircuitTable"]["Circuits"]
    return [
        {
            "circuit_id": c["circuitId"],
            "name": c["circuitName"],
            "country": c["Location"]["country"],
            "city": c["Location"]["locality"],
            "lat": c["Location"]["lat"],
            "long": c["Location"]["long"],
        }
        for c in circuits
    ]


def get_drivers(season: str = "current") -> list:
    """All drivers for a given season."""
    data = _get(f"/{season}/drivers")
    drivers = data["MRData"]["DriverTable"]["Drivers"]
    return [
        {
            "driver_id": d["driverId"],
            "name": f"{d['givenName']} {d['familyName']}",
            "nationality": d.get("nationality"),
            "date_of_birth": d.get("dateOfBirth"),
            "number": d.get("permanentNumber"),
            "code": d.get("code"),
        }
        for d in drivers
    ]


def get_finish_statuses() -> list:
    """All possible finish status codes (Finished, DNF, DNS, etc.)."""
    data = _get("/status")
    statuses = data["MRData"]["StatusTable"]["Status"]
    return [
        {
            "status_id": s["statusId"],
            "status": s["status"],
            "count": s["count"],
        }
        for s in statuses
    ]


def get_lap_times(season: str, round_number: str, lap: str = None) -> list:
    """Lap times for a race. Optionally filter to a specific lap number."""
    endpoint = f"/{season}/{round_number}/laps"
    if lap:
        endpoint += f"/{lap}"
    data = _get(endpoint)
    races = data["MRData"]["RaceTable"]["Races"]
    if not races:
        return []
    laps = races[0]["Laps"]
    result = []
    for lap_data in laps:
        for timing in lap_data["Timings"]:
            result.append({
                "lap": lap_data["number"],
                "driver_id": timing["driverId"],
                "position": timing["position"],
                "time": timing["time"],
            })
    return result


def get_pit_stops(season: str, round_number: str) -> list:
    """Pit stop data for a specific race."""
    data = _get(f"/{season}/{round_number}/pitstops")
    races = data["MRData"]["RaceTable"]["Races"]
    if not races:
        return []
    pit_stops = races[0]["PitStops"]
    return [
        {
            "driver_id": p["driverId"],
            "lap": p["lap"],
            "stop": p["stop"],
            "time": p["time"],
            "duration": p["duration"],
        }
        for p in pit_stops
    ]


def get_sprint_results(season: str, round_number: str) -> list:
    """Sprint race results for a specific round."""
    data = _get(f"/{season}/{round_number}/sprint")
    races = data["MRData"]["RaceTable"]["Races"]
    if not races:
        return []
    results = races[0]["SprintResults"]
    return [
        {
            "position": r["position"],
            "driver": f"{r['Driver']['givenName']} {r['Driver']['familyName']}",
            "team": r["Constructor"]["name"],
            "grid": r["grid"],
            "laps": r["laps"],
            "status": r["status"],
            "points": r["points"],
            "fastest_lap": r.get("FastestLap", {}).get("Time", {}).get("time"),
        }
        for r in results
    ]
