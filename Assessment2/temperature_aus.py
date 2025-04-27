import os
import csv

# Australian temperature seasons
seasons = {
    'Summer': ['December', 'January', 'February'],
    'Autumn': ['March', 'April', 'May'],
    'Winter': ['June', 'July', 'August'],
    'Spring': ['September', 'October', 'November']
}

folder_path = 'data_files/temperature_data'

# Read each CSV file 
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        with open(os.path.join(folder_path, filename), 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                print(row)
         
