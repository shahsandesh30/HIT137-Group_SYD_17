import os
import csv
from collections import defaultdict

# Folder where temperature CSV files are stored
TEMPERATURE_FOLDER = '../data_files/temperature_data'
OUTPUT_FOLDER = './analysis'

# Mapping months to seasons in Australia
SEASON_MAP = {
    '12': 'Summer', '01': 'Summer', '02': 'Summer',
    '03': 'Autumn', '04': 'Autumn', '05': 'Autumn',
    '06': 'Winter', '07': 'Winter', '08': 'Winter',
    '09': 'Spring', '10': 'Spring', '11': 'Spring'
}

def read_temperature_data():
    data = []
    for filename in os.listdir(TEMPERATURE_FOLDER):
        if filename.endswith('.csv'):
            with open(os.path.join(TEMPERATURE_FOLDER, filename), 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)
    return data

def calculate_seasonal_averages(data):
    seasonal_data = defaultdict(list)

    for row in data:
        date = row['Date']
        temp = float(row['Temperature'])
        month = date.split('-')[1]
        season = SEASON_MAP.get(month)
        if season:
            seasonal_data[season].append(temp)

    with open(os.path.join(OUTPUT_FOLDER, 'average_temp.txt'), 'w') as file:
        for season in ['Summer', 'Autumn', 'Winter', 'Spring']:
            temps = seasonal_data[season]
            avg_temp = sum(temps) / len(temps) if temps else 0
            file.write(f"{season}: {avg_temp:.2f}°C\n")
            

def find_largest_temp_range(data):
    station_temps = defaultdict(list)

    for row in data:
        station = row['Station']
        temp = float(row['Temperature'])
        station_temps[station].append(temp)

    max_range = -1
    stations_with_max_range = []

    for station, temps in station_temps.items():
        if temps:
            temp_range = max(temps) - min(temps)
            if temp_range > max_range:
                max_range = temp_range
                stations_with_max_range = [station]
            elif temp_range == max_range:
                stations_with_max_range.append(station)

    with open(os.path.join(OUTPUT_FOLDER, 'largest_temp_range_station.txt'), 'w') as file:
        file.write(f"Largest Temperature Range: {max_range:.2f}°C\n")
        for s in stations_with_max_range:
            file.write(f"{s}\n")