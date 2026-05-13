import os
from scraper import Scraper
from analyzer import Analyzer


def clear_screen():
    """Clears the console based on the operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    FILE_PATH = "countries_data.csv"

    while True:
        print("\n" + "=" * 40)
        print("      GLOBAL DATA ANALYZER")
        print("=" * 40)
        print("1. Update Data (Scrape)")
        print("2. Top 5 Countries by Population")
        print("3. Top 5 Countries by GDP")
        print("4. Continent Analysis")
        print("5. Search for a Country")
        print("6. Filter by Population Range")
        print("0. Exit")
        print("=" * 40)

        choice = input("Select an option: ")

        if choice == "1":
            print("Starting scraper... Please wait.")
            scraper = Scraper()
            scraper.run()
            input("\nData updated! Press Enter for menu...")

        elif choice in ["2", "3", "4", "5", "6"]:
            if not os.path.exists(FILE_PATH):
                print(f"\nERROR: File '{FILE_PATH}' not found. Please select option 1 first.")
                input("Press Enter...")
                continue

            analyzer = Analyzer(FILE_PATH)

            if choice == "2":
                top_pop = analyzer.get_top_5_countries_by_population()
                print("\n--- TOP 5 BY POPULATION ---")
                for c in top_pop:
                    print(f"{c['name']}: {int(c['population']):,}")

            elif choice == "3":
                top_gdp = analyzer.get_top_5_countries_by_gdp()
                print("\n--- TOP 5 BY GDP ---")
                for c in top_gdp:
                    # Използваме 'gdp' с малки букви, за да съвпадне с Analyzer
                    print(f"{c['name']}: ${int(c['gdp']):,}")

            elif choice == "4":
                analysis = analyzer.get_full_continent_analysis()
                print("\n--- CONTINENT ANALYSIS ---")
                for cont, vals in analysis.items():
                    print(f"\nRegion: {cont}")
                    print(f"  - Total Population: {int(vals['Total Population']):,}")
                    print(f"  - Avg GDP: ${vals['Average GDP']:,}")

            elif choice == "5":
                name = input("Enter country name: ")
                info = analyzer.get_country_info(name)
                if info and isinstance(info, dict):
                    print(f"\nResult for {info['name']}:")
                    print(f"  - Population: {int(info['population']):,}")
                    print(f"  - GDP: ${int(info['gdp']):,}")
                    print(f"  - Region: {info['region']}")
                else:
                    print(f"\nResult: {info}")

            elif choice == "6":
                try:
                    min_v = float(input("Minimum population: "))
                    max_v = float(input("Maximum population: "))
                    filtered = analyzer.filter_by_population_range(min_v, max_v)
                    print(f"\nCountries found: {len(filtered)}")
                    for c in filtered[:10]:  # Show top 10 results
                        print(f"- {c['name']} ({int(c['population']):,})")
                except ValueError:
                    print("Please enter valid numbers.")

            input("\nPress Enter to return...")

        elif choice == "0":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid option!")
            input("Press Enter...")

        clear_screen()


if __name__ == "__main__":
    main()