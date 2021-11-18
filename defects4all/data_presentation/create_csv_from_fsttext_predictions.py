import os
import argparse 

KLOG_SIZE=3
SENTENCE_LEN=10
OVERLAP_SENTENCE=False
OVERLAP_KLOG=True


parser = argparse.ArgumentParser(
    description='helper tool to build k-logs from log sequence')
parser.add_argument("file", type=str,
    help="normalized log file")
parser.add_argument("drain_file", type=str,
    help="drained log file")
parser.add_argument("prediction_file", type=str,
    help="file with predictions")
parser.add_argument("--non_overlap","-n", action='store_true',
    help="non overlapping sequences")
parser.add_argument("--klog_size","-k", type=int,
    help="klog size")
parser.add_argument("--sentence_length", "-s", type=int,
    help="klog size")

args = parser.parse_args()

with open(args.file, errors='replace') as f:
    log_lines = f.read().splitlines()
with open(args.prediction_file, errors='replace') as p:
    predictions_lines = p.read().splitlines()

with open(args.drain_file, errors='replace') as f:
    drain_lines = f.read().splitlines()

out_dir = os.path.dirname(args.file)
out_file = out_dir + "/prediction_presentation.csv"

if OVERLAP_KLOG :
    logs_per_prediction = SENTENCE_LEN + KLOG_SIZE - 1
else  :
    logs_per_prediction = SENTENCE_LEN * KLOG_SIZE 

if OVERLAP_SENTENCE:
    log_step = KLOG_SIZE
else:
    log_step = logs_per_prediction
    
print("writing to file ", out_file)
with open(out_file, "a") as o_f:
    i = 0
    while j < len(drain_lines):
    for j in range(len(drain_lines)):
        if not j.startswith("None"):
            o_f.write(log_lines[j]+"\t"+prediction_lines[i%logs_per_prediction])
            i += 1
        else:
            o_f.write(log_lines[j]+"\n")
        

