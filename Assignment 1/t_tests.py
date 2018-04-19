from scipy.stats import ttest_ind
import pandas as pd
import numpy as np

if __name__ == '__main__':
    data = pd.read_csv('./patient_data/p01.csv', index_col=0, parse_dates=True)

    print(data)
    print(
