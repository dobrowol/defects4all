import os
import argparse 
import defects4all.createFastTextTrainSet
import configparser
from defects4all.Klog import Klog

KLOG_MIN_SIZE = 3
KLOG_MAX_SIZE = 6
SENTENCE_MIN_SIZE = 5
SENTENCE_MAX_SIZE = 15
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
KLOGS_DIR=config['DEFAULT']['KLOGS_LOGS_DIR']
if PARSED_LOGS is None:
    print ("Wrong configuration PARSED_LOGS_DIR not set!!!")
    exit() 
in_dir = PARSED_LOGS+"/"+args.issue
in_life_dir = PARSED_LOGS+"/"+args.issue+"/life"
training = True
out_dir = KLOGS_DIR+"/"+args.issue
out_life_dir = KLOGS_DIR+"/"+args.issue+"/life"

klog_overlaps = [True, False]
sentence_overlaps = [True, False]

train_log_sequence_file = createFastTextTrainSet.create_fasttext_sequence_representation(in_dir)
test_log_sequence_file = createFastTextTrainSet.create_fasttext_sequence_representation(in_life_dir)
for klog_size in range(KLOG_MIN_SIZE, KLOG_MAX_SIZE):
    for sentence_size in range(SENTENCE_MIN_SIZE, SENTENCE_MAX_SIZE):
        specific_out_dir = out_dir +"/klog"+str(klog_size)+"/sentence"+str(sentence_size)
        os.makedirs(specific_out_dir, exist_ok=True)
        specific_out_life_dir = out_life_dir +"/klog"+str(klog_size)+"/sentence"+str(sentence_size)
        os.makedirs(specific_out_life_dir, exist_ok=True)
        for ko in klog_overlaps:
            for so in sentence_overlaps:
                train = True
                klog = Klog(klog_size, ko, sentence_size, so)
                klog_train_file = klog.prepare_klog_file(train, train_log_sequence_file, specific_out_dir)
        
                train = False
                klog_test_file = klog.prepare_klog_file(train, test_log_sequence_file, specific_out_life_dir)
        

