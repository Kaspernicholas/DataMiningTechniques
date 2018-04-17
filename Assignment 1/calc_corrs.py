import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    corrs = []

    for i in range(1, 34):
        # load cleaned csv
        try:
            data = pd.read_csv(open('./summaries_cleaned/patient_{}_summary.csv'.format(i),  'rb'), index_col=0, parse_dates=True)
        except:
            continue
        
        data['curr_mood'] = data['mood']
        # shift mood and circumplex data points up 1
        data[['mood', 'circumplex.arousal', 'circumplex.valence']] = data[['mood', 'circumplex.arousal', 'circumplex.valence']].shift(-1)

        corrs.append(np.nan_to_num(data.corr().as_matrix(columns=['mood'])))
    
    summary = sum(corrs)/19
    summary = summary.flatten()

    print(summary)
    for i, corr in enumerate(summary):
        print('{}: {}'.format(data.columns[i], corr)) 

    plt.bar(data.columns, summary)
    plt.show()


