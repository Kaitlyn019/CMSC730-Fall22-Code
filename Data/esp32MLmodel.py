import pickle
import pandas as pd
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

features = pd.read_csv("test.csv")

test_size = 0.33
seed = 7

X = features.values[:, 1:-1]
Y = features.values[:, -1]

X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y, test_size=test_size, random_state=seed)

model = LogisticRegression()
model.fit(X_train, Y_train)

filename = 'finalized_model_LR.sav'
pickle.dump(model, open(filename, 'wb'))

predictions = model.predict(X_test)
print("Accuracy of LR:",metrics.accuracy_score(X_test, Y_test))


#################

forest = RandomForestClassifier(n_estimators=100, random_state=100)
forest.fit(X_train,Y_train)
predictions = forest.predict(X_test)

print("Accuracy of RF:", metrics.accuracy_score(Y_test, predictions))
