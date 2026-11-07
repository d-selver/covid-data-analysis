# COMP 100 — Problem Set 3: COVID-19 Data Analysis

This repository contains my COMP 100 Problem Set 3 Python implementation. The project processes daily COVID-19 cases and deaths and weekly case records by age group, then calculates country-level statistics and an overall impact summary.

## Project files

- `PS3/read_data.py` — reads the daily and weekly JSON datasets and builds the country database.
- `PS3/covid_data_analysis.py` — calculates totals, per-million rates, age-group exposure, case probabilities, death distribution, and top-K daily records.
- `PS3/covid_impact.py` — compares countries and age groups and writes a JSON summary.

## Data files

The original ECDC datasets are not stored in this repository. Download the corresponding JSON datasets from the European Centre for Disease Prevention and Control and place these files in the repository root:

- `covid_data.json` — daily cases and deaths.
- `age_cases.json` — weekly age-specific case data.

Source: [ECDC publications and data](https://www.ecdc.europa.eu/en/publications-data/).

## Run

From the repository root, after adding both JSON files:

```bash
python -c "from PS3.read_data import process_daily_data, process_weekly_data; from PS3.covid_impact import analyze_covid_impact, write_summary_to_json; db = {}; process_daily_data(db); process_weekly_data(db); result = analyze_covid_impact(db); print(result); write_summary_to_json(result)"
```

The analysis uses the date and week ranges defined in the assignment's processing functions.

## Notes

The age-based death distribution uses the weighting assumptions specified in the assignment. It is a mathematical allocation exercise and should not be interpreted as observed age-specific mortality or a clinical estimate.
