import os
import argparse 
import configparser
from defects4all.Klog import Klog

SENTENCE_OVERLAP = False
KLOG_OVERLAP = True

parser = argparse.ArgumentParser(
    description='helper tool to build k-logs from log sequence')
parser.add_argument("issue", type=str,
    help="issue name")

args = parser.parse_args()

config = configparser.ConfigParser()
config.sections()
config.read('defects4all.ini')
PARSED_LOGS=config['DEFAULT']['PARSED_LOGS_DIR']
KLOGS_DIR=config['DEFAULT']['KLOGS_DIR']
KLOG_MIN_SIZE = int(config['DEFAULT']['KLOG_MIN_SIZE'])
KLOG_MAX_SIZE = int(config['DEFAULT']['KLOG_MAX_SIZE'])
SENTENCE_MIN_SIZE = int(config['DEFAULT']['SENTENCE_MIN_SIZE'])
SENTENCE_MAX_SIZE = int(config['DEFAULT']['SENTENCE_MAX_SIZE'])

in_dir = PARSED_LOGS+"/"+args.issue
in_runtime_dir = PARSED_LOGS+"/"+args.issue+"/runtime"
training = True
out_dir = KLOGS_DIR+"/"+args.issue
out_runtime_dir = KLOGS_DIR+"/"+args.issue+"/runtime"

klog_overlaps = [True, False]
sentence_overlaps = [True, False]

from tqdm import tqdm
train_log_sequence_file=in_dir+"/ut_log_as_sequence.vec"
test_log_sequence_file=in_runtime_dir+"/ut_log_as_sequence.vec"
training_klog = Klog(train_log_sequence_file, out_dir)
testing_klog = Klog(test_log_sequence_file, out_runtime_dir)
for klog_size in tqdm(range(KLOG_MIN_SIZE, KLOG_MAX_SIZE)):
    phase = "training"
    training_klog.klog.prepare_training_klog(phase, klog_size, 0, True, False)

    for sentence_size in tqdm(range(SENTENCE_MIN_SIZE, SENTENCE_MAX_SIZE)):
        testing_klog.prepare_klog_file("testing", klog_size, sentence_size, True, False)
        

