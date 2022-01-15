import argparse
import imblearn
import configparser
from defects4all.trainingValidatingSplit import train_test_split_file
from defects4all.Klog import Klog
from defects4all.FastTextTrainer import FastTextTrainer
from defects4all.FastTextValidator import FastTextValidator
import pandas as pd
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler

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

from defects4all.oversampler import get_sampling_strategy as oversampler_strategy
from defects4all.undersampler import get_sampling_strategy as undersampler_strategy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
paramTfIdf = { 
    'classifier__n_estimators': [10, 100, 150, 500],
    'classifier__max_features': ['auto', 'sqrt', 'log2'],
    'classifier__max_depth' : [30, 60, 90, None],
    'classifier__criterion' :['gini', 'entropy']
} 
paramCount = { 
    'count__ngram_range':[(2,2), (3,3), (4,4)],
    'classifier__n_estimators': [10, 100, 150, 500],
    'classifier__max_features': ['auto', 'sqrt', 'log2'],
    'classifier__max_depth' : [30, 60, 90, None],
    'classifier__criterion' :['gini', 'entropy']
}

from sklearn.feature_extraction.text import CountVectorizer
from imblearn.pipeline import Pipeline
import numpy as np
from defects4all.data_statistics import describe_samples

for key in gradient_experiment:
    print("key ", gradient_experiment[key])
    for experiment_file in gradient_experiment[key]:
        X_train, X_test, y_train, y_test = train_test_split_file(experiment_file, 0.8)
        data_stats = describe_samples (pd.DataFrame({"klogs_words":X_train, "test_suite":y_train}))
        oversample_to = int((10*data_stats.max())//100)
        undersample_to = int((50*data_stats.max())//100)
        oversampling_strategy=oversampler_strategy(pd.DataFrame({"klogs_words":X_train, "test_suite":y_train}), oversample_to)
        undersampling_strategy=undersampler_strategy(pd.DataFrame({"klogs_words":X_train, "test_suite":y_train}), undersample_to)
        X_train_res, y_train_res = RandomOverSampler(sampling_strategy=oversampling_strategy).fit_resample(X_train.values.reshape(-1, 1), y_train)
        X_train_bal, y_train_bal = RandomUnderSampler(sampling_strategy=undersampling_strategy).fit_resample(X_train_res, y_train_res)
        pipelinetfIdf = Pipeline([
            ('tfidf', TfidfVectorizer()),
        #    ("os", RandomOverSampler(sampling_strategy=oversampling_strategy)),
        #    ("us", RandomUnderSampler(sampling_strategy=undersampling_strategy)),
            ('classifier', RandomForestClassifier())])
        pipelineNGrams = Pipeline([
            ('count', CountVectorizer()),
        #    ("os", RandomOverSampler(sampling_strategy=oversampling_strategy)),
        #    ("us", RandomUnderSampler(sampling_strategy=undersampling_strategy)),
            ('classifier', RandomForestClassifier())])

        X_train_bal = np.reshape(X_train_bal, -1)
        gs = GridSearchCV(pipelinetfIdf, paramTfIdf, n_jobs=-1)
        cv_fit = gs.fit(X_train_bal, y_train_bal)
        print(pd.DataFrame(cv_fit.cv_results_).sort_values('mean_test_score', ascending=False)[['mean_test_score', 'mean_fit_time', 'param_classifier__n_estimators', 'param_classifier__max_features',
'param_classifier__max_depth', 'param_classifier__criterion']][0:5])
        gs = GridSearchCV(pipelineNGrams, paramCount, n_jobs=-1)
        cv_fit = gs.fit(X_train_bal, y_train_bal)
        #cv_fit = gs.fit(X_train, y_train.values.ravel())
        print(pd.DataFrame(cv_fit.cv_results_).sort_values('mean_test_score', ascending=False)[['mean_test_score', 'mean_fit_time', 'param_count__ngram_range', 'param_classifier__n_estimators',
'param_classifier__max_features', 'param_classifier__max_depth', 'param_classifier__criterion']][0:5])
