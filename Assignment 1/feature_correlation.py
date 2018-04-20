import pandas as pd
import numpy as np

if __name__ == '__main__':
    
    feature_ranks = []
    for i in range(1, 34):
        try:
            data = pd.read_csv('./patient_data/p{:02d}.csv'.format(i), index_col=0,parse_dates=True)
        except:
            continue

        correlations = pd.DataFrame([], columns=['corr', 'abs_corr'])
        for col in data.columns[2:]:
            corr = data['next_mood'].corr(data[col])
            correlations.loc[col] = [corr, abs(corr)] 
            
        #feature_ranks[i] = list(correlations.sort_values(by=[ 'abs_corr'],
                                       #             arrscending=False)[:11].index)
        patient_features = [i, 'mood'] + list(correlations.sort_values(by=[ 'abs_corr'], ascending=False)[:11].index)

        feature_ranks.append(patient_features)

   # feature_ranks = np.array(feature_ranks)
    fr = pd.DataFrame(feature_ranks)
    
    print(fr)
    #np.savetxt('./patient_data/Best_F_Corr.csv', feature_ranks, delimiter=',', fmt='%s')
    fr.to_csv('./patient_data/Best_F_Corr.csv')
