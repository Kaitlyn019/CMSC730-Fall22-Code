import pickle
import pandas as pd
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression

features = pd.read_csv("test.csv")

test_size = 0.33
seed = 7

X = features.values[:, 1:-1]
Y = features.values[:, -1]

X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y, test_size=test_size, random_state=seed)

model = LogisticRegression()
model.fit(X_train, Y_train)

filename = 'finalized_model.sav'
pickle.dump(model, open(filename, 'wb'))