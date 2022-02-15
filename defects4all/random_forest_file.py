from imblearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

from defects4all.balance_dataframe import balance_series
from sklearn.model_selection import cross_validate
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from defects4all.trainingValidatingSplit import train_test_split_file
from statistics import mean
import argparse
from pathlib import Path
parser = argparse.ArgumentParser(
    description='tool to train Naive Bayes on file ')
parser.add_argument("file", type=str,
    help="file name")
parser.add_argument("--generate_klogs", action='store_true')

args = parser.parse_args()

experiment_file=args.file

pipeline = Pipeline([('tfidf',CountVectorizer(analyzer='word', ngram_range=(2,2))),
        ('clf',RandomForestClassifier(max_depth=None, n_estimators=100, criterion='gini', max_features='log2'))])
scoring = {'acc': 'accuracy',
           'prec': 'precision_macro',
           'rec': 'recall_macro'}
X_train, X_test, y_train, y_test = train_test_split_file(experiment_file, 0.8)
X, y = balance_series(X_train, y_train) 
scores = cross_validate(pipeline, X, y, scoring=scoring, cv=5, n_jobs=-1, return_estimator=True)
model = pipeline.fit(X, y)
#y_pred = model.predict(X_test)
#from sklearn.metrics import precision_score, recall_score
#precision = precision_score(y_test, y_pred, average='micro')
#recall = recall_score(y_test, y_pred, average='micro')
#print('Precision: {} / Recall: {} / Accuracy: {}'.format(
#    round(precision, 3), round(recall, 3), round((y_pred==y_test).sum()/len(y_pred), 3)))
print("test accuracy", mean(scores['test_acc']))
print("precision", mean(scores['test_prec']))
print("recall", mean(scores['test_rec']))
import pickle
from pathlib import Path
#
filename = Path(experiment_file).parents[0]/'random_forest_model.sav'
pickle.dump(model, open(filename, 'wb'))
