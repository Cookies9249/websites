import csv
import json

def csv_to_json(csv_file_path, json_file_path):
    # Open the CSV file and read its contents
    with open(csv_file_path, 'r') as csv_file:
        csv_data = csv.reader(csv_file)

        # Convert the CSV data to a list of dictionaries
        data_list = []
        for i, row in enumerate(csv_data):
            if i > 0:
                name = row[1]
                lat = float(row[5])
                lon = float(row[6])
                data_list.append({"Name": name, "Lat": lat, "Long": lon})

    # Write the JSON data to the output file
    with open(json_file_path, 'w') as json_file:
        json.dump(data_list, json_file, indent=4)
