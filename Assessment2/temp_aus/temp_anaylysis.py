import os
import csv
from collections import defaultdict

# Folder where temperature CSV files are stored
temperature_data_path = '../data_files/temperature_data'


import os
import csv
from collections import defaultdict

def read_temperature_data(folder_path):
    station_data = defaultdict(list)
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        try:
                            station = row['STATION_NAME']
                            monthly_temps = [float(row[month]) for month in [
                                'January', 'February', 'March', 'April', 'May', 'June',
                                'July', 'August', 'September', 'October', 'November', 'December'] if row[month]]
                            if len(monthly_temps) == 12:
                                station_data[station].append(monthly_temps)
                        except (ValueError, KeyError):
                            continue
        return station_data
    except Exception as e:
        print(f"Error reading files: {e}")
        return {}

def calculate_seasonal_averages(data):
    seasons = {
        'Summer': [11, 0, 1],
        'Autumn': [2, 3, 4],
        'Winter': [5, 6, 7],
        'Spring': [8, 9, 10]
    }
    season_totals = defaultdict(float)
    season_counts = defaultdict(int)

    for records in data.values():
        for year in records:
            for season, indices in seasons.items():
                try:
                    temps = [year[i] for i in indices]
                    season_totals[season] += sum(temps)
                    season_counts[season] += len(temps)
                except IndexError:
                    continue

    try:
        with open("./analysis/average_temp.txt", 'w') as f:
            for season in seasons:
                if season_counts[season] > 0:
                    avg = season_totals[season] / season_counts[season]
                    f.write(f"{season}: {avg:.2f}\n")
    except Exception as e:
        print(f"Error writing seasonal averages: {e}")

def find_largest_temp_range(data):
    max_range = -1
    stations = []

    for station, records in data.items():
        all_temps = [temp for year in records for temp in year]
        if not all_temps:
            continue
        temp_range = max(all_temps) - min(all_temps)
        if temp_range > max_range:
            max_range = temp_range
            stations = [station]
        elif temp_range == max_range:
            stations.append(station)

    try:
        with open("./analysis/largest_temp_range_station.txt", 'w') as f:
            for station in stations:
                f.write(f"{station}\n")
    except Exception as e:
        print(f"Error writing temp range file: {e}")

def find_warmest_and_coolest(data):
    averages = {}
    for station, records in data.items():
        temps = [temp for year in records for temp in year]
        if temps:
            avg = sum(temps) / len(temps)
            averages[station] = avg

    if not averages:
        return

    max_avg = max(averages.values())
    min_avg = min(averages.values())

    try:
        with open("./analysis/warmest_and_coolest_station.txt", 'w') as f:
            f.write("Warmest Station(s):\n")
            for station, avg in averages.items():
                if avg == max_avg:
                    f.write(f"{station}\n")
            f.write("\nCoolest Station(s):\n")
            for station, avg in averages.items():
                if avg == min_avg:
                    f.write(f"{station}\n")
    except Exception as e:
        print(f"Error writing warmest/coolest station: {e}")

def main():
    if not os.path.exists(temperature_data_path):
        print(f"Folder not found: {temperature_data_path}")
        return

    data = read_temperature_data(temperature_data_path)
    if not data:
        print("No valid data found.")
        return

    calculate_seasonal_averages(data)
    find_largest_temp_range(data)
    find_warmest_and_coolest(data)

if __name__ == "__main__":
    main()
