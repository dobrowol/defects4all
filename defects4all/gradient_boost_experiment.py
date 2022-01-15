import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import argparse
import imblearn
import configparser
from defects4all.trainingValidatingSplit import train_test_split_file
from defects4all.Klog import Klog
from defects4all.FastTextTrainer import FastTextTrainer
from defects4all.FastTextValidator import FastTextValidator

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

tfidf_experiment = {}
if not args.generate_klogs:
    from defects4all.getKlogsFromDirectory import getKlogsFromDirectory
    tfidf_experiment = getKlogsFromDirectory("./klogs")
else:

    print("preparing klogs...")

    for klog_size in tqdm(range(KLOG_MIN_SIZE, KLOG_MAX_SIZE+1,10)):
        phase = "training"
        if not TRAINING_SENTENCE:
            tfidf_experiment[klog_size] = training_klog.prepare_klog_file(phase, klog_size, 0, KLOG_OVERLAP, SENTENCE_OVERLAP)
        else:
            for sentence_size in tqdm(range(SENTENCE_MIN_SIZE, SENTENCE_MAX_SIZE+1,10)):
                tfidf_experiment[klog_size, sentence_size] = training_klog.prepare_klog_file(phase, klog_size, sentence_size, KLOG_OVERLAP, SENTENCE_OVERLAP)
from imblearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier

from defects4all.balance_dataframe import balance_series
from sklearn.model_selection import cross_validate
from sklearn.feature_extraction.text import TfidfVectorizer

pipeline = Pipeline([('tfidf',TfidfVectorizer()),
        ('clf',GradientBoostingClassifier(max_depth=11, n_estimators=100, learning_rate=0.1, max_features='auto'))])
scoring = {'acc': 'accuracy',
           'prec': 'precision_macro',
           'rec': 'recall_macro'}
from statistics import mean
for key in tfidf_experiment:
    print("key ", tfidf_experiment[key])
    for experiment_file in tfidf_experiment[key]:
        X_train, X_test, y_train, y_test = train_test_split_file(experiment_file, 0.8)
        X, y = balance_series(X_train, y_train) 
        scores = cross_validate(pipeline, X, y, scoring=scoring, cv=5, n_jobs=-1)
        print("test accuracy", mean(scores['test_acc']))
        print("precision", mean(scores['test_prec']))
        print("recall", mean(scores['test_rec']))
