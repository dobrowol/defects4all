from drain_RF_train import parsing_file
from drain_RF_infer import infering_file
import argparse
import os
import glob
import subprocess

parser = argparse.ArgumentParser(
    description='defects4All helper tool to drain parsed logs to clusters sequence applicable for forstText.')
parser.add_argument("issue", type=str,
    help="issue name")

args = parser.parse_args()
issue = args.issue

dest_train_path = "../parsed_logs/"+issue+"/"
dest_test_path = dest_train_path + "/life/"

persistent_dir = issue
if not os.path.isdir(persistent_dir):
    os.mkdir(persistent_dir)
persistent_file = persistent_dir + "/drain3_state.bin"
if not os.path.isfile(persistent_file):
    for f in glob.glob(dest_train_path+"/*.log"):
        parsing_file(f.split('/')[-1], dest_train_path, persistent_file)    
for f in  glob.glob(dest_train_path+"/*.log"):
    infering_file(f.split('/')[-1], dest_train_path, persistent_file)    

#subprocess.call("rm -rf %s/*log"%dest_train_path, shell=True)
subprocess.call("cp %sresult/*drain %s"% (dest_train_path, dest_train_path), shell=True)
subprocess.call("rm -rf %sresult" %dest_train_path, shell=True)

for f in  glob.glob(dest_test_path+"/*.log"):
    infering_file(f.split('/')[-1], dest_test_path, persistent_file)    

#subprocess.call("rm -rf %s/*log"%dest_test_path, shell=True)
subprocess.call("cp %sresult/*drain %s"% (dest_test_path, dest_test_path), shell=True)
subprocess.call("rm -rf %sresult" %dest_test_path, shell=True)

import createFastTextTestSet
import createFastTextTrainSet

createFastTextTrainSet.create_fasttext_sequence_representation(dest_train_path)
for f in  glob.glob(dest_test_path+"/*.drain"):
    createFastTextTestSet.create_fasttext_sequence_representation(f)
