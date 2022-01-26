from defects4all.drain_RF_infer import infering_file
import argparse
parser = argparse.ArgumentParser(
    description='tool to infer templates from log file')
parser.add_argument("issue", type=str,
    help="issue name")
parser.add_argument("file", type=str,
    help="issue name")

args = parser.parse_args()

def read_configuration(issue):
    return Path(issue)/"drain3.ini"

drain_ini = read_configurations(args.issue)

infering_file(args.file, drain_ini)




