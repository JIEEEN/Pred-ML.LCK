from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import xgboost as xgb

def predict(path):
    all_data = pd.read_csv(path)
    label = all_data['team1_win']
    X = all_data.drop('team1_win', axis=1)
    
    label = label.astype(int)
    
    encoder = LabelEncoder()
    
    for col in X.columns:
        X[col] = encoder.fit_transform(X[col])
        
    X_train, X_test, y_train, y_test = train_test_split(X, label, test_size=0.2)
    
    model = xgb.XGBClassifier()
    
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    print(accuracy_score(y_test, y_pred))
    
    
if __name__ == "__main__":
    path = '../csv/lck_data.csv'
    predict(path)