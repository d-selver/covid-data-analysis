# COVID-19 Data Analysis

A Python project for processing COVID-19 surveillance data and exploring how reported cases and deaths varied across countries and age groups.

## Overview

The project combines daily country-level case and death records with weekly age-group case data. It builds a structured country database and provides functions to calculate key indicators and compare the impact across countries.

## Features

- Process daily COVID-19 cases and deaths.
- Process weekly case counts by age group.
- Calculate total cases and deaths for each country.
- Compare cases and deaths per one million residents.
- Identify the daily records with the highest case and death counts.
- Calculate age-group exposure ratios.
- Estimate an illustrative age-based death distribution using predefined weights.
- Generate a JSON summary of the country-level impact analysis.

## Project structure

```text
covid-data-analysis/
├── covid_analysis/
│   ├── __init__.py
│   ├── read_data.py
│   ├── analysis.py
│   └── impact.py
├── .github/
│   └── workflows/
│       └── tests.yml
├── .gitignore
└── README.md
```

## Data

The analysis expects two JSON files in the project root:

- `covid_data.json` — daily country-level records, including date, country code, cases, deaths, and population.
- `age_cases.json` — weekly records containing country, year-week, age group, new cases, and age-group population.

The original data files are not included in this repository. Obtain the datasets from an authorized source and check the applicable terms before redistributing them. A starting point is the [European Centre for Disease Prevention and Control (ECDC)](https://www.ecdc.europa.eu/en/publications-data).

## Run

From the project root, run the analysis with:

```bash
python - <<'PY'
from covid_analysis.read_data import process_daily_data, process_weekly_data
from covid_analysis.impact import analyze_covid_impact, write_summary_to_json

database = {}
process_daily_data(database)
process_weekly_data(database)

summary = analyze_covid_impact(database)
print(summary)
write_summary_to_json(summary)
PY
```

The processing functions use the date and week ranges defined in the source code. The summary is written to `covid_impact_summary.json`.

## Methodology note

The age-group exposure ratio is calculated as reported cases divided by the corresponding age-group population. The age-based death distribution applies predefined weights to case shares. This is an illustrative allocation method, not observed age-specific mortality data or a clinical estimate.

## Quality checks

A GitHub Actions workflow runs a Python syntax check whenever changes are pushed or a pull request is opened.
