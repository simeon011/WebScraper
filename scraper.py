from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import csv

URL_POPULATION = "https://www.worldometers.info/geography/countries-of-the-world/"
URL_GDP = "https://www.worldometers.info/gdp/gdp-by-country/"
FILE_FOR_SAVE = "countries_data.csv"


class Scraper:

    def __init__(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.implicitly_wait(10)

    def run(self):
        print("Start on scrapping...")
        data = {}

        try:
            self.driver.get(URL_POPULATION)
            rows_data = self.driver.execute_script("""
                var rows = document.querySelectorAll('table tbody tr');
                return Array.from(rows).map(row => {
                    var cols = row.querySelectorAll('td');
                    return Array.from(cols).map(col => col.innerText.trim());
                }).filter(cols => cols.length >= 4);
            """)

            for cols in rows_data:
                name_of_country = cols[1]
                pop_text = cols[2].replace(",", "").replace(" ", "")
                try:
                    population = float(pop_text)
                except ValueError:
                    population = 0
                region = cols[3]
                data[name_of_country] = {
                    "population": population,
                    "region": region,
                    "GDP": 0
                }

            print("Get data for GDP")
            self.driver.get(URL_GDP)
            rows_gdp_data = self.driver.execute_script("""
                var rows = document.querySelectorAll('div.datatable-container table tbody tr');
                return Array.from(rows).map(row => {
                    var cols = row.querySelectorAll('td');
                    return Array.from(cols).map(col => col.innerText.trim());
                }).filter(cols => cols.length >= 4);
            """)

            for cols in rows_gdp_data:
                name_of_country = cols[1]
                gdp_text = cols[3].replace(",", "").replace("$", "").replace(" ", "")
                try:
                    gdp = float(gdp_text)
                except ValueError:
                    gdp = 0
                if name_of_country in data:
                    data[name_of_country]["GDP"] = gdp

            self.save_to_csv(data)

        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            self.driver.quit()

    def save_to_csv(self, data):
        try:
            with open(FILE_FOR_SAVE, "w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["name", "population", "region", "GDP"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for country_name, stats in data.items():
                    writer.writerow({
                        "name": country_name,
                        "population": stats["population"],
                        "region": stats["region"],
                        "GDP": stats["GDP"]
                    })
            print(f"Successfully saved {len(data)} countries to {FILE_FOR_SAVE}")
        except Exception as e:
            print(f"Error saving CSV: {e}")
