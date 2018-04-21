import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller

VARIABLES = ['mood', 'circumplex.arousal', 'circumplex.valence', 'activity', 'screen', 'call', 'sms', 'appCat.builtin', 'appCat.communication', 'appCat.entertainment', 'appCat.finance', 'appCat.game', 'appCat.office',	'appCat.other', 'appCat.social', 'appCat.travel', 'appCat.unknown', 'appCat.utilities', 'appCat.weather']

if __name__ == '__main__':
    
    p_values = pd.DataFrame([], index=VARIABLES)

    for i in range(1, 34):
        # load patient data and calculate stationarity p_values for each
        # attribute

        try:
            data = pd.read_csv('./summaries_cleaned/patient_{:02d}_summary.csv'.format(i), index_col=0,
                               parse_dates=True)
        except:
            continue
        
        print('Patient {}'.format(i))

        for v in VARIABLES:
            x = data[v].values
            result = adfuller(x)
            p_values.loc[v, i] = result[1]

    print(p_values.mean(axis=1))