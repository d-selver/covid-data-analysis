"""Country and age-band aggregations."""
from collections import defaultdict

def analyze_countries(records, start=None, end=None):
    grouped = {}
    for row in records:
        if (start and row["date"] < start) or (end and row["date"] > end):
            continue
        code = row["country_code"]
        item = grouped.setdefault(code, {"country_code": code, "country": row["country"],
            "cases": 0.0, "deaths": 0.0, "population": 0.0})
        item["cases"] += row["cases"]
        item["deaths"] += row["deaths"]
        if row["population"] > 0:
            item["population"] = row["population"]
    result = []
    for item in grouped.values():
        pop = item["population"]
        item["cases_per_million"] = item["cases"] / pop * 1_000_000 if pop else None
        item["deaths_per_million"] = item["deaths"] / pop * 1_000_000 if pop else None
        result.append(item)
    return sorted(result, key=lambda x: x["country"])

def summarize_age_groups(records, year=None):
    cases, populations = defaultdict(float), {}
    for row in records:
        if year is not None and row["year"] != year:
            continue
        age = row["age_group"]
        cases[age] += row["new_cases"]
        if row["population"] > 0:
            populations[age] = row["population"]
    exposure = {age: total / populations[age] for age, total in cases.items() if populations.get(age, 0) > 0}
    return {"cases_by_age_group": dict(sorted(cases.items())),
            "exposure_by_age_group": dict(sorted(exposure.items())),
            "most_exposed_age_group": max(exposure, key=exposure.get) if exposure else None,
            "least_exposed_age_group": min(exposure, key=exposure.get) if exposure else None}

def estimate_deaths_by_age(total_deaths, age_case_counts):
    """Illustrative weighted allocation; weights are heuristic, not observed mortality."""
    weights = {"<15yr": .05, "15-24yr": .05, "25-49yr": .10,
               "50-64yr": .20, "65-79yr": .25, "80+yr": .35}
    weighted = {age: max(0, count) * weights.get(age, 0) for age, count in age_case_counts.items()}
    denominator = sum(weighted.values())
    if denominator <= 0 or total_deaths <= 0:
        return {age: 0.0 for age in weighted}
    return {age: total_deaths * value / denominator for age, value in weighted.items()}
