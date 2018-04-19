import pandas as pd
import numpy as np
from scipy import stats


VARIABLES = ['mood', 'circumplex.arousal', 'circumplex.valence', 'activity', 'screen', 'call', 'sms', 'appCat.builtin', 'appCat.communication', 'appCat.entertainment', 'appCat.finance', 'appCat.game', 'appCat.office',	'appCat.other', 'appCat.social', 'appCat.travel', 'appCat.unknown', 'appCat.utilities', 'appCat.weather']

'''
Calculate the t-test between next_mood and each attribute
'''
if __name__ == '__main__':
    for i in range(1, 34):
         
        # import patient data
        try:
            with open('./summaries_cleaned/patient_{:02d}_summary.csv'.format(i), 'rb') as f:
                data = pd.read_csv(f, index_col=0, parse_dates=True)
            f.close()
        except:
            continue


        next_mood = data['mood'].copy().shift(-1)
        next_mood.rename('next_mood', inplace=True)
        
        # clean sparse columns
        # 1 identify columns with less than 25% data points

        data['appCat.other'] = data[['appCat.other', 'appCat.unknown']]
        data.drop(columns=['appCat.unknown'], inplace=True)

        density = data.astype(bool).sum(axis=0) / 45

        threshold = 0.25
        sparse = density.loc[density < threshold]
        # add the sparse sets to appCat.other

        data['appCat.other'] =  data.loc[:, ['appCat.other']+list(sparse.index)].sum(axis=1)

        # remove the sparse columns

        data.drop(columns=sparse.index, inplace=True)
        
        print('Removed from patient {}'.format(i))
        print(sparse.index)
        
        k = 1
        data = data.rolling(k).mean()

        data = pd.concat([next_mood, data], axis=1)
        data.rename(columns={0: 'next_mood'}, inplace=True)
        data = data.iloc[k-1:-1, :]

        # save the processed data
        data.to_csv('./patient_data/p{:02d}.csv'.format(i))

