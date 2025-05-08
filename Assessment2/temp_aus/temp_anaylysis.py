import os
import csv

current_dir = os.path.dirname(__file__) # current directory path
parent_dir = os.path.dirname(current_dir)

# Folder where temperature CSV files are stored
temperature_data_path = os.path.join(parent_dir, "data_files", "temperature_data")
    

# to read the temperature data from CSV files
def read_temperature_data(folder_path):
    station_data = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    station = row['STATION_NAME']
                    monthly_temps = [float(row[month]) for month in [
                        'January', 'February', 'March', 'April', 'May', 'June',
                        'July', 'August', 'September', 'October', 'November', 'December'
                    ] if row[month]]
                    
                    if len(monthly_temps) == 12:
                        # Initialize the list if the station is not already in the dictionary
                        if station not in station_data:
                            station_data[station] = []
                        station_data[station].append(monthly_temps)

    return station_data


import os

# Function to calculate seasonal average temperatures and write to a file
def calculate_seasonal_averages(data):
    # Define which months belong to each season (using 0-based indexing)
    seasons = {
        'Summer': [11, 0, 1],   # December, January, February
        'Autumn': [2, 3, 4],    # March, April, May
        'Winter': [5, 6, 7],    # June, July, August
        'Spring': [8, 9, 10]    # September, October, November
    }

    season_totals = {}  # To store total temperatures per season
    season_counts = {}  # To store number of temperature readings per season

    # Loop through all data (grouped by station or location)
    for records in data.values():
        for year in records:
            for season, indices in seasons.items():
                # Get the temperature values for the current season
                temps = [year[i] for i in indices]

                # Initialize totals and counts if not already set
                if season not in season_totals:
                    season_totals[season] = 0.0
                    season_counts[season] = 0

                # Add temperature values to the totals
                season_totals[season] += sum(temps)
                season_counts[season] += len(temps)

    # Define path to save the average temperature file
    average_temp_path = os.path.join(current_dir, "analysis", "average_temp.txt")

    # Write average temperature per season to the file
    with open(average_temp_path, 'w') as f:
        for season in seasons:
            if season_counts.get(season, 0) > 0:
                avg = season_totals[season] / season_counts[season]
                f.write(f"{season}: {avg:.2f}\n")

# to find the station with the largest temperature range
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

    largest_temp_range_station_path = os.path.join(current_dir, "analysis", "largest_temp_range_station.txt")
    with open(largest_temp_range_station_path, 'w') as f:
        for station in stations:
            f.write(f"{station}\n")


# to find the warmest and coolest station
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

    warmest_and_coolest_station_path = os.path.join(current_dir, "analysis", "warmest_and_coolest_station.txt")
    with open(warmest_and_coolest_station_path, 'w') as f:
        f.write("Warmest Station(s):\n")
        for station, avg in averages.items():
            if avg == max_avg:
                f.write(f"{station}\n")
        f.write("\nCoolest Station(s):\n")
        for station, avg in averages.items():
            if avg == min_avg:
                f.write(f"{station}\n")


def main():
    if not os.path.exists(temperature_data_path):
        print(f"Folder not found: {temperature_data_path}")
        return

    data = read_temperature_data(temperature_data_path)
    if not data:
        print("No valid data found.")
        return

    os.makedirs("./analysis", exist_ok=True)
    calculate_seasonal_averages(data)
    find_largest_temp_range(data)
    find_warmest_and_coolest(data)

if __name__ == "__main__":
    main()
