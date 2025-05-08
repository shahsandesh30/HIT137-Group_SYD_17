import os
import csv

# current directory path
current_dir = os.path.dirname(__file__) 
parent_dir = os.path.dirname(current_dir)

# path to temperature data csv files
temperature_data_path = os.path.join(parent_dir, "data_files", "temperature_data")
  
# path to save average temperature reading results
average_temp_path = os.path.join(current_dir, "analysis", "average_temp.txt")  

# defining function to read temperature data
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
                        # initialize new list if the stations is not already in dictionary
                        if station not in station_data:
                            station_data[station] = []
                        station_data[station].append(monthly_temps)

    return station_data


# defining function to calculate seasonal average
def calculate_seasonal_averages(data):
    # defining season for month based on indexing from 0
    seasons = {
        'Summer': [11, 0, 1],   # December, January, February
        'Autumn': [2, 3, 4],    # March, April, May
        'Winter': [5, 6, 7],    # June, July, August
        'Spring': [8, 9, 10]    # September, October, November
    }

    season_totals = {}  # store temperatures per season
    season_counts = {}  # store number of temperature readings per season

    # Loop through data grouped by station or location
    for records in data.values():
        for year in records:
            for season, indices in seasons.items():
                #temperatures for the current season
                temps = [year[i] for i in indices]

                # set totals and counts
                if season not in season_totals:
                    season_totals[season] = 0.0
                    season_counts[season] = 0

                # include temperature values in total
                season_totals[season] += sum(temps)
                season_counts[season] += len(temps)



    # Write average temperature per season to the file
    with open(average_temp_path, 'w') as f:
        for season in seasons:
            if season_counts.get(season, 0) > 0:
                avg = season_totals[season] / season_counts[season]
                f.write(f"average {season} temperature: {avg:.2f}\n")


# station with the largest temperature difference
def find_largest_temp_range(data):
    largest_range = 0  
    station_list = [] 

    for station, records in data.items():
        temps = []  # temps for the station

        # Combine all yearly temperatures into one list
        for year in records:
            temps.extend(year)

        if not temps:
            continue  

        # temp range
        temp_range = max(temps) - min(temps)

        # check temp range diff
        if temp_range > largest_range:
            largest_range = temp_range
            station_list = [station]  
        elif temp_range == largest_range:
            station_list.append(station)  

    # Save the result to a text file
    file_path = os.path.join(current_dir, "analysis", "largest_temp_range_station.txt")
    with open(file_path, 'w') as file:
        for station in station_list:
            file.write(f"station with the largest temperature range: {station}\n")


# Find the warmest and coolest station based on avg temperature
def find_warmest_and_coolest(data):
    station_averages = {}

    for station, records in data.items():
        temps = []

        # Combine all temperatures into one list
        for year in records:
            temps.extend(year)

        if temps:
            avg_temp = sum(temps) / len(temps)
            station_averages[station] = avg_temp

    if not station_averages:
        return  # No valid data

    max_avg = max(station_averages.values())
    min_avg = min(station_averages.values())

    # Write the results to a text file
    file_path = os.path.join(current_dir, "analysis", "warmest_and_coolest_station.txt")
    with open(file_path, 'w') as file:
        file.write("warmest stations are:\n")
        for station, avg in station_averages.items():
            if avg == max_avg:
                file.write(f"{station}\n")

        file.write("\ncoolest stations are:\n")
        for station, avg in station_averages.items():
            if avg == min_avg:
                file.write(f"{station}\n")


def main():
    if not os.path.exists(temperature_data_path):
        print(f"Folder not found: {temperature_data_path}")
        return

    data = read_temperature_data(temperature_data_path)
    if not data:
        print("No valid data found.")
        return

    os.makedirs(os.path.join(current_dir, "analysis"), exist_ok=True)
    calculate_seasonal_averages(data)
    find_largest_temp_range(data)
    find_warmest_and_coolest(data)

if __name__ == "__main__":
    main()
