import math
import sys
import pandas as pd
#from pandas.tools.plotting import autocorrelation_plot
import numpy as np
from statsmodels.tsa.api import VAR
#from statsmodels.tsa.arima_model import ARIMA

#from sklearn.cross_validation import train_test_split
#from sklearn.tree import DecisionTreeClassifier
#from sklearn.metrics import accuracy_score
#from sklearn import tree
#import graphviz
#from keras.models import Sequential
#from keras.layers import Dense
import matplotlib.pyplot as plt 

'''
Takes the mean of the last k time-steps for attributes:
    - mood
    - arousal
    - valence
    - activity
    - screen
Creates a training, validation and test set
'''

def categorise(x):
    '''Rounds a number to nearest 0.5, then multiplies by 10 to get a category
       value'''
    return int(round(x*2)*5)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        patient_num = int(sys.argv[1])
    else:
        patient_num = 1

    mses = []

    for i in range(1, 34):
    
        # load patient data
        try:
            data = pd.read_csv(open('./summaries_cleaned/patient_{:02d}_summary.csv'.format(i),'rb'), index_col=0, parse_dates=True)
        except:
            continue

        print('\n --- Patient {:02d} ---'.format(i))

        p_data = data['mood']
        p_data.rename(columns={'mood': 'next_mood'}, inplace=True)
        
        #p_data = pd.concat([p_data, data.iloc[:, :5].rolling(k).mean()], axis=1)
        p_data = pd.concat([p_data, data[['mood',
                                          'circumplex.arousal',
                                          'circumplex.valence',
                                          'activity',
                                          'screen',
                                          'call',
                                          'sms']]], axis=1)
        
        p_data.rename(columns={p_data.columns[0]: 'next_mood'}, inplace=True)

        p_data['next_mood'] = p_data['next_mood'].shift(-1)

        p_data = p_data[:-1]   # remove final NaN caused by shifting
        
        #print(p_data)

        # split into training, validation and testing set
        seg = [0.7, 0.1, 0.2]
        t = len(p_data)
        splits = [math.floor(seg[0]*t), math.floor((seg[0]+seg[1])*t)]
        
        train = p_data[:splits[0]]
        train2 = p_data[:splits[1]]   # includes validation data
        validate = p_data[splits[0]:splits[1]]
        test = p_data[splits[1]:]
        
        train_x, train_y = train.iloc[:, 1:], train['next_mood']
        train2_x, train2_y = train2.iloc[:, 1:], train2['next_mood']
        validate_x, validate_y = validate.iloc[:, 1:], validate['next_mood']
        test_x, test_y = test.iloc[:, 1:], test['next_mood']

        # --- Run Model Here on p_data ---

        squared_error = []

        # Train on trainset + parts of validation set
        for t in range(len(train), len(train2)):
            #print(p_data.iloc[t-1:t, 1:])
            model = VAR(train2.iloc[:t, :])
            results = model.fit(4)
            yhat = results.forecast(train2.iloc[:t, :].values, 1)[0][0]
            obs = p_data['next_mood'][t]
    
            print('Predicted: {:.2f}, Observed: {:.2f}'.format(yhat, obs))
            squared_error.append((obs - yhat)**2)
        
        mse = np.mean(squared_error)
        print('\nMSE: {}'.format(mse))
        mses.append(mse)

''''
            # VAR MODEL
            squared_error = []

            for t in range(splits[1], len(p_data)):
                #print(p_data.iloc[t-1:t, 1:])
                model = VAR(p_data.iloc[:t, 1:])
                #print(model.select_order(5))
                results = model.fit(2)
                yhat = results.forecast(p_data.iloc[:t, 1:].values, 1)[0][0]
                obs = p_data['next_mood'][t]

                print('Predicted: {:.2f}, Observed: {:.2f}'.format(yhat, obs))
                squared_error.append((obs - yhat)**2)

            mse = np.mean(squared_error)
            print('\nMSE: {}'.format(mse))
            mses.append(mse)
        

'''
print('\n\nAvg. MSE (all patients): {}'.format(np.mean(mses)))


    






