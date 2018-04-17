import math
import sys
import pandas as pd
from pandas.tools.plotting import autocorrelation_plot
import numpy as np
from statsmodels.tsa.api import VAR
from statsmodels.tsa.arima_model import ARIMA

from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
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
         
        k = 1
        p_data = pd.concat([p_data, data.iloc[:, :5].rolling(k).mean()], axis=1)
        p_data.rename(columns={p_data.columns[0]: 'next_mood'}, inplace=True)
        p_data['next_mood'] = p_data['next_mood'].shift(-1)
        
        p_data = p_data[k-1:-1]
        

        # split into training, validation and testing set
        seg = [0.7, 0.1, 0.2]
        t = len(p_data)
        splits = [math.floor(seg[0]*t), math.floor((seg[0]+seg[1])*t)]
        
        # split into training, validation and testing set
        train = p_data[:splits[0]]
        train2 = p_data[:splits[1]]   # includes validation data
        validate = p_data[splits[0]:splits[1]]
        test = p_data[splits[1]:]
        
        train_x, train_y = train.iloc[:, 1:], train['next_mood']
        train2_x, train2_y = train2.iloc[:, 1:], train2['next_mood']
        validate_x, validate_y = validate.iloc[:, 1:], validate['next_mood']
        test_x, test_y = test.iloc[:, 1:], test['next_mood']

        # --- Run Model Here on p_data --- 

        # train the ARIMA model for benchmark test

        #autocorrelation_plot(train['next_mood']) 
        #plt.show()
        #model = ARIMA(train['next_mood'], order=(2, 1, 0))
        #model_fit = model.fit(disp=0)

        #print(model_fit.summary())

        #residuals = pd.DataFrame(model_fit.resid)
        #residuals.plot()
        #plt.show()
        #residuals.plot(kind='kde')
        #plt.show()
        
        history = [x for x in train2['next_mood']]
        predictions = [history[-1]]
        squared_error = []
        for t in range(len(test)):
            model = ARIMA(history, order=(3, 1, 0))
            try:
                model_fit = model.fit(disp=0)
                output=model_fit.forecast()
                yhat = output[0][0]
            except:
                # sometimes LinAlg Error, reuse last prediction...
                yhat = predictions[-1]
            predictions.append(yhat)
            obs = test_y[t]
            history.append(obs)
            print('Predicted = {:.2f}, expected = {:.2f}'.format(yhat, obs))
            squared_error.append((obs - yhat)**2)

        mse = np.mean(squared_error) 
        mses.append(mse)

    print('\n\nAvg. MSE (all patients): {}'.format(np.mean(mses)))

    # --- Plotting the predictions

    #print('\nMSE: {:.4f}'.format(mse))
    #plt.plot(p_data['next_mood'], label='Observed')
    ##plt.plot(test['next_mood'].values, label='Observed')
    #plt.plot(test.index.values, predictions, label='Prediction')
    #plt.show()

    ## train a simple Neural Network on this set:
    #input_dim = len(p_data.columns[1:])
    #hidden_dim = 8
    #model = Sequential()
    #model.add(Dense(hidden_dim, input_dim=input_dim, activation='tanh'))
    #model.add(Dense(hidden_dim, activation='tanh'))
    #model.add(Dense(1, activation='sigmoid'))

    #model.compile(loss='mean_squared_error', optimizer='sgd') 

    #X = train.iloc[:, 1:].as_matrix()
    ## normalise data
    #X[:, 0] /= 10

    #Y = train['next_mood'].as_matrix()/10
    #print(X)
    #print(Y)
    ##model.fit(X, Y, epochs=800, batch_size=3, verbose=0)

    ##scores = model.evaluate(X, Y)
    ##print("\n{}: {:.2f}percent".format(model.metrics_names[1], scores[1]*100))

    ## test on the testing set
    #predictions = model.predict(X)
    #print(predictions)
    ##predictions = model.predict(test.iloc[:, 2:].as_matrix())
    ##print(test.iloc[:, 2:].as_matrix())
    #for i in range(len(predictions)):
    #    print('Guessed: {}, Actual: {}'.format(predictions[i]*10, Y[i]*10))

    ##print(model.summary())
    ##print(model.get_weights())

    






