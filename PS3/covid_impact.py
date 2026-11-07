from PS3.covid_data_analysis import total_cases_and_deaths_per_1m, calc_exposure_per_age_group
import json


def analyze_covid_impact(db):
    """
    Analyzes COVID-19 impact across EU countries from the given dataset.

    Returns the countries with the highest per-million case and death counts,
    plus the most and least exposed age groups across countries.
    """
    top_case_cnt = 0
    top_death_cnt = 0
    top_case_country = ""
    top_death_country = ""
    exposure_rates = {}

    for country_code, country_data in db.items():
        cases_per_million, deaths_per_million = total_cases_and_deaths_per_1m(country_data)

        if deaths_per_million > top_death_cnt:
            top_death_cnt = deaths_per_million
            top_death_country = country_data['name']

        if cases_per_million > top_case_cnt:
            top_case_cnt = cases_per_million
            top_case_country = country_data['name']

        exposure_dict = calc_exposure_per_age_group(country_data)
        for age_group, exposure_rate in exposure_dict.items():
            exposure_rates.setdefault(age_group, []).append(exposure_rate)

    avg_exposure_rates = {
        age_group: sum(rates) / len(rates)
        for age_group, rates in exposure_rates.items() if rates
    }
    most_exposed_age_group = max(avg_exposure_rates, key=avg_exposure_rates.get) if avg_exposure_rates else ""
    least_exposed_age_group = min(avg_exposure_rates, key=avg_exposure_rates.get) if avg_exposure_rates else ""

    return (top_death_country, top_death_cnt, top_case_country,
            top_case_cnt, most_exposed_age_group, least_exposed_age_group)


def write_summary_to_json(data):
    """Writes the COVID-19 impact summary tuple to a JSON file."""
    summary = {
        "Highest_Deaths_per_1M": {
            "Country": data[0],
            "Deaths_per_1M": data[1]
        },
        "Highest_Cases_per_1M": {
            "Country": data[2],
            "Cases_per_1M": data[3]
        },
        "Most_Exposed_Age_Group": data[4],
        "Least_Exposed_Age_Group": data[5]
    }
    with open('covid_impact_summary.json', 'w') as json_file:
        json.dump(summary, json_file, indent=4)
