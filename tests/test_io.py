import json, tempfile, unittest
from pathlib import Path
from covid_analysis.io import load_daily_records, load_age_records

class LoaderTests(unittest.TestCase):
    def test_geo_id_and_date_parsing(self):
        payload = {"records":[{"dateRep":"01/04/2021","geoId":"TR","countriesAndTerritories":"Turkey","cases":4,"deaths":1,"popData2020":"1000"}]}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/"daily.json"
            path.write_text(json.dumps(payload),encoding="utf-8")
            data = load_daily_records(path)
        self.assertEqual(data[0]["country_code"],"TR")
        self.assertEqual(data[0]["cases"],4)

    def test_age_population_is_loaded(self):
        payload = [{"country_code":"TR","year_week":"2021-10","age_group":"80+yr","new_cases":8,"population":200}]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/"age.json"
            path.write_text(json.dumps(payload),encoding="utf-8")
            data = load_age_records(path)
        self.assertEqual(data[0]["week"],10)
        self.assertEqual(data[0]["population"],200)

if __name__ == "__main__":
    unittest.main()
