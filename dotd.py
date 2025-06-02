import json
import os
import re
from pathlib import Path

import requests

urls = {
    # 2025: "https://www.formula1.com/en/latest/article/driver-of-the-day-2025.1vNM15UysUT1r3A2OMaFqH",
    # 2024: "https://www.formula1.com/en/latest/article/driver-of-the-day-2024.1I7A0iPl3nMaXyPIeFVFLZ",
    # 2023: "https://www.formula1.com/en/latest/article/driver-of-the-day-2023.5wGE2ke3SFqQwabYVQXLnF",
    # 2022: "https://www.formula1.com/en/latest/article/driver-of-the-day-2022.6pXweJZLe1l3puCiid9aj3",
    2021: "https://www.formula1.com/en/latest/article/driver-of-the-day-2021.78AqC4wM6NVtaNH1mZA4on",
    2020: "https://www.formula1.com/en/latest/article/driver-of-the-day-2020.30G6kHOGAe7Wcz2KBwwObh",
    2019: "https://www.formula1.com/en/latest/article/driver-of-the-day-2019.4Mflx1u6tsAABdwuDIvXb8",
    # 2018: "https://www.formula1.com/en/latest/article/driver-of-the-day.6dwMp9DDgssMeaAkgYuusQ",
    # 2017: "http://web.archive.org/web/20190413234558/https://www.formula1.com/en/results/awards/driver-of-the-day-2017.html",
    # 2016: "http://web.archive.org/web/20180923235349/https://www.formula1.com/en/results/awards/driver-of-the-day-2016.html",
}


F1_RACES = {
    2025: {
        "FORMULA 1 LOUIS VUITTON AUSTRALIAN GRAND PRIX 2025": "Australian Grand Prix",
        "FORMULA 1 HEINEKEN CHINESE GRAND PRIX 2025": "Chinese Grand Prix",
        "FORMULA 1 LENOVO JAPANESE GRAND PRIX 2025": "Japanese Grand Prix",
        "FORMULA 1 GULF AIR BAHRAIN GRAND PRIX 2025": "Bahrain Grand Prix",
        "FORMULA 1 STC SAUDI ARABIAN GRAND PRIX 2025": "Saudi Arabian Grand Prix",
        "FORMULA 1 CRYPTO.COM MIAMI GRAND PRIX 2025": "Miami Grand Prix",
        "FORMULA 1 AWS GRAN PREMIO DEL MADE IN ITALY E DELL'EMILIA-ROMAGNA 2025": "Emilia Romagna Grand Prix",
        "FORMULA 1 TAG HEUER GRAND PRIX DE MONACO 2025": "Monaco Grand Prix",
        "FORMULA 1 ARAMCO GRAN PREMIO DE ESPANA 2025": "Spanish Grand Prix",
        "FORMULA 1 PIRELLI GRAND PRIX DU CANADA 2025": "Canadian Grand Prix",
        "FORMULA 1 MSC CRUISES AUSTRIAN GRAND PRIX 2025": "Austrian Grand Prix",
        "FORMULA 1 QATAR AIRWAYS BRITISH GRAND PRIX 2025": "British Grand Prix",
        "FORMULA 1 MOET & CHANDON BELGIAN GRAND PRIX 2025": "Belgian Grand Prix",
        "FORMULA 1 LENOVO HUNGARIAN GRAND PRIX 2025": "Hungarian Grand Prix",
        "FORMULA 1 HEINEKEN DUTCH GRAND PRIX 2025": "Dutch Grand Prix",
        "FORMULA 1 PIRELLI GRAN PREMIO D’ITALIA 2025": "Italian Grand Prix",
        "FORMULA 1 QATAR AIRWAYS AZERBAIJAN GRAND PRIX 2025": "Azerbaijan Grand Prix",
        "FORMULA 1 SINGAPORE AIRLINES SINGAPORE GRAND PRIX 2025": "Singapore Grand Prix",
        "FORMULA 1 MSC CRUISES UNITED STATES GRAND PRIX 2025": "United States Grand Prix",
        "FORMULA 1 GRAN PREMIO DE LA CIUDAD DE MEXICO 2025": "Mexico City Grand Prix",
        "FORMULA 1 MSC CRUISES GRANDE PREMIO DE SAO PAULO 2025": "São Paulo Grand Prix",
        "FORMULA 1 HEINEKEN LAS VEGAS GRAND PRIX 2025": "Las Vegas Grand Prix",
        "FORMULA 1 QATAR AIRWAYS QATAR GRAND PRIX 2025": "Qatar Grand Prix",
        "FORMULA 1 ETIHAD AIRWAYS ABU DHABI GRAND PRIX 2025": "Abu Dhabi Grand Prix",
    },
    2024: {
        "FORMULA 1 ETIHAD AIRWAYS ABU DHABI GRAND PRIX 2024": "Abu Dhabi Grand Prix",
        "FORMULA 1 QATAR AIRWAYS QATAR GRAND PRIX 2024": "Qatar Grand Prix",
        "FORMULA 1 HEINEKEN SILVER LAS VEGAS GRAND PRIX 2024": "Las Vegas Grand Prix",
        "FORMULA 1 LENOVO GRANDE PREMIO DE SAO PAULO 2024": "São Paulo Grand Prix",
        "FORMULA 1 GRAN PREMIO DE LA CIUDAD DE MEXICO 2024": "Mexico City Grand Prix",
        "FORMULA 1 PIRELLI UNITED STATES GRAND PRIX 2024": "United States Grand Prix",
        "FORMULA 1 SINGAPORE AIRLINES SINGAPORE GRAND PRIX 2024": "Singapore Grand Prix",
        "FORMULA 1 QATAR AIRWAYS AZERBAIJAN GRAND PRIX 2024": "Azerbaijan Grand Prix",
        "FORMULA 1 PIRELLI GRAN PREMIO D’ITALIA 2024": "Italian Grand Prix",
        "FORMULA 1 HEINEKEN DUTCH GRAND PRIX 2024": "Dutch Grand Prix",
        "FORMULA 1 ROLEX BELGIAN GRAND PRIX 2024": "Belgian Grand Prix",
        "FORMULA 1 HUNGARIAN GRAND PRIX 2024": "Hungarian Grand Prix",
        "FORMULA 1 QATAR AIRWAYS BRITISH GRAND PRIX 2024": "British Grand Prix",
        "FORMULA 1 QATAR AIRWAYS AUSTRIAN GRAND PRIX 2024": "Austrian Grand Prix",
        "FORMULA 1 ARAMCO GRAN PREMIO DE ESPANA 2024": "Spanish Grand Prix",
        "FORMULA 1 AWS GRAND PRIX DU CANADA 2024": "Canadian Grand Prix",
        "FORMULA 1 GRAND PRIX DE MONACO 2024": "Monaco Grand Prix",
        "FORMULA 1 MSC CRUISES GRAN PREMIO DEL MADE IN ITALY E DELL'EMILIA-ROMAGNA 2024": "Emilia Romagna Grand Prix",
        "FORMULA 1 CRYPTO.COM MIAMI GRAND PRIX 2024": "Miami Grand Prix",
        "FORMULA 1 LENOVO CHINESE GRAND PRIX 2024": "Chinese Grand Prix",
        "FORMULA 1 MSC CRUISES JAPANESE GRAND PRIX 2024": "Japanese Grand Prix",
        "FORMULA 1 ROLEX AUSTRALIAN GRAND PRIX 2024": "Australian Grand Prix",
        "FORMULA 1 STC SAUDI ARABIAN GRAND PRIX 2024": "Saudi Arabian Grand Prix",
        "FORMULA 1 GULF AIR BAHRAIN GRAND PRIX 2024": "Bahrain Grand Prix",
    },
    2023: {
        "FORMULA 1 ETIHAD AIRWAYS ABU DHABI GRAND PRIX 2023": "Abu Dhabi Grand Prix",
        "FORMULA 1 HEINEKEN SILVER LAS VEGAS GRAND PRIX 2023": "Las Vegas Grand Prix",
        "FORMULA 1 ROLEX GRANDE PREMIO DE SAO PAULO 2023": "São Paulo Grand Prix",
        "FORMULA 1 GRAN PREMIO DE LA CIUDAD DE MEXICO 2023": "Mexico City Grand Prix",
        "FORMULA 1 LENOVO UNITED STATES GRAND PRIX 2023": "United States Grand Prix",
        "FORMULA 1 QATAR AIRWAYS QATAR GRAND PRIX 2023": "Qatar Grand Prix",
        "FORMULA 1 LENOVO JAPANESE GRAND PRIX 2023": "Japanese Grand Prix",
        "FORMULA 1 SINGAPORE AIRLINES SINGAPORE GRAND PRIX 2023": "Singapore Grand Prix",
        "FORMULA 1 PIRELLI GRAN PREMIO D’ITALIA 2023": "Italian Grand Prix",
        "FORMULA 1 HEINEKEN DUTCH GRAND PRIX 2023": "Dutch Grand Prix",
        "FORMULA 1 MSC CRUISES BELGIAN GRAND PRIX 2023": "Belgian Grand Prix",
        "FORMULA 1 QATAR AIRWAYS HUNGARIAN GRAND PRIX 2023": "Hungarian Grand Prix",
        "FORMULA 1 ARAMCO BRITISH GRAND PRIX 2023": "British Grand Prix",
        "FORMULA 1 ROLEX GROSSER PREIS VON OSTERREICH 2023": "Austrian Grand Prix",
        "FORMULA 1 PIRELLI GRAND PRIX DU CANADA 2023": "Canadian Grand Prix",
        "FORMULA 1 AWS GRAN PREMIO DE ESPANA 2023": "Spanish Grand Prix",
        "FORMULA 1 GRAND PRIX DE MONACO 2023": "Monaco Grand Prix",
        "FORMULA 1 CRYPTO.COM MIAMI GRAND PRIX 2023": "Miami Grand Prix",
        "FORMULA 1 AZERBAIJAN GRAND PRIX 2023": "Azerbaijan Grand Prix",
        "FORMULA 1 ROLEX AUSTRALIAN GRAND PRIX 2023": "Australian Grand Prix",
        "FORMULA 1 STC SAUDI ARABIAN GRAND PRIX 2023": "Saudi Arabian Grand Prix",
        "FORMULA 1 GULF AIR BAHRAIN GRAND PRIX 2023": "Bahrain Grand Prix",
    },
    2022: {
        "FORMULA 1 ETIHAD AIRWAYS ABU DHABI GRAND PRIX 2022": "Abu Dhabi Grand Prix",
        "FORMULA 1 HEINEKEN GRANDE PREMIO DE SAO PAULO 2022": "São Paulo Grand Prix",
        "FORMULA 1 GRAN PREMIO DE LA CIUDAD DE MEXICO 2022": "Mexico City Grand Prix",
        "FORMULA 1 ARAMCO UNITED STATES GRAND PRIX 2022": "United States Grand Prix",
        "FORMULA 1 HONDA JAPANESE GRAND PRIX 2022": "Japanese Grand Prix",
        "FORMULA 1 SINGAPORE AIRLINES SINGAPORE GRAND PRIX 2022": "Singapore Grand Prix",
        "FORMULA 1 PIRELLI GRAN PREMIO D’ITALIA 2022": "Italian Grand Prix",
        "FORMULA 1 HEINEKEN DUTCH GRAND PRIX 2022": "Dutch Grand Prix",
        "FORMULA 1 ROLEX BELGIAN GRAND PRIX 2022": "Belgian Grand Prix",
        "FORMULA 1 ARAMCO MAGYAR NAGYDIJ 2022": "Hungarian Grand Prix",
        "FORMULA 1 LENOVO GRAND PRIX DE FRANCE 2022": "French Grand Prix",
        "FORMULA 1 ROLEX GROSSER PREIS VON OSTERREICH 2022": "Austrian Grand Prix",
        "FORMULA 1 LENOVO BRITISH GRAND PRIX 2022": "British Grand Prix",
        "FORMULA 1 AWS GRAND PRIX DU CANADA 2022": "Canadian Grand Prix",
        "FORMULA 1 AZERBAIJAN GRAND PRIX 2022": "Azerbaijan Grand Prix",
        "FORMULA 1 GRAND PRIX DE MONACO 2022": "Monaco Grand Prix",
        "FORMULA 1 PIRELLI GRAN PREMIO DE ESPANA 2022": "Spanish Grand Prix",
        "FORMULA 1 CRYPTO.COM MIAMI GRAND PRIX 2022": "Miami Grand Prix",
        "FORMULA 1 ROLEX GRAN PREMIO DEL MADE IN ITALY E DELL'EMILIA-ROMAGNA 2022": "Emilia Romagna Grand Prix",
        "FORMULA 1 HEINEKEN AUSTRALIAN GRAND PRIX 2022": "Australian Grand Prix",
        "FORMULA 1 STC SAUDI ARABIAN GRAND PRIX 2022": "Saudi Arabian Grand Prix",
        "FORMULA 1 GULF AIR BAHRAIN GRAND PRIX 2022": "Bahrain Grand Prix",
    },
    2021: {
        "Formula 1 Etihad Airways Abu Dhabi Grand Prix 2021": "Abu Dhabi Grand Prix",
        "Formula 1 stc Saudi Arabian Grand Prix 2021": "Saudi Arabian Grand Prix",
        "Formula 1 Ooredoo Qatar Grand Prix 2021": "Qatar Grand Prix",
        "Formula 1 Heineken Grande Prêmio de São Paulo 2021": "São Paulo Grand Prix",
        "Formula 1 Gran Premio de la Ciudad de México 2021": "Mexico City Grand Prix",
        "Formula 1 Aramco United States Grand Prix 2021": "United States Grand Prix",
        "Formula 1 Rolex Turkish Grand Prix 2021": "Turkish Grand Prix",
        "Formula 1 VTB Russian Grand Prix 2021": "Russian Grand Prix",
        "Formula 1 Heineken Gran Premio d’Italia 2021": "Italian Grand Prix",
        "Formula 1 Heineken Dutch Grand Prix 2021": "Dutch Grand Prix",
        "Formula 1 Rolex Magyar Nagydíj 2021": "Hungarian Grand Prix",
        "Formula 1 Pirelli British Grand Prix 2021": "British Grand Prix",
        "Formula 1 BWT Grosser Preis von Osterreich 2021": "Austrian Grand Prix",
        "Formula 1 Grosser Preis Der Steiermark 2021": "Styrian Grand Prix",
        "Formula 1 Emirates Grand Prix de France 2021": "French Grand Prix",
        "Formula 1 Azerbaijan Grand Prix 2021": "Azerbaijan Grand Prix",
        "Formula 1 Grand Prix de Monaco 2021": "Monaco Grand Prix",
        "Formula 1 Aramco Gran Premio de España 2021": "Spanish Grand Prix",
        "Formula 1 Heineken Grande Prémio de Portugal 2021": "Portuguese Grand Prix",
        "Formula 1 Pirelli Gran Premio del Made In Italy e dell'Emilia Romagna 2021": "Emilia Romagna Grand Prix",
        "Formula 1 Gulf Air Bahrain Grand Prix 2021": "Bahrain Grand Prix",
    },
    2020: {
        "Formula 1 Etihad Airways Abu Dhabi Grand Prix 2020": "Abu Dhabi Grand Prix",
        "Formula 1 Rolex Sakhir Grand Prix 2020": "Sakhir Grand Prix",
        "Formula 1 Gulf Air Bahrain Grand Prix 2020": "Bahrain Grand Prix",
        "Formula 1 DHL Turkish Grand Prix 2020": "Turkish Grand Prix",
        "Formula 1 Emirates Gran Premio dell'Emilia Romagna 2020": "Emilia Romagna Grand Prix",
        "Formula 1 Heineken Portuguese Grand Prix 2020": "Portuguese Grand Prix",
        "Formula 1 Aramco Grosser Preis der Eifel 2020": "Eifel Grand Prix",
        "Formula 1 VTB Russian Grand Prix 2020": "Russian Grand Prix",
        "Formula 1 Pirelli Gran Premio della Toscana Ferrari 1000 2020": "Tuscan Grand Prix",
        "Formula 1 Gran Premio Heineken d’Italia 2020": "Italian Grand Prix",
        "Formula 1 Rolex Belgian Grand Prix 2020": "Belgian Grand Prix",
        "Formula 1 Aramco Gran Premio de Espana 2020": "Spanish Grand Prix",
        "Emirates Formula 1 70th Anniversary Grand Prix 2020": "70th Anniversary Grand Prix",
        "Formula 1 Pirelli British Grand Prix 2020": "British Grand Prix",
        "Formula 1 Aramco Magyar Nagydij 2020": "Hungarian Grand Prix",
        "Formula 1 Pirelli Grosser Preis Der Steiermark 2020": "Styrian Grand Prix",
        "Formula 1 Rolex Grosser Preis von Osterreich 2020": "Austrian Grand Prix",
    },
    2019: {
        "Formula 1 Etihad Airways Abu Dhabi Grand Prix 2019": "Abu Dhabi Grand Prix",
        "Formula 1 Heineken Grande Premio do Brasil 2019": "Brazilian Grand Prix",
        "Formula 1 Emirates United States Grand Prix 2019": "United States Grand Prix",
        "Formula 1 Gran Premio de Mexico 2019": "Mexican Grand Prix",
        "Formula 1 Japanese Grand Prix 2019": "Japanese Grand Prix",
        "Formula 1 VTB Russian Grand Prix 2019": "Russian Grand Prix",
        "Formula 1 Singapore Airlines Singapore Grand Prix 2019": "Singapore Grand Prix",
        "Formula 1 Gran Premio Heineken d'Italia 2019": "Italian Grand Prix",
        "Formula 1 Johnnie Walker Belgian Grand Prix 2019": "Belgian Grand Prix",
        "Formula 1 Rolex Magyar Nagydij 2019": "Hungarian Grand Prix",
        "Formula 1 Mercedes-Benz Grosser Preis von Deutschland 2019": "German Grand Prix",
        "Formula 1 Rolex British Grand Prix 2019": "British Grand Prix",
        "Formula 1 myWorld Grosser Preis von Osterreich 2019": "Austrian Grand Prix",
        "Formula 1 Pirelli Grand Prix de France 2019": "French Grand Prix",
        "Formula 1 Pirelli Grand Prix du Canada 2019": "Canadian Grand Prix",
        "Formula 1 Grand Prix de Monaco 2019": "Monaco Grand Prix",
        "Formula 1 Emirates Gran Premio de Espana 2019": "Spanish Grand Prix",
        "Formula 1 Socar Azerbaijan Grand Prix 2019": "Azerbaijan Grand Prix",
        "Formula 1 Heineken Chinese Grand Prix 2019": "Chinese Grand Prix",
        "Formula 1 Gulf Air Bahrain Grand Prix 2019": "Bahrain Grand Prix",
        "Formula 1 Rolex Australian Grand Prix 2019": "Australian Grand Prix",
    },
    2018: {
        "Formula 1 2018 Etihad Airways Abu Dhabi Grand Prix": "Abu Dhabi Grand Prix",
        "Formula 1 Grande Premio Heineken do Brasil 2018": "Brazilian Grand Prix",
        "Formula 1 Gran Premio de Mexico 2018": "Mexican Grand Prix",
        "Formula 1 Pirelli 2018 United States Grand Prix": "United States Grand Prix",
        "Formula 1 2018 Honda Japanese Grand Prix": "Japanese Grand Prix",
        "Formula 1 2018 VTB Russian Grand Prix": "Russian Grand Prix",
        "Formula 1 2018 Singapore Airlines Singapore Grand Prix": "Singapore Grand Prix",
        "Formula 1 Gran Premio Heineken d'Italia 2018": "Italian Grand Prix",
        "Formula 1 2018 Johnnie Walker Belgian Grand Prix": "Belgian Grand Prix",
        "Formula 1 Rolex Magyar Nagydij 2018": "Hungarian Grand Prix",
        "Formula 1 Emirates Grosser Preis von Deutschland 2018": "German Grand Prix",
        "Formula 1 2018 Rolex British Grand Prix": "British Grand Prix",
        "Formula 1 Eyetime Grosser Preis von Osterreich 2018": "Austrian Grand Prix",
        "Formula 1 Pirelli Grand Prix de France 2018": "French Grand Prix",
        "Formula 1 Grand Prix Heineken du Canada 2018": "Canadian Grand Prix",
        "Formula 1 Grand Prix de Monaco 2018": "Monaco Grand Prix",
        "Formula 1 Gran Premio de Espana Emirates 2018": "Spanish Grand Prix",
        "Formula 1 2018 Azerbaijan Grand Prix": "Azerbaijan Grand Prix",
        "Formula 1 2018 Heineken Chinese Grand Prix": "Chinese Grand Prix",
        "Formula 1 2018 Gulf Air Bahrain Grand Prix": "Bahrain Grand Prix",
        "Formula 1 2018 Rolex Australian Grand Prix": "Australian Grand Prix",
    },
}


def fetch_markdown_from_url(url):
    """Fetch markdown content from Jina AI URL"""
    jina_url = f"https://r.jina.ai/{url}"

    try:
        print(f"Fetching data from: {jina_url}")
        response = requests.get(jina_url, timeout=30)
        response.raise_for_status()

        print(f"Successfully fetched {len(response.text)} characters")
        return response.text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from URL: {e}")
        return None


def extract_dotd_data(content, year):
    """Extract Driver of the Day data from markdown content"""

    # Get race mappings for the year
    race_mappings = F1_RACES.get(year, {})

    # Find all race sections
    race_sections = re.findall(
        r"### (FORMULA 1 .+? \d{4})\n\n.*?\n\n(.*?)\n\n\*\*(.*?)\*\*",
        content,
        re.DOTALL,
    )

    all_races_data = []

    for race_title, description, voting_data in race_sections:
        # Get clean race name from mapping
        clean_race_name = race_mappings.get(
            race_title,
            race_title.replace("FORMULA 1 ", "").replace(f" {year}", "").strip(),
        )

        # Extract voting percentages
        vote_lines = voting_data.strip().split("\n")
        drivers_votes = []

        for line in vote_lines:
            line = line.strip()
            if " - " in line and "%" in line:
                # Split driver name and percentage
                parts = line.split(" - ")
                if len(parts) == 2:
                    driver_name = parts[0].strip()
                    percentage = parts[1].strip().replace("%", "")

                    try:
                        percentage_float = float(percentage)
                        drivers_votes.append(
                            {"driver": driver_name, "percentage": percentage_float}
                        )
                    except ValueError:
                        continue

        # Create race data structure
        race_data = {
            "race_name": clean_race_name,
            "year": int(year),
            "winner": drivers_votes[0]["driver"] if drivers_votes else None,
            "voting_results": drivers_votes,
        }

        all_races_data.append(race_data)

        # Create folder structure and save individual race file
        save_race_data(race_data, year, clean_race_name)

    return all_races_data


def save_race_data(race_data, year, clean_race_name):
    """Save individual race data to JSON file in organized folder structure"""

    # Create year folder
    year_folder = Path(str(year))
    year_folder.mkdir(exist_ok=True)

    # Create race folder using clean race name as is
    race_folder = year_folder / clean_race_name
    race_folder.mkdir(exist_ok=True)

    # Save race data as JSON
    json_file = race_folder / "dotd.json"

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(race_data, f, indent=2, ensure_ascii=False)

    print(f"Saved: {json_file}")


def process_year(year, url):
    """Process DOTD data for a specific year"""

    print(f"\n{'=' * 50}")
    print(f"Processing {year} Driver of the Day data...")
    print(f"{'=' * 50}")

    # Fetch markdown content from URL
    content = fetch_markdown_from_url(url)

    if not content:
        print(f"Failed to fetch data for {year}!")
        return []

    try:
        print("Extracting race data...")
        all_races = extract_dotd_data(content, year)

        if not all_races:
            print(f"No race data found for {year}!")
            return []

        # Save summary file with all races for the year
        summary_file = Path(str(year)) / f"dotd_{year}.json"

        summary_data = {
            "year": year,
            "total_races": len(all_races),
            "last_updated": "2025-01-27",
            "source_url": url,
            "races": all_races,
        }

        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Extraction complete for {year}!")
        print(f"📊 Total races processed: {len(all_races)}")
        print(f"📁 Summary saved: {summary_file}")

        # Print race list
        print(f"\n🏁 Races processed for {year}:")
        for i, race in enumerate(all_races, 1):
            print(f"{i:2d}. {race['race_name']} - Winner: {race['winner']}")

        return all_races

    except Exception as e:
        print(f"❌ Error processing data for {year}: {e}")
        import traceback

        traceback.print_exc()
        return []


def main():
    """Main function to process all years of DOTD data"""

    print("🏎️  Formula 1 Driver of the Day Data Extractor")
    print("=" * 60)

    all_years_data = {}

    for year, url in urls.items():
        races_data = process_year(year, url)
        if races_data:
            all_years_data[year] = races_data

    # Create overall summary
    if all_years_data:
        overall_summary = {
            "years_processed": list(all_years_data.keys()),
            "total_years": len(all_years_data),
            "total_races": sum(len(races) for races in all_years_data.values()),
            "last_updated": "2025-01-27",
            "data_by_year": {
                year: {
                    "total_races": len(races),
                    "races": [race["race_name"] for race in races],
                }
                for year, races in all_years_data.items()
            },
        }

        with open("dotd_overall_summary.json", "w", encoding="utf-8") as f:
            json.dump(overall_summary, f, indent=2, ensure_ascii=False)

        print(f"\n🎯 Overall Summary:")
        print(f"📅 Years processed: {len(all_years_data)}")
        print(f"🏁 Total races: {sum(len(races) for races in all_years_data.values())}")
        print(f"📁 Overall summary saved: dotd_overall_summary.json")


if __name__ == "__main__":
    main()
