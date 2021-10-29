train_directory = "./parsed_logs/issue1/train/result"
test_directory = "./parsed_logs/issue1/test/result"
import os
from itertools import islice
import argparse
import difflib
from operator import itemgetter

parser = argparse.ArgumentParser(
    description='fastText helper tool to reduce model dimensions.')
parser.add_argument("train_directory", type=str,
    help="directory with basic sequences")
parser.add_argument("test_file", type=str,
    help="directory with sequence to be analyzed")

args = parser.parse_args()

train_directory = args.train_directory
test_file = args.test_file

if train_directory[-1] != '/':
    train_directory.append('/')

vec_train_dir = train_directory + "sequence"

#if not os.path.exists(vec_test_dir):
#    create_vector_represetation(test_directory)
#if not os.path.exists(vec_train_dir):
#    create_vector_representation(train_directory)


similarities = {}


def find_similar_sequences(sequence):
    similarities_at_line = {}
    lenSeq = len(sequence)
    lenSeqStart = len(sequence.split(' ')[0])# skip the __label_name

    filename = "ut_log_as_sentence.vec"
    with open(vec_train_dir +"/"+ filename) as subsequence:
        lines = subsequence.readlines()
    for line in lines:
        lenLine = len(line)
        subsequence_id = line.split(' ')[0]
        lenLineStart = len(subsequence_id)
        temp = difflib.SequenceMatcher(None,sequence ,line)#skip the __label__name
        m = temp.find_longest_match(lenSeqStart, lenSeq, lenLineStart, lenLine)
        ratio = m.size/(lenLine)
        #print (ratio)
        if ratio > 0:
            if m.a not in similarities_at_line:
                similarities_at_line[m.a] = []
            similarities_at_line[m.a].append([subsequence_id, ratio, m])
        #print("adding subsequence ", subsequence_id, " with similarity ", similarity)
    for key, value in similarities_at_line.items():
        similarities_at_line[key] = (sorted(value, key=itemgetter(1),reverse=True))[:3]
    return similarities_at_line 


def sequence_length(sequence_id):
    filename = vec_train_dir +"/"+ sequence_id + ".log.res.vec"
    if not os.path.exists(filename):
        filename = vec_train_dir +"/"+ sequence_id + ".log.vec"
    with open(filename) as file:
        lines = file.readlines()
    return len(lines)


with open(test_file) as sequence_file:
    sequence = sequence_file.readline()
    similarities = find_similar_sequences(sequence)


for similar_sequence in sorted(similarities.items()):
    print (similar_sequence)
