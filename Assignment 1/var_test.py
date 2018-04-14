import numpy as np
import pandas as pd
from statsmodels.tsa.api import VAR

if __name__ == '__main__':

    # load paatient data
    data = pd.read_csv(open('./summaries_cleaned/patient_01_summary.csv', 'rb'), index_col=0, parse_dates=True)

    # shift mood and circumplex data
    data.iloc[:, :3] = data.iloc[:, :3].shift(-1)

    # print(data)

    # generate VAR model and print summary
    model = VAR(data[:-1])
    results = model.fit(1)
    print(results.summary())
