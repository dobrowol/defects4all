from defects4all.createFastTextTrainSet import create_fasttext_sequence_representation
import configparser
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(
    description='defects4All helper tool to drain parsed logs to clusters sequence applicable for forstText.')
parser.add_argument("issue", type=str,
    help="issue name")

args = parser.parse_args()
issue = args.issue

config = configparser.ConfigParser()
config.sections()
config.read('defects4all.ini')
LEVEL=config['DEFAULT']['LEVEL']
PARSED_LOGS=config['DEFAULT']['PARSED_LOGS_DIR']


dest_train_path = Path(PARSED_LOGS)/issue
create_fasttext_sequence_representation(str(dest_train_path), LEVEL)

from defects4all.describe_mt import describe_mt

mt_stats_path = dest_train_path/"sequence"
describe_mt(mt_stats_path)
