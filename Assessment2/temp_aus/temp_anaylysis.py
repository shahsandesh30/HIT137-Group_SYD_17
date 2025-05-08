import os
import csv

current_dir = os.path.dirname(__file__) # current directory path
parent_dir = os.path.dirname(current_dir)

# Folder where temperature CSV files are stored
temperature_data_path = os.path.join(parent_dir, "data_files", "temperature_data")
    

# to read the temperature data from CSV files
import os
import csv

def read_temperature_data(folder_path):
    
    """
    Reads temperature data from all CSV files in the given folder.
    
    Each file is expected to have columns for 'STATION_NAME' and each month from January to December.
    Returns a dictionary where keys are station names and values are lists of 12-element lists,
    each containing monthly temperatures for one row (year) of data.
    """
    station_data = {}

    # make list of all the files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        station = row.get('STATION_NAME', '').strip()
                        
                        if not station:
                            continue  # skip the rows if there is no valid station available

                        months = [
                            'January', 'February', 'March', 'April', 'May', 'June',
                            'July', 'August', 'September', 'October', 'November', 'December'
                        ]

                        try:
                            # skip if any value is not available or not valid
                            monthly_temps = [float(row[month]) for month in months if row[month].strip()]
                        except (ValueError, KeyError):
                            continue  # Skip this row if it can not do the conversion

                        if len(monthly_temps) == 12:
                            # Initialize station list if not already present
                            if station not in station_data:
                                station_data[station] = []
                            station_data[station].append(monthly_temps)
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")

    return station_data


# to calculate seasonal averages and write to a file
def calculate_seasonal_averages(data):
    seasons = {
        'Summer': [11, 0, 1],
        'Autumn': [2, 3, 4],
        'Winter': [5, 6, 7],
        'Spring': [8, 9, 10]
    }
    season_totals = {}
    season_counts = {}

    for records in data.values():
        for year in records:
            for season, indices in seasons.items():
                temps = [year[i] for i in indices]

                # Initialize if not already in dictionary
                if season not in season_totals:
                    season_totals[season] = 0.0
                    season_counts[season] = 0

                season_totals[season] += sum(temps)
                season_counts[season] += len(temps)

    average_temp_path = os.path.join(current_dir, "analysis", "average_temp.txt")

    with open(average_temp_path, 'w') as f:
        for season in seasons:
            if season in season_counts and season_counts[season] > 0:
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
