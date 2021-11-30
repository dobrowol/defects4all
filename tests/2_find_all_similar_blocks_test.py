from defects4all.find_all_similar_blocks import find_all_similar_blocks2
import time

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

@pytest.fixture
def perf_subsequences():
    with open("./tests/data/issue_perf/ut_log_as_sentence.vec") as f:
        subsequences=f.readlines()
    return subsequences
@pytest.fixture
def perf_sequence():
    with open("./tests/data/issue_perf/runtime_sentence.vec") as f:
        sequence=f.readline()
    return sequence

def test_match_is_whole_subseq_many_times():
    sequence="__label__seq 1 2 3 4 5 6 7 1 2 3 4 5 6 76 1 2 3"
    subseq = ["__label__subseq 1 2 3"]
    res = find_all_similar_blocks2(sequence, subseq)
    assert(res[1][0]=="__label__subseq")
    assert(res[2][0]=="__label__subseq")
    assert(res[3][0]=="__label__subseq")
    assert(4 not in res)
    assert(7 not in res)
    assert(res[8][0]=="__label__subseq")
    assert(res[9][0]=="__label__subseq")
    assert(res[10][0]=="__label__subseq")
    assert(11 not in res)
    assert(res[15][0]=="__label__subseq")
    assert(res[16][0]=="__label__subseq")
    assert(res[17][0]=="__label__subseq")
def test_find_all_similar_blocks2(init_sequence, init_subsequences):
    start_time = time.time()
    res = find_all_similar_blocks2(init_sequence, init_subsequences)
    print("--- %s seconds ---" % (time.time() - start_time))
    assert(17 not in res)
    assert(res[18][0]=="__label__ClipperWisdomTest_LTE20x2") 
    assert(res[1][0]=="__label__ClipperWisdomTest_LTE20x2") 
    assert(0 not in res)
def find_all_similar_blocks_perf(perf_sequence, perf_subsequences):
    start_time = time.time()
    res = find_all_similar_blocks2(perf_sequence, perf_subsequences)
    elapsed_time=(time.time() - start_time)
    assert (elapsed_time < 120)
