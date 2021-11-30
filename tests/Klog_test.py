from defects4all.Klog import Klog
from defects4all.createFastTextTrainSet import create_fasttext_sequence_representation
import pytest
import os
from pathlib import Path

@pytest.fixture
def init_subsequences():
    with open("./tests/data/issue_test2/ut_log_as_sentence.vec") as f:
        subsequences=f.readlines()
    return subsequences



def test_create_overlaping_klogs_for_train_set(init_subsequences):
    klog_size=3
    klog_overlap=True
    klog = Klog(klog_size, klog_overlap)
    train = True
    specific_out_dir = "./tests/data/klog_tests/result"
    Path(specific_out_dir).mkdir(parents=True, exist_ok=True)
    train_log_sequence_file = "./tests/data/issue_test2/ut_log_as_sentence.vec"
    klog_train_file = klog.prepare_klog_file(train, train_log_sequence_file, specific_out_dir)
