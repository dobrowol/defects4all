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

from tqdm import tqdm
for klog_size in tqdm(range(KLOG_MIN_SIZE, KLOG_MAX_SIZE)):
    train = True
    klog = Klog(klog_size, True)
    specific_out_dir = out_dir +"/klog"+str(klog_size)
    os.makedirs(specific_out_dir, exist_ok=True)
    klog.prepare_klog_file(train, train_log_sequence_file, specific_out_dir)

    for sentence_size in tqdm(range(SENTENCE_MIN_SIZE, SENTENCE_MAX_SIZE)):
        specific_out_life_dir = out_life_dir +"/klog"+str(klog_size)+"/sentence"+str(sentence_size)
        os.makedirs(specific_out_life_dir, exist_ok=True)
        klog2 = Klog(klog_size, True, sentence_size, False)
        train = False
        klog2.prepare_klog_file(train, test_log_sequence_file, specific_out_life_dir)
        

