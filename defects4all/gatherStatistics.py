import argparse
import configparser
from defects4all.trainingValidatingSplit import splitToTrainingAndValidatingSet
from defects4all.Klog import Klog
from defects4all.FastTextTrainer import FastTextTrainer
from defects4all.FastTextValidator import FastTextValidator

config = configparser.ConfigParser()
config.sections()
config.read('defects4all.ini')
FASTTEXT_DIR=config['DEFAULT']['FASTTEXT_DIR']
KLOGS_DIR=config['DEFAULT']['KLOGS_DIR']
PARSED_LOGS=config['DEFAULT']['PARSED_LOGS_DIR']

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
testing_klog = Klog(test_log_sequence_file, klogs_runtime_dir)

fasttext_experiment = {}
print("preparing klogs...")
#for klog_size in tqdm(range(KLOG_MIN_SIZE, KLOG_MAX_SIZE+1,10)):
#for klog_size in tqdm(range(KLOG_MIN_SIZE, KLOG_MIN_SIZE+1)):
#    phase = "training"
#    if not TRAINING_SENTENCE:
#        fasttext_experiment[klog_size] = training_klog.prepare_klog_file(phase, klog_size, 0, KLOG_OVERLAP, SENTENCE_OVERLAP)
#    else:
#        for sentence_size in tqdm(range(SENTENCE_MIN_SIZE, SENTENCE_MAX_SIZE+1,10)):
        #for sentence_size in tqdm(range(SENTENCE_MIN_SIZE, SENTENCE_MIN_SIZE+1)):
#            fasttext_experiment[klog_size, sentence_size] = training_klog.prepare_klog_file(phase, klog_size, sentence_size, KLOG_OVERLAP, SENTENCE_OVERLAP)

    #for sentence_size in tqdm(range(SENTENCE_MIN_SIZE, SENTENCE_MAX_SIZE)):
    #    testing_klog.prepare_klog_file("testing", klog_size, sentence_size, KLOG_OVERLAP, SENTENCE_OVERLAP)
 
#print("only uniqe data...")
#from defects4all.unique_klogs import remove_duplicated_lines
#remove_duplicated_lines("./klogs")
#from defects4all.data_statistics import describe_words
from defects4all.data_statistics import describe_sentence
#describe_words("./klogs", "./stats")
describe_sentence("./klogs", "./stats")
