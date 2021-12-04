import os
import argparse
import configparser

KLOG_SIZE=3
SENTENCE_LEN=10
OVERLAP_SENTENCE=False
OVERLAP_KLOG=True

# parser = argparse.ArgumentParser(
#     description='helper tool to build k-logs from log sequence')
# parser.add_argument("issue", type=str,
#     help="issue to be presented")
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
LOG_FILE = "/runtime_DEFAULT.log"
DRAIN_FILE = "/runtime_DEFAULT.drain"
OUT_FILE="/LCS_prediction_presentation_"
config = configparser.ConfigParser()
config.sections()
config.read('defects4all.ini')
PARSED_LOGS=config['DEFAULT']['PARSED_LOGS_DIR']
RESULT=config['DEFAULT']['RESULT_DIR']
if PARSED_LOGS is None:
    print ("Wrong configuration PARSED_LOGS_DIR not set!!!")
    exit()
if RESULT is None:
    print ("Wrong configuration RESULT_DIR not set!!!")
    exit()


def similarity_presentation(issue, sequence_id, similarities):
    log_file = PARSED_LOGS+"/"+issue+"/runtime/"+sequence_id+".log"
    drain_file = PARSED_LOGS+"/"+issue+"/runtime/"+sequence_id+".drain"
    out_dir = RESULT+"/"+issue
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    out_file = out_dir + OUT_FILE+sequence_id + ".csv"

    with open(log_file, errors='replace') as f:
        log_lines = f.read().splitlines()
    with open(drain_file, errors='replace') as f:
        drain_lines = f.read().splitlines()
    print("writing to file ", out_file)
    with open(out_file, "a") as o_f:

        all_line_idx = 0
        parsed_lines = []
        for line in drain_lines:
            if not line.startswith("None"):
                parsed_lines.append(all_line_idx)
            all_line_idx += 1
        j = 0
        from tqdm import tqdm
        for j in tqdm(range(len(log_lines))):
            if j in parsed_lines:
                if j in similarities:
                    for i in range(j, similarities[j][1]):
                        o_f.write(log_lines[j+i]+"\t"+str(similarities[j][0])+"\t"+str(similarities[j][1]-j)+"\n")
                else:
                    o_f.write(log_lines[j] + "\t \t \n")
            else:
                o_f.write(log_lines[j]+"\t \t \n")
            j+=1
        #for j in range(len(parsed_lines)):
        #    if j in similarities:
        #        for i in range(similarities[j][0][2].size):
        #            o_f.write(log_lines[parsed_lines[j+i]]+"\t"+str(similarities[j][0][0])+"\t"+str(similarities[j][0][1])+"\n")
        #    o_f.write(log_lines[parsed_lines[j]]+"\t \t \n")
        #    j+=1

