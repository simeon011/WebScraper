import unittest
import os
import csv
from analyzer import Analyzer

class TestAnalyzer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Create a temporary test CSV file"""
        cls.test_file = "test_countries.csv"
        with open(cls.test_file, "w", newline="", encoding="utf-8") as f:
            # Note: headers are lowercase 'gdp' to match your updated Analyzer requirements
            writer = csv.DictWriter(f, fieldnames=["name", "population", "region", "gdp"])
            writer.writeheader()
            writer.writerow({"name": "Bulgaria", "population": "6900000", "region": "Europe", "gdp": "70000"})
            writer.writerow({"name": "Germany", "population": "83000000", "region": "Europe", "gdp": "4000000"})
            writer.writerow({"name": "China", "population": "1400000000", "region": "Asia", "gdp": "17000000"})
            writer.writerow({"name": "Japan", "population": "125000000", "region": "Asia", "gdp": "5000000"})
            writer.writerow({"name": "Egypt", "population": "100000000", "region": "Africa", "gdp": "400000"})
            writer.writerow({"name": "Nigeria", "population": "200000000", "region": "Africa", "gdp": "450000"})

        cls.analyzer = Analyzer(cls.test_file)

    @classmethod
    def tearDownClass(cls):
        """Delete the temporary file after tests are completed"""
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)

    def test_1_load_data(self):
        """Test: Is data loaded correctly with the right number of rows?"""
        self.assertEqual(len(self.analyzer.data), 6)
        print("✔ Test 1: Correct number of countries loaded.")

    def test_2_data_types(self):
        """Test: Are values converted to integers correctly?"""
        country = self.analyzer.data[0]
        self.assertIsInstance(country["population"], int)
        self.assertIsInstance(country["gdp"], int)
        print("✔ Test 2: Data types (int) are correct.")

    def test_3_get_country_info_success(self):
        """Test: Can a country be found by name (case-insensitive)?"""
        info = self.analyzer.get_country_info("bulgaria")
        self.assertIsNotNone(info)
        self.assertEqual(info["name"], "Bulgaria")
        self.assertEqual(info["population"], 6900000)
        print("✔ Test 3: Search by name is working.")

    def test_4_get_country_info_fail(self):
        """Test: Does it return None or error for a non-existent country?"""
        result = self.analyzer.get_country_info("Atlantis")
        self.assertIsNone(result)
        print("✔ Test 4: Handling of missing country works.")

    def test_5_filter_by_region(self):
        """Test: Are all countries from a specific region retrieved correctly?"""
        asia_countries = self.analyzer.get_all_countries_in_a_certain_region("Asia")
        self.assertEqual(len(asia_countries), 2)
        print("✔ Test 5: Filtering by region is accurate.")

    def test_6_top_5_population(self):
        """Test: Does sorting by population work correctly?"""
        top_5 = self.analyzer.get_top_5_countries_by_population()
        self.assertEqual(top_5[0]["name"], "China")  # China should be first
        self.assertEqual(len(top_5), 5)
        print("✔ Test 6: Population ranking is correct.")

    def test_7_top_5_gdp(self):
        """Test: Does sorting by GDP work correctly?"""
        top_5 = self.analyzer.get_top_5_countries_by_gdp()
        self.assertEqual(top_5[0]["name"], "China")
        self.assertEqual(top_5[1]["name"], "Japan")
        print("✔ Test 7: GDP ranking is correct.")

    def test_8_continent_analysis_math(self):
        """Test: Is the math for total continent population correct?"""
        analysis = self.analyzer.get_full_continent_analysis()
        europe_pop = 6900000 + 83000000
        self.assertEqual(analysis["Europe"]["Total Population"], europe_pop)
        print("✔ Test 8: Mathematical calculations for continents are accurate.")

    def test_9_filter_by_range(self):
        """Test: Does the population range filter work?"""
        # Countries between 50M and 150M (Egypt, Japan)
        filtered = self.analyzer.filter_by_population_range(50000000, 150000000)
        self.assertEqual(len(filtered), 2)
        print("✔ Test 9: Range filtering works.")

    def test_10_top_in_continent(self):
        """Test: Is the top country in a specific continent found correctly?"""
        top_africa = self.analyzer.get_top_5_in_continents("Africa")
        self.assertEqual(top_africa[0]["name"], "Nigeria")
        print("✔ Test 10: Top country in continent found successfully.")

if __name__ == "__main__":
    unittest.main()