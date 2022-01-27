from defects4all.drain_RF_infer import infering_file
from pathlib import Path
import argparse
import subprocess

parser = argparse.ArgumentParser(
    description='tool to infer templates from log file')
parser.add_argument("issue", type=str,
    help="issue name")
parser.add_argument("file", type=str,
    help="issue name")

args = parser.parse_args()

def normalize_file(in_file, issue):
    in_dir = Path(in_file).parents[0]
    filename = Path(in_file).stem
    subprocess.call("sh ./{}/normalize.sh {}".format(issue, str(in_dir)))    
    assert(Path(in_dir/"normalized"/filename).isfile())
    return in_dir/"normalized"/filename
def read_persistence(issue):
    return Path(issue)/"drain3_state.bin"
def read_config(issue):
    return Path(issue)/"drain3.ini"

normalized_file = normalize_file(args.file, args.issue)
persistance_file = read_persistence(args.issue)
drain_ini = read_config(args.issue)

infering_file(args.file, drain_ini, persistance_file)
