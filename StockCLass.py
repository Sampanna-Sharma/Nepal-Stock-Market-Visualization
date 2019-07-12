import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR

class StockPredictor():
    def __init__(self,x_train,kernel='rbf', C=1e3, gamma=0.1):
        self.predictor = SVR(kernel=kernel, C=C, gamma=gamma)
        self.scaler = StandardScaler()
        self.scaler.fit(x_train.values)
        self.stdev = None
        
        
    def train(self,x,y):
        x_n = self.scaler.transform(x.values)
        x_n = pd.DataFrame(x_n, index=x.index, columns=x.columns)
        self.predictor.fit(x_n,y)
        self.stdev = np.sqrt(sum((self.predictor.predict(x_n) - y)**2) / (len(y) - 2))   
        
    def predict(self,X,critical_value):
        x_n = self.scaler.transform(X.values)
        x_n = pd.DataFrame(x_n, index=X.index, columns=X.columns)
        yhat = self.predictor.predict(x_n)
        higher, lower = yhat + critical_value * self.stdev, yhat - critical_value * self.stdev
        return higher, lower

