from defects4all.find_similar_sequences import find_similar_sequences 
import pytest
import unittest

@pytest.fixture
def init_sequence():
    print("init_sequences fixture")
    sequence="__label__Sequence 23 43 45 56 67 888 2 3 4 3 2 1"
    return sequence

@pytest.fixture
def init_subsequences():
    subsequences=["__label__Sub1 23 43",
            "__label__Sub2 2 3 4 3"]
    return subsequences


def test_find_best_sequence_at_0(init_sequence, init_subsequences):
    res = find_similar_sequences(init_sequence, init_subsequences)
    assert(res[0][0] == '__label__Sub1')

def test_find_best_of_2_sequences(init_sequence, init_subsequences):
    init_subsequences.append("__label__Sub3 23 43 45")
    res = find_similar_sequences(init_sequence, init_subsequences)
    assert(res[0][0] == '__label__Sub3')
    
def test_find_best_of_2_sequences_reverse_order(init_sequence, init_subsequences):
    init_subsequences.append("__label__Sub3 23")
    res = find_similar_sequences(init_sequence, init_subsequences)
    assert(res[0][0] == '__label__Sub1')
