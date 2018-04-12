import pickle as pkl
import pandas as pd
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

        # save this summary
        patient_summary.to_csv('./summaries/patient_{:02}_summary.csv'.format(i))
        print('Saved patient {} summary'.format(patient_name))

        # patient_summary.plot(subplots=True)
        # plt.show()
        # print(patient_summary)
