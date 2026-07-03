"""Live smoke test against the Jolpica API. Run: python test_api.py"""

import api


def test_smoke():
    schedule = api.get_season_schedule("2023")
    assert len(schedule) == 22, f"expected 22 races in 2023, got {len(schedule)}"
    assert schedule[0]["name"] == "Bahrain Grand Prix"

    results = api.get_race_results("2023", "1")
    assert results[0]["driver"] == "Max Verstappen"
    assert results[0]["position"] == "1"

    quali = api.get_qualifying_results("2023", "1")
    assert quali[0]["position"] == "1"

    pits = api.get_pit_stops("2023", "1")
    assert pits and pits[0]["driver_id"]

    drivers = api.get_drivers("2023")
    assert any(d["driver_id"] == "max_verstappen" for d in drivers)

    laps = api.get_lap_times("2023", "1", "1")
    assert laps and laps[0]["lap"] == "1"


if __name__ == "__main__":
    test_smoke()
    print("ok")
