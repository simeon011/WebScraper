import csv


class Analyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        countries = []
        try:
            with open(self.file_path, 'r', encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    countries.append({
                        "name": row["name"],
                        "population": int(float(row["population"])),
                        "region": row["region"],
                        "GDP": int(float(row["GDP"]))
                    })
                return countries
        except FileNotFoundError:
            print("Error: CSV file not found. Please run the scraper first.")
            return []

    def get_country_info(self, name):
        for country in self.data:
            if country["name"].lower() == name.lower():
                return {
                    "Country": country["name"],
                    "Population": country["population"],
                    "GDP": country["GDP"]
                }
        return "Error no country with that name"

    def get_all_countries_in_a_certain_region(self, region):
        result = []
        for country in self.data:
            if country["region"].lower() == region.lower():
                result.append(country)
        return result

    def get_full_continent_analysis(self):
        analysis = {}
        for country in self.data:
            cont = country["region"]
            if cont not in analysis:
                analysis[cont] = {"pop_list": [], "gdp_list": []}

            analysis[cont]["pop_list"].append(country["population"])
            analysis[cont]["gdp_list"].append(country["GDP"])

        results = {}
        for cont, values in analysis.items():
            total_pop = sum(values["pop_list"])
            total_gdp = sum(values["gdp_list"])
            count = len(values["pop_list"])

            results[cont] = {
                "Total Population": total_pop,
                "Total GDP": total_gdp,
                "Average Population": round(total_pop / count, 2),
                "Average GDP": round(total_gdp / count, 2)
            }
        return results

    def get_top_5_countries_by_population(self):
        sorted_list = sorted(self.data, key=lambda x: x["population"], reverse=True)
        return sorted_list[:5]

    def get_top_5_countries_by_gdp(self):
        sorted_list = sorted(self.data, key=lambda x: x["GDP"], reverse=True)
        return sorted_list[:5]

    def get_top_5_in_continents(self, continent, populations="population"):
        continent_countries = []
        for country in self.data:
            if country["region"].lower() == continent.lower():
                continent_countries.append(country)
        sorted_data = sorted(continent_countries, key=lambda x: x[populations], reverse=True)
        return sorted_data[:5]

    def filter_by_population_range(self, min_val=0, max_val=float('inf')):
        filtered = []
        for c in self.data:
            if min_val <= c["population"] <= max_val:
                filtered.append(c)
        return filtered

