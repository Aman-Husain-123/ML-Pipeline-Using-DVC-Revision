import numpy as np
import pandas as pd
import pickle
import json

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    roc_auc_score
)

from sklearn.preprocessing import LabelEncoder

clf = pickle.load(open('model.pkl', 'rb'))
test_data = pd.read_csv('./data/features/test_bow.csv')

X_test = test_data.iloc[:, 0:-1].values
y_test = test_data.iloc[:, -1].values

y_pred = clf.predict(X_test)
y_pred_proba = clf.predict_proba(X_test)[:, 1]

le = LabelEncoder()
y_test_encoded = le.fit_transform(y_test)

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    average='weighted'
)

recall = recall_score(
    y_test,
    y_pred,
    average='weighted'
)

auc = roc_auc_score(y_test_encoded, y_pred_proba)

metrics_dict = {
    'accuracy': accuracy,
    'precision': precision,
    'recall': recall,
    'auc': auc
}

with open('./data/metrics.json', 'w') as file:
    json.dump(metrics_dict, file, indent=4)