import pickle
from datetime import datetime
import re
from matplotlib import pyplot as plt


# Import structured_data.pckl file
with (open('structured_data.pckl', 'rb')) as f:
    patient_data = pickle.load(f)


# Select only the specific data lines from the patient_data file
screen_per_patient = []
mood_per_patient = []
for i in range(0, 27):
    screen_data = []
    mood_data = []
    for j in range(0, len(patient_data[i])):
        if patient_data[i][j][1] == 'screen':
            screen_data.append(patient_data[i][j])
        if patient_data[i][j][1] == 'mood':
            mood_data.append(patient_data[i][j])
    screen_per_patient.append(screen_data)
    mood_per_patient.append(mood_data)


# This function returns an array with total screen time per day. Indices of the array indicate which day.
def screen_per_day(id):
    date = ''
    tot_time = 0
    screen_per_day = []
    screen_data = screen_per_patient[id]
    for i in range(0, len(screen_data)):
        if datetime.strptime(re.sub('\ .*', '', screen_data[i][0]), "%Y-%m-%d") == date:
            tot_time += float(screen_data[i][2])

        else:
            date = datetime.strptime(re.sub('\ .*', '', screen_data[i][0]), "%Y-%m-%d")
            screen_per_day.append(tot_time / 3600)
            tot_time = float(screen_data[i][2])

    return screen_per_day[1:]


# This function returns an array with average mood per day. Indices of the array indicate which day.
def mood_per_day(id):
    tot_mood = []
    mood_per_day = []
    mood_data = mood_per_patient[id]
    date = datetime.strptime(re.sub('\ .*', '', mood_data[0][0]), "%Y-%m-%d")
    for i in range(0, len(mood_data)):
        if datetime.strptime(re.sub('\ .*', '', mood_data[i][0]), "%Y-%m-%d") == date:
            tot_mood.append(float(mood_data[i][2]))

        else:
            date = datetime.strptime(re.sub('\ .*', '', mood_data[i][0]), "%Y-%m-%d")
            mood_per_day.append(sum(tot_mood) / len(tot_mood))
            tot_mood = []
            tot_mood.append(float(mood_data[i][2]))

    return mood_per_day


# Plot total screen time and average mood as a function of date.
for id in range(0, 27):

    screen_array = screen_per_day(id)
    plt.plot(range(1, len(screen_array)+1), screen_array)
    plt.xlabel('Date')
    plt.ylabel('Total Screen Time [Hr]')
    plt.show()

    mood_array = mood_per_day(id)
    plt.plot(range(1, len(mood_array)+1), mood_array)
    plt.xlabel('Date')
    plt.ylabel('Average Mood')
    plt.ylim(0, 10)
    plt.show()



