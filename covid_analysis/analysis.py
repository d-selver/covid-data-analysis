def daily_records_to_string(country_obj, idxs):
    output_str = ""
    for idx in idxs:
        record = country_obj['daily_records'][idx]
        output_str += f"Date: {record['date']}, Cases: {record['cases']}, Deaths: {record['deaths']} \n"
    return output_str


def get_total_cases(country_obj):
    """Calculates the total number of COVID-19 cases from daily records."""
    total_cases = sum(record['cases'] for record in country_obj['daily_records'])
    return total_cases


def get_total_deaths(country_obj):
    """Calculates the total number of COVID-19 deaths from daily records."""
    total_deaths = sum(record['deaths'] for record in country_obj['daily_records'])
    return total_deaths


def total_cases_and_deaths_per_1m(country_obj):
    """Scales the total number of cases and deaths to per 1 million population."""
    total_cases = get_total_cases(country_obj)
    total_deaths = get_total_deaths(country_obj)
    population = country_obj['population']
    if population <= 0:
        return 0, 0
    cases_per_1m = (total_cases / population) * 1_000_000
    deaths_per_1m = (total_deaths / population) * 1_000_000
    return int(cases_per_1m), int(deaths_per_1m)


def sort_records_by(country_obj, param):
    """Sorts daily records by a selected field and returns their indices."""
    nums = [(i, record[param]) for i, record in enumerate(country_obj['daily_records'])]
    nums.sort(key=lambda x: x[1])
    indexes = [index for index, value in nums]
    return indexes


def find_top_k_cases(country_obj, k):
    idxs = sort_records_by(country_obj, "cases")[-k:]
    return daily_records_to_string(country_obj, idxs)


def find_top_k_deaths(country_obj, k):
    idxs = sort_records_by(country_obj, "deaths")[-k:]
    return daily_records_to_string(country_obj, idxs)


def calc_exposure_per_age_group(country_obj):
    """Calculates total cases divided by population for each age group."""
    exposure_dict = {}
    for age_group, records in country_obj['weekly_records'].items():
        total_cases = sum(record['new_cases'] for record in records)
        population = country_obj['population_by_agegroup'][age_group]
        if population > 0:
            exposure_dict[age_group] = total_cases / population
    return exposure_dict


def find_most_exposed_age_group(country_obj):
    """Identifies the most exposed age group based on infection rates."""
    exposure_dict = calc_exposure_per_age_group(country_obj)
    return max(exposure_dict, key=exposure_dict.get)


def find_least_exposed_age_group(country_obj):
    """Identifies the least exposed age group based on infection rates."""
    exposure_dict = calc_exposure_per_age_group(country_obj)
    return min(exposure_dict, key=exposure_dict.get)


def calc_prob_of_cases_per_age_group(country_obj):
    """Calculates the probability of a new case belonging to each age group."""
    total_cases = get_total_cases(country_obj)
    prob_dict = {}
    for age_group, records in country_obj['weekly_records'].items():
        age_group_cases = sum(record['new_cases'] for record in records)
        prob_dict[age_group] = age_group_cases / total_cases if total_cases > 0 else 0
    return prob_dict


def distribute_deaths_to_age_groups(country_obj):
    """Allocates deaths using age-group case shares and weighted death probabilities."""
    case_probs = calc_prob_of_cases_per_age_group(country_obj)
    age_groups = list(case_probs.keys())
    death_probs = {
        '<15yr': 0.05,
        '15-24yr': 0.05,
        '25-49yr': 0.1,
        '50-64yr': 0.2,
        '65-79yr': 0.25,
        '80+yr': 0.35
    }
    total_deaths = get_total_deaths(country_obj)
    weighted_probs = {age_group: case_probs[age_group] * death_probs[age_group] for age_group in case_probs}
    total_weighted = sum(weighted_probs.values())
    if total_weighted == 0:
        return total_deaths, {age_group: 0 for age_group in age_groups}
    normalized_probs = {age_group: weight / total_weighted for age_group, weight in weighted_probs.items()}
    death_distribution = {age_group: normalized_probs[age_group] * total_deaths for age_group in normalized_probs}
    return total_deaths, death_distribution
