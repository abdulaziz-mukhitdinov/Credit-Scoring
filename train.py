import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score

data = pd.read_csv('/Users/abdulaziz/Desktop/credit_scoring/data/scoring.csv')
X = data.drop(columns=["default"]).values
y = data["default"].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression(class_weight="balanced")
model.fit(X_train, y_train)

joblib.dump(model, 'model.pkl')