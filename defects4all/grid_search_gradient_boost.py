import argparse
import imblearn
import configparser
from defects4all.trainingValidatingSplit import train_test_split_file
from defects4all.Klog import Klog
from defects4all.FastTextTrainer import FastTextTrainer
from defects4all.FastTextValidator import FastTextValidator
import pandas as pd

config = configparser.ConfigParser()
config.sections()
config.read('defects4all.ini')
FASTTEXT_DIR=config['DEFAULT']['FASTTEXT_DIR']
KLOGS_DIR=config['DEFAULT']['KLOGS_DIR']
PARSED_LOGS=config['DEFAULT']['PARSED_LOGS_DIR']
RESULT_DIR=config['DEFAULT']['RESULT_DIR']

KLOG_MIN_SIZE = int(config['DEFAULT']['KLOG_MIN_SIZE'])
KLOG_MAX_SIZE = int(config['DEFAULT']['KLOG_MAX_SIZE'])
SENTENCE_MIN_SIZE = int(config['DEFAULT']['SENTENCE_MIN_SIZE'])
SENTENCE_MAX_SIZE = int(config['DEFAULT']['SENTENCE_MAX_SIZE'])
SENTENCE_OVERLAP = config['DEFAULT']['SENTENCE_OVERLAP'] == "True"
KLOG_OVERLAP = config['DEFAULT']['KLOG_OVERLAP'] == "True"
TRAINING_SENTENCE = config['DEFAULT']['TRAINING_SENTENCE'] == "True"
TESTING_SENTENCE = config['DEFAULT']['TESTING_SENTENCE'] == "True"

parser = argparse.ArgumentParser(
    description='helper tool to build k-logs from log sequence')
parser.add_argument("issue", type=str,
    help="issue name")
parser.add_argument("--generate_klogs", action='store_true')

args = parser.parse_args()

klogs_dir = KLOGS_DIR+"/"+args.issue
klogs_runtime_dir = KLOGS_DIR+"/"+args.issue+"/runtime"
kos = ["klog_overlap", "klog_nooverlap"]
sos = ["sentence_overlap", "sentence_nooverlap"]

from tqdm import tqdm
parsed_dir = PARSED_LOGS+"/"+args.issue
parsed_runtime_dir = PARSED_LOGS+"/"+args.issue+"/runtime"
train_log_sequence_file=parsed_dir+"/sequence/ut_log_as_sentence.vec"
test_log_sequence_file=parsed_runtime_dir+"/sequence/ut_log_as_sentence.vec"
training_klog = Klog(train_log_sequence_file, klogs_dir)
gradient_experiment = {}
if not args.generate_klogs:
    from defects4all.getKlogsFromDirectory import getKlogsFromDirectory
    gradient_experiment = getKlogsFromDirectory("./klogs")
else:

    print("preparing klogs...")

    for klog_size in tqdm(range(KLOG_MIN_SIZE, KLOG_MAX_SIZE+1,10)):
        phase = "training"
        if not TRAINING_SENTENCE:
            gradient_experiment[klog_size] = training_klog.prepare_klog_file(phase, klog_size, 0, KLOG_OVERLAP, SENTENCE_OVERLAP)
        else:
            for sentence_size in tqdm(range(SENTENCE_MIN_SIZE, SENTENCE_MAX_SIZE+1,10)):
                gradient_experiment[klog_size, sentence_size] = training_klog.prepare_klog_file(phase, klog_size, sentence_size, KLOG_OVERLAP, SENTENCE_OVERLAP)
paramTfIdf = { 
    'classifier__n_estimators': [100, 150],
    'classifier__max_features': ['auto', 'sqrt', 'log2'],
    'classifier__max_depth' : [11, 15],
    'classifier__learning_rate' :[0.1]
} 
paramCount = { 
    'count__ngram_range':[(2,2), (3,3), (4,4)],
    'classifier__n_estimators': [100, 150],
    'classifier__max_features': ['auto', 'sqrt', 'log2'],
    'classifier__max_depth' : [11, 15],
    'classifier__learning_rate' :[0.1]
}

from imblearn.over_sampling import RandomOverSampler
from imblearn.pipeline import Pipeline
from imblearn.under_sampling import RandomUnderSampler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import GradientBoostingClassifier
pipelinetfIdf = Pipeline([
    ('tfidf', TfidfVectorizer()),
#    ("os", RandomOverSampler(sampling_strategy=oversampling_strategy)),
#    ("us", RandomUnderSampler(sampling_strategy=undersampling_strategy)),
    ('classifier', GradientBoostingClassifier())])
pipelineNGrams = Pipeline([
    ('count', CountVectorizer()),
#    ("os", RandomOverSampler(sampling_strategy=oversampling_strategy)),
#    ("us", RandomUnderSampler(sampling_strategy=undersampling_strategy)),
    ('classifier', GradientBoostingClassifier())])

from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from defects4all.balance_dataframe import balance_series
 
for key in gradient_experiment:
    print("key ", gradient_experiment[key])
    for experiment_file in gradient_experiment[key]:
        X_train, X_test, y_train, y_test = train_test_split_file(experiment_file, 0.8)
        X_train_bal, y_train_bal = balance_series(X_train, y_train) 
        from sklearn.model_selection import GridSearchCV
        #gs = GridSearchCV(gb, param, cv=5, n_jobs=-1)
        #cv_fit = gs.fit(X_train_vect, y_train.values.ravel())
        #print(pd.DataFrame(cv_fit.cv_results_).sort_values('mean_test_score', ascending=False)[['mean_test_score', 'mean_fit_time', 'param_learning_rate', 'param_max_depth', 'param_n_estimators']][0:5])
        gs = GridSearchCV(pipelinetfIdf, paramTfIdf, n_jobs=-1)
        cv_fit = gs.fit(X_train_bal, y_train_bal)
        print(pd.DataFrame(cv_fit.cv_results_).sort_values('mean_test_score', ascending=False)[['mean_test_score', 'mean_fit_time', 'param_classifier__n_estimators',
'param_classifier__max_features', 'param_classifier__max_depth', 'param_classifier__learning_rate']][0:5])
        gs = GridSearchCV(pipelineNGrams, paramCount, n_jobs=-1)
        cv_fit = gs.fit(X_train_bal, y_train_bal)
        #cv_fit = gs.fit(X_train, y_train.values.ravel())
        print(pd.DataFrame(cv_fit.cv_results_).sort_values('mean_test_score', ascending=False)[['mean_test_score', 'mean_fit_time', 'param_count__ngram_range', 'param_classifier__n_estimators',
'param_classifier__max_features', 'param_classifier__max_depth', 'param_classifier__learning_rate']][0:5])
