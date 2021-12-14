import createFastTextTrainSet
import configparser
import argparse

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
PARSED_LOGS=config['DEFAULT']['PARSED_LOGS']


dest_train_path = PARSED_LOGS+"/"+issue+"/"
createFastTextTrainSet.create_fasttext_sequence_representation(dest_train_path, LEVEL)

from defects4all.describe_mt import describe_mt

describe_mt(dest_train_path)
