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

parser = argparse.ArgumentParser(
    description='tool to train Naive Bayes on file ')
parser.add_argument("file", type=str,
    help="file name")
parser.add_argument("--generate_klogs", action='store_true')

args = parser.parse_args()

experiment_file=args.file

pipeline = Pipeline([('tfidf',TfidfVectorizer()),
        ('clf', XGBClassifier(use_label_encoder=False,nthread=10, max_depth=11, n_estimators=100, learning_rate=0.1))])
scoring = {'acc': 'accuracy',
           'prec': 'precision_macro',
           'rec': 'recall_macro'}
X_train, X_test, y_train, y_test = train_test_split_file(experiment_file, 0.8)

label_encoder = LabelEncoder()
label_encoder = label_encoder.fit(y_test)
label_encoder = label_encoder.fit(y_train)
label_encoded_y = label_encoder.transform(y_train)
X, y = balance_series(X_train, label_encoded_y) 
scores = cross_validate(pipeline, X, y, scoring=scoring, cv=5, n_jobs=-1, return_estimator=True)
model = pipeline.fit(X, y)
#rfc_fit = scores['estimator']
#model = rfs_fit[0]
print("test accuracy", mean(scores['test_acc']))
print("precision", mean(scores['test_prec']))
print("recall", mean(scores['test_rec']))
import pickle
filename = 'gradient_boost_model.sav'
pickle.dump(model, open(filename, 'wb'))
