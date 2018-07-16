import json
import csv


# converting csv file into json file
def csv_to_json():
    with open('my_csv.csv') as c:
        reader = csv.DictReader(c)
        rows = list(reader)

    with open('my_json.json', 'w') as j:
        json.dump(rows, j, indent=4)


csv_to_json()
