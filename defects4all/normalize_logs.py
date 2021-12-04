import subprocess
import argparse
import os

parser = argparse.ArgumentParser(
    description='defects4All helper tool to parse raw logs to clusters sequence applicable for forstText.')
parser.add_argument("issue", type=str,
    help="issue name")
parser.add_argument("test_type", type=str,
    help="UT or MT")

args = parser.parse_args()

issue = args.issue

if args.test_type == "UT":
    folder = "/UTLogs"
else:
    folder = "/MTLogs"
train_dir = "/var/wodobrow/logs" + folder + "/" + issue 
test_dir = train_dir + "/runtime"
if not os.path.isdir(train_dir+"/normalized"):
    subprocess.call("./normalize.sh %s"% train_dir, shell=True)
if not os.path.isdir(test_dir+"/normalized"):
    subprocess.call("./normalize.sh %s runtime"% test_dir, shell=True)

dest_train_path = "./parsed_logs/"+issue+args.test_type
dest_test_path = dest_train_path + "/runtime/"
if not os.path.isdir(dest_train_path):
    print("create train dir ", dest_train_path)
    os.mkdir(dest_train_path)
subprocess.call("cp %s/normalized/*log %s" %(train_dir, dest_train_path), shell=True)
if not os.path.isdir(dest_test_path):
    print ("create test dir ", dest_test_path)
    os.mkdir(dest_test_path)
print ("cp %s/normalized/*log %s" %(test_dir, dest_test_path))
subprocess.call("cp %s/normalized/*log %s" %(test_dir, dest_test_path), shell=True)


