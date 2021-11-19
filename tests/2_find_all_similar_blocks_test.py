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


def test_find_all_similar_blocks2(init_sequence, init_subsequences):
    start_time = time.time()
    res = find_all_similar_blocks2(init_sequence, init_subsequences)
    print("--- %s seconds ---" % (time.time() - start_time))
    assert(17 not in res)
    assert(res[18][0]=="__label__ClipperWisdomTest_LTE20x2") 
    assert(res[0][0]=="__label__ClipperWisdomTest_LTE20x2") 
def test_find_all_similar_blocks_perf(perf_sequence, perf_subsequences):
    start_time = time.time()
    res = find_all_similar_blocks2(perf_sequence, perf_subsequences)
    elapsed_time=(time.time() - start_time)
    assert (elapsed_time < 120)
