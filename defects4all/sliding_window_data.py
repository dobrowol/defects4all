from defects4all.Klog import Klog
from defects4all.config_utils import get_param
import argparse
import imblearn

PARSED_LOGS = get_param("PARSED_LOGS_DIR")
KLOGS_DIR = get_param("KLOGS_DIR")
parser = argparse.ArgumentParser(
    description='helper tool to build k-logs from log sequence')
parser.add_argument("issue", type=str,
    help="issue name")
parser.add_argument("window_size", type=str,
    help="sloding window size")

args = parser.parse_args()

klogs_dir = KLOGS_DIR+"/"+args.issue

from tqdm import tqdm
parsed_dir = PARSED_LOGS+"/"+args.issue
train_log_sequence_file=parsed_dir+"/sequence/ut_log_as_sentence.vec"
training_klog = Klog(train_log_sequence_file, klogs_dir)
training_klog.prepare_klog_file("training", 1, int(args.window_size), False, True)
