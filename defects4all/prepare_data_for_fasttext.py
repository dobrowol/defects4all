import subprocess
import argparse
import os
from Drain3.drain_RF_train import parsing_file
from Drain3.drain_RF_infer import infering_file

parser = argparse.ArgumentParser(
    description='defects4All helper tool to parse raw logs to clusters sequence applicable for forstText.')
parser.add_argument("train_dir", type=str,
    help="directory with logs for UT/MT")
parser.add_argument("test_dir", type=str,
    help="directory with logs from life")

args = parser.parse_args()

print("DUPA2")
train_dir = args.train_dir
test_dir = args.test_dr

if not os.path.isdir(train_dir+"/normalized"):
    subrpocess.call("./normalize.sh %s"% train_dir, shell=True)
if not os.path.isdir(test_dir+"/normalized"):
    subrpocess.call("./normalize.sh %s life"% test_dir, shell=True)

print("DUPA3")
dest_train_dir = os.path.dirname(train_dir)
dest_train_path = "./parsed_logs/"+dest_train_dir
dest_test_path = dest_train_path + "/life/"
if not os.path.isdir(dest_train_path):
    os.mkdir(dest_train_path)
    subprocess.call("cp %s/normalized/*log %s" %(train_dir, dest_train_path), shell=True)
if not os.path.isdir(dest_test_path):
    os.mkdir(dest_test_path)
    subprocess.call("cp %s/normalized/*log %s" %(test_dir, dest_test_path), shell=True)

import glob

print("DUPA4")
for f in glob.glob(dest_train_path+"/*.log"):
    parsing_file(f.split('/')[-1], dest_train_path)    
for f in  glob.glob(dest_train_path+"/*.log"):
    infering_file(f.split('/')[-1], dest_train_path)    

subprocess.call("rm -rf %s/*log"%dest_train_path, shell=True)
subprocess.call("cp %s/result/*drain %s"% (dest_train_path, dest_train_path), shell=True)
subprocess.call("rm -rf %s/result" %dest_train_path, shell=True)

for f in  glob.glob(dest_test_path+"/*.log"):
    infering_file(f.split('/')[-1], dest_test_path)    

subprocess.call("rm -rf %s/*log"%dest_test_path, shell=True)
subprocess.call("cp %s/result/*drain %s"% (dest_test_path, dest_test_path), shell=True)
subprocess.call("rm -rf %s/result" %dest_test_path, shell=True)

import createFastTextTestSet
import createFastTextTrainSet

createFastTextTrainSet.create_fasttext_sequence_representation(dest_train_path)
for f in  glob.glob(dest_train_path+"/*.drain"):
    createFastTextTestSet.create_fasttext_sequence_representation(f)
