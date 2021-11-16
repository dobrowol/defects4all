import os
import argparse
import createFastTextTrainSet
import sys

parser = argparse.ArgumentParser(
    description='fastText helper tool to reduce model dimensions.')
parser.add_argument("issue", type=str,
    help="issue to be processed")

args = parser.parse_args()
issue = args.issue
train_directory = "./parsed_logs/"+issue
test_directory = train_directory +"/life"
vec_train_dir = train_directory + "/sequence"
test_file = test_directory+"/sequence/ut_log_as_sentence.vec"
filename = vec_train_dir + "/" + "ut_log_as_sentence.vec"

if not os.path.isfile(filename):
    train_log_sequence_file = createFastTextTrainSet.create_fasttext_sequence_representation(train_directory)
if not os.path.isfile(test_file):
    test_log_sequence_file = createFastTextTrainSet.create_fasttext_sequence_representation(test_directory)

similarities = {}

filename = vec_train_dir + "/" + "ut_log_as_sentence.vec"
with open(filename) as subsequences_file:
    subsequences = subsequences_file.readlines()
from data_presentation.lcs_python_presentation import similarity_presentation
with open(test_file) as sequence_file:
    sequences = sequence_file.readlines()
for sequence in sequences:
    similarities = find_similar_sequences(sequence, subsequences)

    sequence_id = ((sequence.split()[0]).split("__label__")[1]).split('.')[0]

    similarity_presentation(issue, sequence_id, similarities)
