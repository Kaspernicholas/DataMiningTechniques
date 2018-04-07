import csv
from collections import defaultdict
import pickle


# Import data set from .csv file
columns = defaultdict(list)  # each value in each column is appended to a list
with open('dataset_mood_smartphone.csv', encoding='utf-8') as f:  # open desired file
    reader = csv.DictReader(f, delimiter=',')  # read rows into a dictionary format
    for row in reader:  # read a row as {column1: value1, column2: value2,...}
        for (k, v) in row.items():  # go over each column name and value
            columns[k].append(v)  # append the value into the appropriate list  based on column name k


# Make separate lists for columns of csv and clear some memory
ids, timestamps, variables, values = columns['id'], columns['time'], columns['variable'], columns['value']
del columns['id'], columns['time'], columns['variable'], columns['value']


# Structure data per patient
patient_data = []
for i in range(1, 34):

    # Make patient id
    if i < 10:
        id = 'AS14.0%d' % i
    else:
        id = 'AS14.%d' % i

    # Check for all instances of the patient id in the data set and save corresponding information
    sub_data = []
    for j in range(0, len(ids)):
        if ids[j] == '%s' %id:
            sub_data.append([timestamps[j], variables[j], values[j]])

    if sub_data != []:
        patient_data.append(sub_data)
    else:
        print('Patient id %s is not present in data set.' % id)


# Save the structured data object as a .pckl file so we can use it in another script.
f = open('structured_data.pckl', 'wb')
pickle.dump(patient_data, f)
f.close()

