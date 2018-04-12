import pickle
import re
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt

# Import structured_data.pckl file
with (open('structured_data.pckl', 'rb')) as f:
    data = pickle.load(f)

# List with all variable names
variables = [
    'screen',
    'mood',
    'circumplex.arousal',
    'circumplex.valence',
    'activity',
    'call',
    'sms',
    'appCat.builtin',
    'appCat.communication',
    'appCat.entertainment',
    'appCat.finance',
    'appCat.game',
    'appCat.office',
    'appCat.other',
    'appCat.social',
    'appCat.travel',
    'appCat.unknown',
    'appCat.utilities',
    'appCat.weather'
]


def get_date(line):
    date = datetime.strptime(re.sub('\ .*', '', line[0]), "%Y-%m-%d")
    return date


def get_specific_data(id, variable):
    specific_data = []
    for line in range(0, len(data[id])):
        if data[id][line][1] == variable:
            specific_data.append(data[id][line])
    return specific_data


def total_time(variable_data, date):
    tot_time = 0
    for line in variable_data:

        if get_date(line) == date:
            if line[2] == 'NA':
                print(line)
                continue
            else:
                tot_time += float(line[2])
    return tot_time / 3600


def total_number(variable_data, date):
    tot_number = 0
    for line in variable_data:
        if get_date(line) == date:
            tot_number += float(line[2])
    return tot_number


def average_value(variable_data, date):
    tot_number = []
    for line in variable_data:
        if get_date(line) == date:
            if line[2] == 'NA':
                continue
            else:
                tot_number.append(float(line[2]))

    if tot_number == []:
        return 0
    else:
        return np.average(tot_number)


def generate_table(id):

    index_j = 0

    for variable in variables:

        print(variable)
        index_i = 0

        variable_specific_data = get_specific_data(id, variable)

        if variable == 'screen':
            dates = []
            date = ''
            for line in variable_specific_data:
                if get_date(line) != date:
                    date = get_date(line)
                    dates.append(date)
            patient_table = np.zeros((len(dates), len(variables)))

        for date in dates:
            if variable in ['mood', 'circumplex.arousal', 'circumplex.valence', 'activity']:
                patient_table[index_i, index_j] = average_value(variable_specific_data, date)
            elif variable in ['call', 'sms']:
                patient_table[index_i, index_j] = total_number(variable_specific_data, date)
            elif variable in ['screen', 'appCat.builtin', 'appCat.communication', 'appCat.entertainment', \
                              'appCat.finance', 'appCat.game', 'appCat.office', 'appCat.other', 'appCat.social', \
                              'appCat.travel', 'appCat.unknown', 'appCat.utilities', 'appCat.weather']:
                patient_table[index_i, index_j] = total_time(variable_specific_data, date)
            index_i += 1

        index_j += 1

    return patient_table, dates



##########################################################################
#                                                                        #
#   PASS TO GENERATE_TABLE(ID) THE ID OF THE PATIENT YOU WANT TO CHECK   #
#                                                                        #
##########################################################################
ID = 1
table, date_array = generate_table(ID)

date_formatted = []
for date in date_array:
    month = date.month
    day = date.day
    date_formatted.append(('%s.%s' % (month, day)))


good_table = np.zeros((len(date_array), len(variables)+1))
good_table[:, 0] = date_formatted
good_table[:, 1:] = table

header = ['date'] + variables
print(header)

np.savetxt('table_%d.csv' % ID, good_table, delimiter=';')