from defects4all.find_all_similar_blocks import find_all_similar_blocks

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

def test_find_all_similar_blocks(init_sequence, init_subsequences):
    res = find_all_similar_blocks(init_sequence, init_subsequences)
    assert(17 not in res)
    assert(res[18][0]=="__label__ClipperWisdomTest_LTE20x2") 
