import os
import argparse 
import glob
from defects4all.utils import get_runtime_file_name_from_klog_file
import configparser

def get_runtime_filename(klog_name):
    p = klog_name.split('/')[-1]
    k = p.split('.')[0]
    r = k.split("predictions_")[1]
    return r

KLOG_SIZE=3
SENTENCE_LEN=10
OVERLAP_SENTENCE=False
OVERLAP_KLOG=True

parser = argparse.ArgumentParser(
    description='helper tool to build k-logs from log sequence')
parser.add_argument("issue", type=str,
    help="issue name")

config = configparser.ConfigParser()
config.sections()
config.read('defects4all.ini')
PARSED_LOGS=config['DEFAULT']['PARSED_LOGS_DIR']
KLOGS_DIR=config['DEFAULT']['KLOGS_DIR']
KLOG_MIN_SIZE = int(config['DEFAULT']['KLOG_MIN_SIZE'])
KLOG_MAX_SIZE = int(config['DEFAULT']['KLOG_MAX_SIZE'])
SENTENCE_MIN_SIZE = int(config['DEFAULT']['SENTENCE_MIN_SIZE'])
SENTENCE_MAX_SIZE = int(config['DEFAULT']['SENTENCE_MAX_SIZE'])

args = parser.parse_args()

in_klogs_dir = KLOGS_DIR+"/"+args.issue
in_klogs_runtime_dir = KLOGS_DIR+"/"+args.issue+"/runtime"
in_log_dir = PARSED_LOGS+"/"+args.issue
in_log_runtime_dir = PARSED_LOGS+"/"+args.issue+"/runtime"

for klog_size in range(KLOG_MIN_SIZE, KLOG_MAX_SIZE):
    for sentence_size in range(SENTENCE_MIN_SIZE, SENTENCE_MAX_SIZE):
        print(in_klogs_runtime_dir +"/klog"+str(klog_size)+"/sentence"+str(sentence_size))
        ind_dir = in_klogs_runtime_dir +"/klog"+str(klog_size)+"/sentence"+str(sentence_size)
        for prediction_file in glob.glob(ind_dir+"/*.pred"):
            print(prediction_file)
            runtime_name = get_runtime_filename(prediction_file)
            print(in_log_runtime_dir+"/%s.drain"%(runtime_name))
            runtime_drain_file = glob.glob(in_log_runtime_dir+"/%s.drain"%(runtime_name))[0]
            runtime_log_file = glob.glob(in_log_runtime_dir+"/%s.log"%(runtime_name))[0]

            with open(runtime_log_file, errors='replace') as f:
                log_lines = f.read().splitlines()
            with open(prediction_file, errors='replace') as p:
                predictions_lines = p.read().splitlines()

            with open(runtime_drain_file, errors='replace') as f:
                drain_lines = f.read().splitlines()

            out_dir = ind_dir 
            out_file = out_dir + "/prediction_presentation_%s.csv"%(runtime_name)
            
            logs_per_prediction = SENTENCE_LEN * KLOG_SIZE 

            log_step = logs_per_prediction
    
            print("writing to file ", out_file)
            with open(out_file, "a") as o_f:
                i = 0
                while i < len(drain_lines):
                    for j in range(len(drain_lines)):
                        if not drain_lines[j].startswith("None"):
                            o_f.write(log_lines[j]+"\t"+predictions_lines[i%logs_per_prediction])
                            i += 1
                        else:
                            o_f.write(log_lines[j]+"\n")
        

