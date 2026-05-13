import unittest
from unittest.mock import patch, MagicMock
import os
import main


class TestMainMenu(unittest.TestCase):

    def setUp(self):
        # Path to the test file
        self.file_path = "countries_data.csv"

    @patch('builtins.input', side_effect=['0'])
    @patch('builtins.print')
    def test_exit_logic(self, mock_print, mock_input):
        """Test 1: Verify the program exits correctly when '0' is selected"""
        main.main()
        # Check if the goodbye message was printed
        mock_print.assert_any_call("Exiting. Goodbye!")
        print("✔ Test 1: Menu exit (0) works correctly.")

    @patch('os.path.exists', return_value=False)
    @patch('builtins.input', side_effect=['2', '0'])
    @patch('builtins.print')
    def test_missing_file_error(self, mock_print, mock_input, mock_exists):
        """Test 2: Check for error message if the CSV file is missing"""
        main.main()
        mock_print.assert_any_call(f"\nERROR: File '{self.file_path}' not found. Please select option 1 first.")
        print("✔ Test 2: Protection against missing CSV file works.")

    @patch('builtins.input', side_effect=['9', '0'])
    @patch('builtins.print')
    def test_invalid_option(self, mock_print, mock_input):
        """Test 3: Check for invalid menu option handling"""
        main.main()
        mock_print.assert_any_call("Invalid option!")
        print("✔ Test 3: Handling of invalid option (e.g., 9) works.")

    @patch('main.Scraper')
    @patch('builtins.input', side_effect=['1', '', '0'])
    def test_scraper_integration(self, mock_input, mock_scraper_class):
        """Test 4: Verify that option 1 calls the Scraper class"""
        # Create a mock object for the scraper
        mock_scraper_instance = mock_scraper_class.return_value

        main.main()

        # Verify Scraper was instantiated and the run method was called
        mock_scraper_class.assert_called_once()
        mock_scraper_instance.run.assert_called_once()
        print("✔ Test 4: Option 1 successfully activates the Scraper.")

    @patch('main.Analyzer')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.input', side_effect=['5', 'Bulgaria', '', '0'])
    @patch('builtins.print')
    def test_search_country_call(self, mock_print, mock_input, mock_exists, mock_analyzer_class):
        """Test 5: Verify option 5 calls the country search method"""
        mock_analyzer_instance = mock_analyzer_class.return_value
        mock_analyzer_instance.get_country_info.return_value = {"name": "Bulgaria", "population": 6900000}

        main.main()

        mock_analyzer_instance.get_country_info.assert_called_with('Bulgaria')
        print("✔ Test 5: Option 5 correctly passes the name to the Analyzer.")

    @patch('main.Analyzer')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.input', side_effect=['6', 'invalid', '0'])
    @patch('builtins.print')
    def test_filter_population_error(self, mock_print, mock_input, mock_exists, mock_analyzer_class):
        """Test 6: Check for ValueError in the population filter (option 6)"""
        main.main()
        mock_print.assert_any_call("Please enter valid numbers.")
        print("✔ Test 6: Caught invalid input (text instead of number) in option 6.")

    @patch('main.Analyzer')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.input', side_effect=['2', '', '0'])
    def test_top_population_call(self, mock_input, mock_exists, mock_analyzer_class):
        """Test 7: Does option 2 call the Top 5 population method?"""
        mock_analyzer_instance = mock_analyzer_class.return_value
        mock_analyzer_instance.get_top_5_countries_by_population.return_value = []

        main.main()

        mock_analyzer_instance.get_top_5_countries_by_population.assert_called_once()
        print("✔ Test 7: Option 2 activates the population sorting.")

    @patch('main.Analyzer')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.input', side_effect=['3', '', '0'])
    def test_top_gdp_call(self, mock_input, mock_exists, mock_analyzer_class):
        """Test 8: Does option 3 call the Top 5 GDP method?"""
        mock_analyzer_instance = mock_analyzer_class.return_value
        mock_analyzer_instance.get_top_5_countries_by_gdp.return_value = []

        main.main()

        mock_analyzer_instance.get_top_5_countries_by_gdp.assert_called_once()
        print("✔ Test 8: Option 3 activates the GDP sorting.")

    @patch('main.Analyzer')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.input', side_effect=['4', '', '0'])
    def test_continent_analysis_call(self, mock_input, mock_exists, mock_analyzer_class):
        """Test 9: Does option 4 call the full continent analysis?"""
        mock_analyzer_instance = mock_analyzer_class.return_value
        mock_analyzer_instance.get_full_continent_analysis.return_value = {}

        main.main()

        mock_analyzer_instance.get_full_continent_analysis.assert_called_once()
        print("✔ Test 9: Option 4 successfully starts the continent analysis.")

    @patch('main.clear_screen')
    @patch('builtins.input', side_effect=['0'])
    def test_clear_screen_call(self, mock_input, mock_clear):
        """Test 10: Is the screen clearing function called?"""
        main.main()
        # Should be called at least once before exit
        self.assertTrue(mock_clear.called)
        print("✔ Test 10: Console clearing function is active.")


if __name__ == "__main__":
    unittest.main()