train_directory = "./parsed_logs/issue1/train/result"
test_directory = "./parsed_logs/issue1/test/result"
import os
from itertools import islice

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

similarities = {}


def find_similar_sequences(line_nbr, sequence):
    similarities_at_line = {}
    for filename in os.listdir(train_directory):

        if filename.endswith(".vec"):
            print("processing sequence ", filename)
            with open(train_directory +"/"+ filename) as subsequence:
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

            if similarity > 0:
                print("adding subsequence ", subsequence_id, " with similarity ", similarity)
                similarities_at_line[subsequence_id] = similarity
    sorted_dir_items =  dict(sorted(similarities_at_line.items(), key=lambda item: item[1], reverse=True)).items()
    print("similar item ", list(sorted_dir_items)[:3])
    return list(sorted_dir_items)[:3]


def sequence_length(sequence_id):
    with open(train_directory +"/"+ sequence_id + ".log.vec") as file:
        lines = file.readlines()
    return len(lines)


for filename in os.listdir(test_directory):
    if filename.endswith(".vec") :
        print('processing ', filename)
        with open(test_directory +"/"+ filename) as sequence:
            lines = sequence.readlines()
            line_nbr = 0
            while line_nbr < len(lines):
                similarities [line_nbr] = find_similar_sequences(line_nbr, lines)
                if similarities [line_nbr]:
                    line_nbr = line_nbr + sequence_length(similarities [line_nbr][0][0])
                else:
                    line_nbr = line_nbr + 1
                print(line_nbr)


for similar_sequence in similarities.items():
    print (similar_sequence)