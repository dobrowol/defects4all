import argparse
import configparser

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
    fastTextTrainer = FastTextTrainer(FASTTEXT_DIR, in_dir, klog_size)
    model_file = fastTextTrainer.train()
        for sentence_size in tqdm(range(SENTENCE_MIN_SIZE, SENTENCE_MAX_SIZE)):
            fastTextPredictor = FastTextPreidctor(FASTTEXT_DIR, in_life_dir, klog_size, sentence_size, model_file)
            fastTextPredictor.predict()
        
