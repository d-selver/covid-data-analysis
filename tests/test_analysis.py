import unittest
from datetime import date
from covid_analysis.analysis import analyze_countries, summarize_age_groups, estimate_deaths_by_age

class AnalysisTests(unittest.TestCase):
    def test_country_totals_and_rates(self):
        rows = [{"country_code":"TR","country":"Türkiye","date":date(2021,4,1),"cases":150,"deaths":3,"population":10_000_000}]
        result = analyze_countries(rows)[0]
        self.assertEqual(result["cases"], 150)
        self.assertEqual(result["cases_per_million"], 15)
        self.assertAlmostEqual(result["deaths_per_million"], .3)

    def test_date_window_is_inclusive(self):
        rows = [{"country_code":"X","country":"X","date":date(2021,4,d),"cases":1,"deaths":0,"population":100} for d in (1,2,3)]
        self.assertEqual(analyze_countries(rows,date(2021,4,2),date(2021,4,2))[0]["cases"],1)

    def test_age_exposure(self):
        rows = [{"year":2021,"age_group":"20-39","new_cases":30,"population":1000}]
        result = summarize_age_groups(rows,2021)
        self.assertAlmostEqual(result["exposure_by_age_group"]["20-39"],.03)

    def test_weighted_death_allocation(self):
        result = estimate_deaths_by_age(100,{"<15yr":10,"80+yr":10})
        self.assertAlmostEqual(sum(result.values()),100)
        self.assertEqual(sum(estimate_deaths_by_age(10,{"80+yr":0}).values()),0)

if __name__ == "__main__":
    unittest.main()
