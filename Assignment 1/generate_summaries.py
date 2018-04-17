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

    corrs = []

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

        # remove rows of data without mood data
        # (have to find longest series of real valued NaNs)

        a = patient_summary.mood.values
        m = np.concatenate(([True], np.isnan(a), [True]))
        ss = np.flatnonzero(m[1:] != m[:-1]).reshape(-1, 2)
        start, stop = ss[(ss[:, 1] - ss[:, 0]).argmax()]

        # shift mood and circumplex up one
        # patient_summary[['mood', 'circumplex.arousal', 'circumplex.valence']] = patient_summary[['mood', 'circumplex.arousal', 'circumplex.valence']].shift(-1)

        # corrs.append(patient_summary[start:stop-1].corr()['mood'])

        save this summary
        patient_summary[start:stop].to_csv('./summaries_cleaned/patient_{:02}_summary.csv'.format(i), na_rep='0')
        print('Saved patient {} summary'.format(patient_name))
    # print(corrs)
