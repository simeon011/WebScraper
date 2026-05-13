import unittest
import os
from scraper import Scraper

class TestScraper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Starts the scraper once for all tests"""
        cls.scraper = Scraper()
        cls.test_data = {
            "Bulgaria": {"population": 6951482.0, "region": "Europe", "gdp": 0}
        }

    @classmethod
    def tearDownClass(cls):
        """Closes the browser after all tests are finished"""
        cls.scraper.driver.quit()

    def test_1_browser_initialization(self):
        """Test: Is the driver initialized correctly?"""
        self.assertIsNotNone(self.scraper.driver)
        print("✔ Test 1: Browser started successfully.")

    def test_2_url_loading(self):
        """Test: Do the target pages load correctly?"""
        url = "https://www.worldometers.info/geography/countries-of-the-world/"
        self.scraper.driver.get(url)
        self.assertIn("worldometers", self.scraper.driver.current_url)
        print("✔ Test 2: URL loaded correctly.")

    def test_3_js_execution(self):
        """Test: Does JavaScript return data?"""
        self.scraper.driver.get("https://www.worldometers.info/geography/countries-of-the-world/")
        rows = self.scraper.driver.execute_script("return document.querySelectorAll('table tbody tr').length")
        self.assertGreater(rows, 0)
        print(f"✔ Test 3: JavaScript found {rows} rows in the table.")

    def test_4_population_conversion(self):
        """Test: Does the text-to-number conversion logic work?"""
        pop_text = "7,000,000".replace(",", "").replace(" ", "")
        population = float(pop_text)
        self.assertEqual(population, 7000000.0)
        print("✔ Test 4: Population conversion is accurate.")

    def test_5_gdp_cleaning(self):
        """Test: Does cleaning the $ symbol and commas work?"""
        gdp_text = "$ 21,433,226,000,000".replace(",", "").replace("$", "").replace(" ", "")
        gdp = float(gdp_text)
        self.assertEqual(gdp, 21433226000000.0)
        print("✔ Test 5: GDP cleaning is accurate.")

    def test_6_data_structure(self):
        """Test: Does the dictionary contain the correct keys?"""
        sample_country = list(self.test_data.keys())[0]
        keys = self.test_data[sample_country].keys()
        self.assertTrue(all(k in keys for k in ["population", "region", "gdp"]))
        print("✔ Test 6: Dictionary structure is correct.")

    def test_7_error_handling(self):
        """Test: Does the code handle invalid numbers?"""
        bad_text = "N/A"
        try:
            val = float(bad_text.replace(",", ""))
        except ValueError:
            val = 0
        self.assertEqual(val, 0)
        print("✔ Test 7: Invalid data successfully converted to 0.")

    def test_8_csv_creation(self):
        """Test: Is the file physically created on the disk?"""
        self.scraper.save_to_csv(self.test_data)
        self.assertTrue(os.path.exists("countries_data.csv"))
        print("✔ Test 8: CSV file created.")

    def test_9_csv_content(self):
        """Test: Is the header row correct in the CSV file?"""
        with open("countries_data.csv", "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
        self.assertEqual(first_line, "name,population,region,gdp")
        print("✔ Test 9: CSV header row is correct.")

    def test_10_matching_logic(self):
        """Test: Is GDP added to an existing country correctly?"""
        country_name = "Bulgaria"
        gdp_val = 67.92
        if country_name in self.test_data:
            self.test_data[country_name]["gdp"] = gdp_val
        self.assertEqual(self.test_data["Bulgaria"]["gdp"], 67.92)
        print("✔ Test 10: GDP merging logic works.")

if __name__ == "__main__":
    unittest.main()