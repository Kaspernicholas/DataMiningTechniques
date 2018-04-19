import pickle as pkl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

VARIABLES = ['mood', 'circumplex.arousal', 'circumplex.valence', 'activity', 'screen', 'call', 'sms', 'appCat.builtin', 'appCat.communication', 'appCat.entertainment', 'appCat.finance', 'appCat.game', 'appCat.office',	'appCat.other', 'appCat.social', 'appCat.travel', 'appCat.unknown', 'appCat.utilities', 'appCat.weather']


'''
Generates a day-by-day summary of each patient and saves the results
'''
if __name__ == '__main__':
    # import data
    data = pd.read_csv(open('./dataset_mood_smartphone.csv', 'rb'))
    print('Data Imported...\n')


    for i in range(1, 34):
        # load a patient's data
        patient_name = 'AS14.{:02}'.format(i)
        patient_data = data.loc[data['id'] == patient_name]

        if len(patient_data) == 0:
            print('Could not find patient {}'.format(patient_name))
            continue

        # set the time as the index
        patient_data['time'] = pd.to_datetime(patient_data['time'])
        patient_data.index = patient_data['time']
        del patient_data['time']
        patient_data = patient_data.sort_index()

        # print(patient_data)

        # for each variable, create a resampled time series
        day_series = []
        for j, var in enumerate(VARIABLES):
            patient_variable = patient_data.loc[patient_data['variable'] == var]
            if j < 4:
                pv = patient_variable['value'].resample('D').mean()
            else:
                pv = patient_variable['value'].resample('D').sum()
            # pv.rename(index=str, columns={'value': var})
            day_series.append(pv.copy())

        # combine into new DataFrame
        patient_summary = pd.concat(day_series, axis=1)
        patient_summary.columns = VARIABLES

        # --- Filling in missing data
        # finds longest run of days where there can be at most a break of 2
        # days of missing data, which is filled in by linear interpolation

        a = patient_summary.mood.values
        mask_print = ''
        for j,b in enumerate(np.isnan(a)):
            if b:
                mask_print += '_'
            else:
                mask_print += '#'
        
        print("p{:02d}| {}".format(i, mask_print))
        
        m = np.invert(np.isnan(a))
        block = []
        blocks = []
        c = 0
        for j in range(len(a)):
            if m[j]:
                c = 0
                block.append(j)
            else:
                c += 1

            if c >= 2:
                blocks.append(block)
                block = []

        blocks.append(block)

        maxi = 0
        for b in blocks:
            if len(b) > maxi:
                indicies = b
                maxi = len(b)
        
        patient_summary = patient_summary[indicies[0]:indicies[-1]+1]
        patient_summary['mood'] = patient_summary['mood'].interpolate()

        # save this summary
        patient_summary.to_csv('./summaries_cleaned/patient_{:02}_summary.csv'.format(i),
            na_rep='0')
        #print('Saved patient {} summary'.format(patient_name))
        
        
