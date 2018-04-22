import math
import pandas as pd
import numpy as np
from statsmodels.tsa.api import VAR

'''
Runs the VAR model with given parameters
    - k: the lag to use
    - n: number of features to select (includes mood)
    - test: True if final testing of model, False if just validatin
    - fs: feature selection scheme, either 'Corrs' or 'MSE'
'''

def run_var(k=1, n=1, test=True, fs='Corrs'):
    mses = []
    if fs == 'MSE':
        features_all = pd.read_csv('./patient_data/Best_F_MSE', index_col=0)
    else:
        features_all = pd.read_csv('./patient_data/Best_F_Corr.csv', index_col=0)

    for i in range(1, 34):
    
        # load patient data
        try:
            data = pd.read_csv(open('./patient_data/p{:02d}.csv'.format(i),'rb'), index_col=0, parse_dates=True)
        except:
            continue

        #print('\n --- Patient {:02d} ---'.format(i))
        
        # Feature selection
        features = list(features_all.loc[i])[0:n] 
        p_data = data[['next_mood']+features]

        # split into training, validation and testing set
        seg = [0.7, 0.1, 0.2]
        t = len(p_data)
        splits = [math.floor(seg[0]*t), math.floor((seg[0]+seg[1])*t)]
        
        # --- Run Model Here on p_data ---

        squared_error = []

        # Train on trainset + parts of validation set
        if test:
            start, stop = splits[1], len(p_data)
        else:
            start, stop = splits[0], splits[1]

        for t in range(start, stop):
            # find first order differences over all points
            diff = p_data.iloc[:t, 1:].diff().iloc[1:]
            model = VAR(diff)
            results = model.fit(k)
            yhat_diff = results.forecast(diff.values, 1)[0][0]
            yhat = p_data.iloc[t, 1] + yhat_diff
            obs = p_data.iloc[t, 0]
            #print('Predicted: {:.2f}, Observed: {:.2f}'.format(yhat, obs))
            #print(yhat)
            squared_error.append((obs - yhat)**2)
        
        mse = np.mean(squared_error)
        #print('\nMSE: {}'.format(mse))
        mses.append(mse)

    s = np.std(mses, ddof=1)
    mean = np.mean(mses)
    lb = mean - 2.06*s / math.sqrt(27)
    ub = mean + 2.06*s / math.sqrt(27)
    print('\n\nVAR model (k={}, n={}) results:'.format(k, n))
    print('Mean: {:.4f}, std: {:.4f}, CI: ({:.4f}, {:.4f}))'.format(mean, s,
                                                                    lb, ub))
    
    return mean 

if __name__ == '__main__':
    results = np.zeros([4, 7])   # referenced k, n

    for k in range(1, 5):
        for n in range(2, 9):
            results[k-1, n-2] = run_var(k, n, test=False, fs='MSE')
    print(results)
    print('Lowest MSE: {}'.format(np.min(results)))
    #run_var(2, 2, test=True, fs='Corrs') 
