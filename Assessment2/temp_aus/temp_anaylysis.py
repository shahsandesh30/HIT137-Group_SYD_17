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