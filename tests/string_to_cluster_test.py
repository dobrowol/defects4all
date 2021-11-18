from defects4all.string_to_cluster import get_cluster_position

import pytest

@pytest.fixture
def init_sequence():
    with open("./tests/data/issue_test2/runtime_sentence.vec") as f:
        sequence=f.readline()
    return sequence


def test_cluster_id_after_label_should_be_0_blocks(init_sequence):
    res = get_cluster_position(init_sequence, 35)
    assert(res == 1) 

def test_cluster_id_should_be_ok_blocks(init_sequence):
    res = get_cluster_position(init_sequence, 104)
    print(init_sequence.split()[res])
    print(res)
    assert(init_sequence.split()[res] == '408')
    assert(init_sequence.split()[res+1] == '409')
    assert(res == 18) 
