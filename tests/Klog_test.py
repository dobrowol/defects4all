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

def test_create_klog_from_sequence():
    klog_size=3
    klog_overlap=True
    klog = Klog(klog_size, klog_overlap)
    sequence="__label__someTest 1 2 3 4 5"
    print(sequence.split()[1:])
    klogs = klog.createKlogsFromSequence(sequence.split()[1:])
    assert(klogs=="1t2t3t 2t3t4t 3t4t5t")

def test_create_klog_from_sequence_shorter_than_klog_size():
    klog_size=3
    klog_overlap=True
    klog = Klog(klog_size, klog_overlap)
    sequence="__label__someTest 1 2"
    print(sequence.split()[1:])
    klogs = klog.createKlogsFromSequence(sequence.split()[1:])
    assert(klogs=="1t2t")

def test_create_overlaping_klogs_for_train_set():
    klog_size=3
    klog_overlap=True
    klog = Klog(klog_size, klog_overlap)

    train = True
    specific_out_dir = "./tests/data/klog_tests/result"
    Path(specific_out_dir).mkdir(parents=True, exist_ok=True)
    train_log_sequence_file = "./tests/data/issue_test2/ut_log_as_sentence.vec"
    klog_train_file = klog.prepare_klog_file(train, train_log_sequence_file, specific_out_dir)
    with open(klog_train_file[0]) as f:
        line = f.readline()
    assert(line.split()[0] == "__label__ClipperWisdomTest_LTE20x2")
    assert(line.split()[1] == "406t406t249t")
    assert(line.split()[-1] == "409t422t423t")

def test_create_overlaping_klogs_and_sentences_for_test_set():
    klog_size=3
    klog_overlap=True
    sentence_size=5
    klog = Klog(klog_size, klog_overlap, sentence_size)

    train = False
    specific_out_dir = "./tests/data/klog_sentence_tests/result"
    Path(specific_out_dir).mkdir(parents=True, exist_ok=True)
    test_log_sequence_file = "./tests/data/issue_test2/runtime_sentence.vec"
    with open(test_log_sequence_file) as f:
        sequence = f.readline()
    klog_train_file = klog.prepare_klog_file(train, test_log_sequence_file, specific_out_dir)
    with open(klog_train_file[0]) as f:
        lines = f.readlines()
    assert(lines[0].split()[0] == "408t409t410t")
    assert(lines[0].split()[-1] == "412t413t414t")
    assert(len(lines) == (len(sequence.split())-1-klog_size+1)//sentence_size)

def test_result_file_should_be_overwrited():
    klog_size=3
    klog_overlap=True
    klog = Klog(klog_size, klog_overlap)

    train = True
    specific_out_dir = "./tests/data/klog_tests/result"
    Path(specific_out_dir).mkdir(parents=True, exist_ok=True)
    train_log_sequence_file = "./tests/data/issue_test2/ut_log_as_sentence.vec"
    klog_train_file_1 = klog.prepare_klog_file(train, train_log_sequence_file, specific_out_dir)
    with open(klog_train_file_1[0]) as f:
        lines1 = f.readlines()
    klog.prepare_klog_file(train, train_log_sequence_file, specific_out_dir)
    with open(klog_train_file_1[0]) as f:
        lines2 = f.readlines()
    assert(len(lines1) == len(lines2))

def test_create_overlaping_klogs_and_sentences_for_two_test_sets():
    klog_size=3
    klog_overlap=True
    sentence_size=5
    klog = Klog(klog_size, klog_overlap, sentence_size)

    train = False
    specific_out_dir = "./tests/data/klog_two_sentences_tests/result"
    Path(specific_out_dir).mkdir(parents=True, exist_ok=True)
    test_log_sequence_file = "./tests/data/issue_test2/runtime_sentence_2.vec"
    with open(test_log_sequence_file) as f:
        sequence = f.readline()
    klog_train_file = klog.prepare_klog_file(train, test_log_sequence_file, specific_out_dir)
    assert(len(klog_train_file) == 2)
    with open(klog_train_file[0]) as f:
        lines = f.readlines()
    assert(lines[0].split()[0] == "408t409t410t")
    assert(lines[0].split()[-1] == "412t413t414t")
    assert(len(lines) == (len(sequence.split())-1-klog_size+1)//sentence_size)


