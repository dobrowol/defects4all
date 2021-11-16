import createFastTextTestSet
import createFastTextTrainSet
import subprocess
import glob
import argparse

parser = argparse.ArgumentParser(
    description='defects4All helper tool to drain parsed logs to clusters sequence applicable for forstText.')
parser.add_argument("train_dir", type=str,
    help="directory with logs for UT/MT")
parser.add_argument("test_dir", type=str,
    help="directory with logs from life")

args = parser.parse_args()

dest_train_path = args.train_dir
dest_test_path = args.test_dir


createFastTextTrainSet.create_fasttext_sequence_representation(dest_train_path)
for f in  glob.glob(dest_test_path+"/*.drain"):
    createFastTextTestSet.create_fasttext_sequence_representation(f)
