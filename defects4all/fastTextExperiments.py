import subprocess
import argparse
import os
import configparser
from defects4all.utils import get_runtime_file_name_from_klog_file
import glob

def get_runtime_filename(klog_name):
    p = klog_name.split('/')[-1]
    k = p.split('.')[0]
    r = k.split("klog_overlap_sentence_nooverlap_")[1]
    return r

config = configparser.ConfigParser()
config.sections()
config.read('defects4all.ini')
FASTTEXT_DIR=config['DEFAULT']['FASTTEXT_DIR']
KLOGS_DIR=config['DEFAULT']['KLOGS_DIR']

KLOG_MIN_SIZE = int(config['DEFAULT']['KLOG_MIN_SIZE'])
KLOG_MAX_SIZE = int(config['DEFAULT']['KLOG_MAX_SIZE'])
SENTENCE_MIN_SIZE = int(config['DEFAULT']['SENTENCE_MIN_SIZE'])
SENTENCE_MAX_SIZE = int(config['DEFAULT']['SENTENCE_MAX_SIZE'])
SENTENCE_OVERLAP = False
KLOG_OVERLAP = True

parser = argparse.ArgumentParser(
    description='helper tool to build k-logs from log sequence')
parser.add_argument("issue", type=str,
    help="issue name")

args = parser.parse_args()


in_dir = KLOGS_DIR+"/"+args.issue
in_life_dir = KLOGS_DIR+"/"+args.issue+"/life"
kos = ["klog_overlap", "klog_nooverlap"]
sos = ["sentence_overlap", "sentence_nooverlap"]
from tqdm import tqdm
for klog_size in tqdm(range(KLOG_MIN_SIZE, KLOG_MAX_SIZE)):
    specific_train_in_dir = in_dir +"/klog"+str(klog_size)
    filename = "/klog_overlap_sentence_nooverlap.klog"
    model_file = "/klog_model"
    subprocess.call("%s/fasttext supervised -input %s -output %s" %(FASTTEXT_DIR, specific_train_in_dir+filename, specific_train_in_dir+model_file), shell=True)
    for sentence_size in tqdm(range(SENTENCE_MIN_SIZE, SENTENCE_MAX_SIZE)):
        file_pattern = "/klog_overlap_sentence_nooverlap*.klog"
        specific_in_life_dir = in_life_dir +"/klog"+str(klog_size)+"/sentence"+str(sentence_size)
        for klog_name in glob.glob(specific_in_life_dir+file_pattern):
            print("predicting on ", klog_name)
            runtime_name = get_runtime_filename(klog_name)
            predictions_file = "/predictions_%s.pred"%(runtime_name)
            print("writing to ", predictions_file)
            subprocess.call("%s/fasttext predict %s %s > %s" %(FASTTEXT_DIR, specific_train_in_dir+model_file+".bin", klog_name, specific_in_life_dir+predictions_file), shell=True)
