from defects4all.drain_RF_train import parsing_file
from defects4all.drain_RF_infer import infering_file
from defects4all.template_miner import get_template_miner
import argparse
import os
import glob
import subprocess
import configparser

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

dest_train_path = PARSED_LOGS+"/"+issue+"/"
dest_test_path = dest_train_path + "/runtime/"

persistent_dir = issue
if not os.path.isdir(persistent_dir):
    os.mkdir(persistent_dir)
persistent_file = issue + "/drain3_state.bin"
config_file = issue + "/drain3.ini"
template_miner = get_template_miner(config_file, persistent_file)
from tqdm import tqdm
if not os.path.isfile(persistent_file):
    print("training drain")
    for f in tqdm(glob.glob(dest_train_path+"/*.log")):
        parsing_file(f, template_miner)    
#if not glob.glob(dest_train_path+"/*drain"):
print("infering files")
for f in  tqdm(glob.glob(dest_train_path+"/*.log")):
    infering_file(f, template_miner)    
#subprocess.call("rm -rf %s/*log"%dest_train_path, shell=True)
subprocess.call("cp %sresult/*drain %s"% (dest_train_path, dest_train_path), shell=True)
subprocess.call("rm -rf %sresult" %dest_train_path, shell=True)

#for f in  glob.glob(dest_test_path+"/*.log"):
#    infering_file(f, template_miner)    

#subprocess.call("rm -rf %s/*log"%dest_test_path, shell=True)
#subprocess.call("cp %sresult/*drain %s"% (dest_test_path, dest_test_path), shell=True)
#subprocess.call("rm -rf %sresult" %dest_test_path, shell=True)

#import defects4all.createFastTextTestSet
from defects4all.createFastTextTrainSet import create_fasttext_sequence_representation 

create_fasttext_sequence_representation(dest_train_path, LEVEL)
#for f in  glob.glob(dest_test_path+"/*.drain"):
#    createFastTextTestSet.create_fasttext_sequence_representation(f)
