train_directory = "./parsed_logs/issue1/train/result"
test_directory = "./parsed_logs/issue1/test/result"
import os
from itertools import islice
import argparse
from createVector import create_vector_representation

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

if test_directory[-1] != '/':
    test_directory.append('/')
if train_directory[-1] != '/':
    train_directory.append('/')

vec_test_dir = test_directory + "vector"
vec_train_dir = train_directory + "vector"

if not os.path.exists(vec_test_dir):
    create_vector_representation(test_directory)
if not os.path.exists(vec_train_dir):
    create_vector_representation(train_directory)


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

similarities = {}


def find_similar_sequences(line_nbr, sequence):
    similarities_at_line = {}
    for filename in os.listdir(vec_train_dir):

        if filename.endswith(".vec"):
            with open(vec_train_dir +"/"+ filename) as subsequence:
                lines = subsequence.readlines()
            subsequence_id = filename.split('.')[0]
            c = 1
            similarity = 0
            sequence_line = line_nbr
            seq_length = len(sequence)
            max_subseq_length = seq_length - line_nbr
            subseq_line_nbr = 0
            if max_subseq_length > len(lines):
                max_subseq_length = len(lines)
            while subseq_line_nbr < max_subseq_length:
                if lines[subseq_line_nbr] == sequence[sequence_line]:
                    similarity = similarity + c
                    c = c + 1
                else:
                    c = 1
                sequence_line = sequence_line + 1
                subseq_line_nbr = subseq_line_nbr + 1

            if similarity/len(lines) > 0:
                #print("adding subsequence ", subsequence_id, " with similarity ", similarity)
                similarities_at_line[subsequence_id] = similarity/len(lines)
    sorted_dir_items =  dict(sorted(similarities_at_line.items(), key=lambda item: item[1], reverse=True)).items()
    return list(sorted_dir_items)[:3]


def sequence_length(sequence_id):
    filename = vec_train_dir +"/"+ sequence_id + ".vec"
    with open(filename) as file:
        lines = file.readlines()
    return len(lines)


for filename in os.listdir(vec_test_dir):
    if filename.endswith(".vec") :
        with open(vec_test_dir +"/"+ filename) as sequence:
            lines = sequence.readlines()
            line_nbr = 0
            while line_nbr < len(lines):
                similarities [line_nbr] = find_similar_sequences(line_nbr, lines)
                if similarities [line_nbr]:
                    seq_len = sequence_length(similarities [line_nbr][0][0])
                    #print ("at line ", line_nbr, " most similar ", similarities [line_nbr][0][0], " of length ", seq_len)
                    #line_nbr = line_nbr + sequence_length(similarities [line_nbr][0][0])
                #else:
                line_nbr = line_nbr + 1
                #print (line_nbr)


out_dir = "./results/issue4/"
out_file = "lcs_similarities_sequence.txt"
if not os.isdir(out_dir):
    os.mkdir(out_dir)
with open(out_dir+out_file, "w+") as f:
    for similar_sequence in similarities.items():
        f.write(similar_sequence+"\n")
