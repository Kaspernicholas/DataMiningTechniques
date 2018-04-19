import numpy as np
import pandas as pd

if __name__ == '__main__':
    data = pd.read_csv('./patient_data/p05.csv', index_col=0, parse_dates=True)
    
    correlations = pd.DataFrame([], columns=['corr', 'abs_corr'])
    for col in data.columns[1:]:
        corr = data['next_mood'].corr(data[col])
        correlations.loc[col] = [corr, abs(corr)] 
        
    print(correlations.sort_values(by=['abs_corr'], ascending=False))
