import os
import argparse

KLOG_SIZE=3
SENTENCE_LEN=10
OVERLAP_SENTENCE=False
OVERLAP_KLOG=True

# parser = argparse.ArgumentParser(
#     description='helper tool to build k-logs from log sequence')
# parser.add_argument("file", type=str,
#     help="normalized log file")
# parser.add_argument("drain_file", type=str,
#     help="drained log file")
# parser.add_argument("prediction_file", type=str,
#     help="file with predictions")
# parser.add_argument("--non_overlap","-n", action='store_true',
#     help="non overlapping sequences")
# parser.add_argument("--klog_size","-k", type=int,
#     help="klog size")
# parser.add_argument("--sentence_length", "-s", type=int,
#     help="klog size")

#args = parser.parse_args()
LOG_FILE = "./results/issue4/1runtime_DEFAULT.log"
DRAIN_FILE = "./results/issue4/1runtime_DEFAULT.drain"
PREDICTIONS_FILE="./results/issue4/predictions"

with open(LOG_FILE, errors='replace') as f:
    log_lines = f.read().splitlines()
with open(PREDICTIONS_FILE, errors='replace') as p:
    predictions_lines = p.read().splitlines()

with open(DRAIN_FILE, errors='replace') as f:
    drain_lines = f.read().splitlines()


if OVERLAP_KLOG :
    logs_per_prediction = SENTENCE_LEN + KLOG_SIZE - 1
else  :
    logs_per_prediction = SENTENCE_LEN * KLOG_SIZE

if OVERLAP_SENTENCE:
    log_step = KLOG_SIZE
else:
    log_step = logs_per_prediction - 1


def similarity_presentation(similarities, log_file=LOG_FILE, drain_file=DRAIN_FILE):
    out_dir = os.path.dirname(log_file)
    out_file = out_dir + "/LCS_prediction_presentation.csv"

    print("writing to file ", out_file)
    with open(out_file, "a") as o_f:

        all_line_idx = 0
        parsed_lines = []
        for line in drain_lines:
            if not line.startswith("None"):
                parsed_lines.append(all_line_idx)
            all_line_idx += 1
        j = 0
        for j in range(len(parsed_lines)):
            if j in similarities:
                for i in range(similarities[j][0][2].size):
                    o_f.write(log_lines[parsed_lines[j+i]]+"\t"+str(similarities[j][0][0])+"\t"+str(similarities[j][0][1])+"\n")
            o_f.write(log_lines[parsed_lines[j]]+"\t \t \n")
            j+=1

