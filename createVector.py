max_num_lines=0
import os
train_directory = "./parsed_logs/issue1/train/"
test_directory = "./parsed_logs/issue1/test/"

import argparse

parser = argparse.ArgumentParser(
    description='fastText helper tool to reduce model dimensions.')
parser.add_argument("train_directory", type=str,
    help="directory with basic sequences")
parser.add_argument("test_directory", type=str,
    help="directory with sequence to be analyzed")

args = parser.parse_args()

if args.train_directory:
    train_directory = args.train_directory
if args.test_directory:
    test_directory = args.test_directory


def create_vector_representation(directory):
    print ("create vec representation ", directory)
    for filename in os.listdir(directory):
        vec_lines = []
        i=0
        if filename.endswith(".drain"):
            with open(directory  + filename) as f:
                lines = f.readlines()
            for line in lines:
                vec_lines.append(line.split('[')[0])
                i = i + 1
            if directory[-1] != '/':
                directory.append('/')
            out_dir = directory + "vector"
            if not os.path.exists(out_dir):
                os.mkdir(out_dir)
            vec_path = out_dir +"/" + filename.split('.')[0] + ".vec"
            with open(vec_path, "a+") as f:
                for item in vec_lines:
                    if item != "None":
                        f.write(item + "\n")


create_vector_representation(train_directory)
create_vector_representation(test_directory)
