# COVID-19 Surveillance Data Analysis

A reproducible Python project for exploring country-level COVID-19 cases and deaths, population-adjusted rates, and weekly case patterns by age group.

## Features
- Load ECDC-style daily and weekly JSON exports.
- Aggregate cases and deaths by country over an optional date window.
- Calculate cases and deaths per million residents.
- Summarize weekly cases and descriptive exposure ratios by age band.
- Export structured JSON summaries.
- Run automated unit tests with GitHub Actions.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Run
```bash
covid-analysis --daily data/covid_data.json --age data/age_cases.json --start 2021-03-08 --end 2021-05-02 --output output/summary.json
```
Dates are inclusive. Daily JSON may be a list or an object containing a `records` list. Age data must be a JSON list.

## Data and methodology
This repository intentionally does not redistribute course-assignment datasets. Add a permitted ECDC export locally under `data/`; verify the current source terms and metadata before redistribution. Source: [ECDC publications and data](https://www.ecdc.europa.eu/en/publications-data).

Per-million rates equal total count / population * 1,000,000. Age exposure is accumulated weekly reported cases divided by the age-band population; it is descriptive and must not be interpreted as an individual's infection probability. The optional death-by-age allocation is a transparent heuristic, not observed mortality data or a clinical estimate.

## Tests
```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```
