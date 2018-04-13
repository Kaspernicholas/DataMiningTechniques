import pandas as pd
import numpy as np

if __name__ == '__main__':
    corrs = []

    for i in range(1, 34):
        # load cleaned csv
        try:
            data = pd.read_csv(open('./summaries_cleaned/patient_{}_summary.csv'.format(i), 'rb'))
        except:
            continue

        # shift mood and circumplex data points up 1
        data[['mood', 'circumplex.arousal', 'circumplex.valence']] = data[['mood', 'circumplex.arousal', 'circumplex.valence']].shift(-1)

        corrs.append(np.nan_to_num(data.corr().as_matrix(columns=['mood'])))

    print(sum(corrs)/19)
