import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller

VARIABLES = ['mood', 'circumplex.arousal', 'circumplex.valence', 'activity', 'screen', 'call', 'sms', 'appCat.builtin', 'appCat.communication', 'appCat.entertainment', 'appCat.finance', 'appCat.game', 'appCat.office',	'appCat.other', 'appCat.social', 'appCat.travel', 'appCat.unknown', 'appCat.utilities', 'appCat.weather']

if __name__ == '__main__':
    
    p_values = pd.DataFrame([], index=VARIABLES)
    p_values_diff = pd.DataFrame([], index=VARIABLES)

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

            x_diff = data[v].diff()[1:].values
            result = adfuller(x_diff)
            p_values_diff.loc[v, i] = result[1]
        
    # calculate the mean and std for each variable
    for v in VARIABLES:
            vals = p_values.loc[v].values
            mean = np.nanmean(vals)
            std = np.nanstd(vals, ddof=1)

            vals_diff = p_values_diff.loc[v].values
            mean_diff = np.nanmean(vals_diff)
            std_diff = np.nanstd(vals_diff, ddof=1)
            ci_diff = 2.06*std / np.sqrt(len(vals))
            print('{} & {:.4f} ({:.4f}) & {:.4f} ({:.4f})  \\\\'.format(v,
                                                                        mean,
                                                                        std,
                                                                        mean_diff,
                                                                        std_diff)) 
