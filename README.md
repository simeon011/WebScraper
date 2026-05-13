# Global Data Analyzer

A Python CLI tool that scrapes and analyzes global country data (population and GDP) from [Worldometers](https://www.worldometers.info).

## Features

- Scrape live data for 195+ countries (population, region, GDP)
- Top 5 countries by population
- Top 5 countries by GDP
- Full continent/region analysis (total and average population & GDP)
- Search for a specific country
- Filter countries by population range

## Project Structure

```
WebScraper/
├── main.py                     # CLI entry point (Bulgarian language menu)
├── scraper.py                  # Selenium web scraper
├── analyzer.py                 # Data analysis logic
├── countries_data.csv          # Scraped data storage
├── table_population_photos/    # Reference screenshots (see below)
└── table_gdp_photos/           # Reference screenshots (see below)
```

## How It Works

### Scraper (`scraper.py`)

Data is scraped from two Worldometers pages:

- **Population & Region:** `worldometers.info/geography/countries-of-the-world/`
- **GDP:** `worldometers.info/gdp/gdp-by-country/`

The scraper uses Selenium with headless Chrome. Because both tables are rendered dynamically by JavaScript, standard Selenium element iteration (`.text`) returns empty strings. Instead, data is extracted in a single `execute_script` call using `innerText`, which reads the fully rendered content directly from the browser.

### Finding the Column Indices

To identify which column index (`col[0]`, `col[1]`, etc.) holds each piece of data, the table structure was inspected manually using browser DevTools. Screenshots of each column were taken and saved in:

- `table_population_photos/` — documents index 1 (country name), index 2 (population), index 3 (region)
- `table_gdp_photos/` — documents index 1 (country name), index 3 (GDP value)

These photos serve as reference for the column mapping used in the scraper.

### Analyzer (`analyzer.py`)

Reads the CSV file and provides:

| Method | Description |
|--------|-------------|
| `get_top_5_countries_by_population()` | Top 5 by population |
| `get_top_5_countries_by_gdp()` | Top 5 by GDP |
| `get_full_continent_analysis()` | Totals and averages per region |
| `get_country_info(name)` | Search by country name |
| `get_top_5_in_continents(continent)` | Top 5 in a specific region |
| `filter_by_population_range(min, max)` | Filter by population range |

## Installation

```bash
pip install selenium webdriver-manager
```

Chrome must be installed on your system. `webdriver-manager` handles the ChromeDriver automatically.

## Usage

```bash
python main.py
```

**Always run option 1 (Scrape) first** to populate `countries_data.csv` before using any analysis options. Scraping takes approximately 15–30 seconds.

## Data Sources

- [Worldometers — Countries of the World](https://www.worldometers.info/geography/countries-of-the-world/)
- [Worldometers — GDP by Country](https://www.worldometers.info/gdp/gdp-by-country/)
