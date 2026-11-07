from datetime import datetime
import json


def add_daily_record(country_obj, date, cases, deaths):
    """
    Adds a daily record of cases and deaths to the country's data.

    Parameters:
    - country_obj (dict): The country's data object.
    - date (str): The date of the record in DD/MM/YYYY format.
    - cases (int): Number of new cases.
    - deaths (int): Number of new deaths.
    """
    country_obj['daily_records'].append({'date': date, 'cases': cases, 'deaths': deaths})


def add_weekly_case_data(country_obj, age_group, year_week, new_cases):
    """
    Adds a weekly record of new cases for a specific age group to the country's data.

    Parameters:
    - country_obj (dict): The country's data object.
    - age_group (str): The age group for the data record.
    - year_week (str): The week of the year in YYYY-WW format.
    - new_cases (int): Number of new cases.
    """
    country_obj['weekly_records'][age_group].append({'year_week': year_week, 'new_cases': new_cases})


def create_country_entry(name, population):
    """
    Creates a new country entry with the specified name and population,
    including data structures for daily and weekly records.
    """
    return {
        'name': name,
        'population': population,
        'population_by_agegroup': {'<15yr': -1, '15-24yr': -1, '25-49yr': -1, '50-64yr': -1, '65-79yr': -1,
                                   '80+yr': -1},
        'daily_records': [],
        'weekly_records': {'<15yr': [], '15-24yr': [], '25-49yr': [], '50-64yr': [], '65-79yr': [], '80+yr': []},
    }


def process_daily_data(db):
    """
    Reads daily COVID-19 data and updates the database in place.
    """
    with open('covid_data.json', 'r') as file:
        data = json.load(file)
    for record in data['records']:
        date_string = record['dateRep']
        date_object = datetime.strptime(date_string, '%d/%m/%Y')

        if datetime(2021, 3, 7) < date_object < datetime(2021, 5, 3):
            country_code = record['geoId']
            cases = record['cases']
            deaths = record['deaths']
            population = int(record['popData2020'])

            if country_code not in db:
                db[country_code] = create_country_entry(record['countriesAndTerritories'], population)

            add_daily_record(db[country_code], date_string, cases, deaths)


def process_weekly_data(db):
    """
    Reads weekly COVID-19 data by age group and updates the database in place.
    """
    with open('age_cases.json', 'r') as file:
        data = json.load(file)
    for record in data:
        year_week = record['year_week']
        week_number = int(year_week.split('-')[1])

        if 9 < week_number < 18:
            country_code = record['country_code']
            new_cases = record['new_cases']
            population = record['population']

            if country_code not in db:
                db[country_code] = create_country_entry(record['country'], population)

            age_group = record['age_group']
            if db[country_code]['population_by_agegroup'][age_group] == -1:
                db[country_code]['population_by_agegroup'][age_group] = population
            add_weekly_case_data(db[country_code], age_group, year_week, new_cases)
