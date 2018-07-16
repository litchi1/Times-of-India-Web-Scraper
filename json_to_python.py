''' Guideline for preprocessing of data.
READ CAREFULLY THE ENTIRE PROGRAM BEFORE PROCEEDING.
Comment out the part which you do not need. '''


import json

with open('my_json.json') as f:
    data = json.load(f)


# printing the entire json file
print(data)


# printing single uid; change only the first index of data[] to get its respective "UID"
'''Similarly "DATE", "TITLE" & "ARTICLE_LINK" can be found out'''
print(data[0]["UID"])


# printing all the uids
for line in data:
    print(line["UID"])


# printing all the dates
for line in data:
    print(line["DATE"])


'''Similarly all the "TITLE" and "ARTICLE_LINK" can be found out'''


# printing each dictionary with respective keyword and its value from the list
for line in data:
    print(line["UID"])
    print(line["DATE"])
    print(line["TITLE"])
    print(line["ARTICLE_LINK"])

