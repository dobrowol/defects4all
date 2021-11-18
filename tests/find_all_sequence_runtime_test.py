from defects4all.find_similar_sequences import find_similar_sequences 
import pytest

@pytest.fixture
def init_sequence():
    with open("./tests/data/issue_test2/runtime_sentence.vec") as f:
        sequence=f.readline()
    return sequence

@pytest.fixture
def init_subsequences():
    with open("./tests/data/issue_test2/ut_log_as_sentence.vec") as f:
        subsequences=f.readlines()
    return subsequences

def test_find_best_sequence_at_0(init_sequence, init_subsequences):
    res = find_similar_sequences(init_sequence, init_subsequences)
    assert(res[0][0] == '__label__ClipperWisdomTest_LTE20x2')
    #assert(res[18][0] == '__label__ClipperWisdomTest_LTE20x2')
    #assert(res[35][0] == '__label__ClipperWisdomTest_LTE20x2')
