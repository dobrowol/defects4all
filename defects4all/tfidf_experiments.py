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
#
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

for key in tfidf_experiment:
    print("key ", tfidf_experiment[key])
    for experiment_file in tfidf_experiment[key]:
        X_train, X_test, y_train, y_test = train_test_split_file(experiment_file, 0.8)
        tfidf_vect = TfidfVectorizer()
        tfidf_vect.fit(X_train)
        X_train_vect = tfidf_vect.transform(X_train)
        X_test_vect = tfidf_vect.transform(X_test)
        from sklearn.ensemble import RandomForestClassifier

        rf = RandomForestClassifier()
        rf_model = rf.fit(X_train_vect, y_train.values.ravel()) 

        y_pred = rf_model.predict(X_test_vect)
        from sklearn.metrics import precision_score, recall_score

        precision = precision_score(y_test, y_pred, average='weighted', zero_division=1)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=1)
        print('Precision: {} / Recall: {} / Accuracy: {}'.format(
            round(precision, 3), round(recall, 3), round((y_pred==y_test).sum()/len(y_pred), 3)))
