from imblearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier

from defects4all.balance_dataframe import balance_series
from sklearn.model_selection import cross_validate
from sklearn.feature_extraction.text import TfidfVectorizer
from defects4all.trainingValidatingSplit import train_test_split_file
from statistics import mean
import argparse
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np
from pathlib import Path

parser = argparse.ArgumentParser(
    description='tool to train Naive Bayes on file ')
parser.add_argument("file", type=str,
    help="file name")
parser.add_argument("experiment_file", type=str,
    help="file name")

args = parser.parse_args()

training_file=args.file

pipeline = Pipeline([('tfidf',TfidfVectorizer()),
        ('clf', XGBClassifier(use_label_encoder=False,nthread=10, max_depth=11, n_estimators=100, learning_rate=0.1))])
scoring = {'acc': 'accuracy',
           'prec': 'precision_macro',
           'rec': 'recall_macro'}
X_train, X_test, y_train, y_test = train_test_split_file(training_file, 0.8)

label_encoder = LabelEncoder()
label_encoder = label_encoder.fit(y_test)
label_encoder = label_encoder.fit(y_train)
np.save(Path(training_file).parents[0]/'label_encoder.sav', label_encoder.classes_)
label_encoded_y = label_encoder.transform(y_train)
X, y = balance_series(X_train, label_encoded_y) 
#scores = cross_validate(pipeline, X, y, scoring=scoring, cv=5, n_jobs=-1, return_estimator=True)
#print("test accuracy", mean(scores['test_acc']))
#print("precision", mean(scores['test_prec']))
#print("recall", mean(scores['test_rec']))
model = pipeline.fit(X, y)
#rfc_fit = scores['estimator']
#model = rfs_fit[0]
import pickle
from pathlib import Path
filename = Path(training_file).parents[0]/'gradient_boost_model.sav'
pickle.dump(model, open(filename, 'wb'))

pred_file = str(Path(args.experiment_file).parents[0])+"/"+str(Path(args.experiment_file).stem)+"_gradient.pred"
pred05_file = str(Path(args.experiment_file).parents[0])+"/"+str(Path(args.experiment_file).stem)+"gradient_05"+".pred"
pred = open(pred_file,"w")
pred05 = open(pred05_file, "w")
best_window_size=110
target_label = label_encoder.transform(["__label__org.apache.hadoop.hdfs.server.blockmanagement.TestReplicationPolicy"])[0]

with open(args.experiment_file) as drained:
    series = drained.read()
    series = series.split(' ')

#predicted = series.rolling(window=window_size).apply(model.predict)
series = series[:-1]
window_size = best_window_size
print ("target label", target_label)
for window_start in range(len(series)-best_window_size):
    prob = (model.predict_proba([" ".join(series[window_start:window_start+window_size])])).max(1).item()
    label = model.predict([" ".join(series[window_start:window_start+window_size])])
    print("predicted labels ", label)
    print("predicted target label ", label[target_label])
    pred.write(str(prob)+", "+str(window_start)+","+str(window_start+window_size)+","+label_encoder.inverse_transform([label])[0]+"\n")
    if prob > 0.5:
        pred05.write(str(prob)+", "+str(window_start)+","+str(window_start+window_size)+","+label_encoder.inverse_transform([label])[0]+"\n")
        print(prob, window_start, window_start+window_size, label_encoder.inverse_transform([label])[0])

pred.close()
pred05.close()
 
