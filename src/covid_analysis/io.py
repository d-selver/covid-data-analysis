"""Load and normalize ECDC-style JSON data."""
import json
from datetime import datetime
from pathlib import Path

def _number(value):
    try:
        return max(0.0, float(value))
    except (TypeError, ValueError):
        return 0.0

def _load(path):
    with Path(path).open(encoding="utf-8") as f:
        return json.load(f)

def load_daily_records(path):
    payload = _load(path)
    rows = payload.get("records", []) if isinstance(payload, dict) else payload
    if not isinstance(rows, list):
        raise ValueError("Daily JSON must be a list or contain a 'records' list")
    result = []
    for row in rows:
        code = row.get("geoId") or row.get("geo_id")
        name = row.get("countriesAndTerritories") or row.get("country")
        raw_date = row.get("dateRep") or row.get("date")
        if not code or not name or not raw_date:
            continue
        try:
            day = datetime.strptime(raw_date, "%d/%m/%Y").date() if "/" in raw_date else datetime.fromisoformat(raw_date).date()
        except (TypeError, ValueError):
            continue
        result.append({"country_code": str(code), "country": str(name).replace("_", " "),
                       "date": day, "cases": _number(row.get("cases")),
                       "deaths": _number(row.get("deaths")),
                       "population": _number(row.get("popData2020") or row.get("population"))})
    return result

def load_age_records(path):
    rows = _load(path)
    if not isinstance(rows, list):
        raise ValueError("Age-group JSON must be a list")
    result = []
    for row in rows:
        try:
            year, week = (int(x) for x in row["year_week"].split("-", 1))
            code, age = row["country_code"], row["age_group"]
        except (KeyError, TypeError, ValueError):
            continue
        result.append({"country_code": str(code), "country": row.get("country", code),
                       "year": year, "week": week, "age_group": str(age),
                       "new_cases": _number(row.get("new_cases")),
                       "population": _number(row.get("population"))})
    return result
