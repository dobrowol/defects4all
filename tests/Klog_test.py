import pytest
import os
from pathlib import Path
from defects4all.Klog import Klog

def count_sequence_from_many_lines(sequences):
    count = 0
    for seq in sequences:
        count += len(seq.split()[1:])
    return count

class NumberOfSentences:
    def __init__(self,level, overlap):
        self._log_event_number_getter = self._get_log_events_counter(level)
        self._number_of_sentences_counter = self._get_sentences_counter(overlap)

    def _training_num_of_log_event(self, sequence):
        print("_training_num_of_log_event ", len(sequence.split()[1:]), sequence)
        return len(sequence.split()[1:])

    def _testing_num_of_log_event(self, sequence):
        print("_testing_num_of_log_event ", len(sequence.split()), sequence)
        return len(sequence.split())

    def _get_log_events_counter(self,level):
        if level == "training":
            return self._training_num_of_log_event
        else:
            return self._testing_num_of_log_event
        
    def _get_sentences_counter(self, overlap):
        if overlap == True:
            return self._sentences_overlaping_counter
        else:
            return self._sentences_nonoverlaping_counter

    def _sentences_nonoverlaping_counter(self, sequences, klog_size, sentence_size):
        num = 0
        print("_sentences_nonoverlaping_counter ", len(sequences))
        for seq in sequences:
            log_event_num = self._log_event_number_getter(seq)
            if log_event_num < klog_size:
                print("add 1")
                num+= 1
            elif log_event_num - klog_size < sentence_size:
                print("add 1")
                num += 1
            else:
                print("add ", (log_event_num - klog_size + 1)//sentence_size)
                num += (log_event_num - klog_size + 1)//sentence_size
        return num

    def _sentences_overlaping_counter(self, sequences, klog_size, sentence_size):
        num = 0
        for seq in sequences:
            log_event_num = self._log_event_number_getter(seq)
            if log_event_num < klog_size:
                num+= 1
            elif log_event_num - klog_size < sentence_size:
                num += 1
            else:
                num += log_event_num - klog_size - sentence_size + 2
        return num

    def countSentences(self, sequences, klog_size, sentence_size):
        return self._number_of_sentences_counter(sequences, klog_size, sentence_size)


@pytest.fixture
def init_subsequences():
    with open("./tests/data/issue_test2/ut_log_as_sentence.vec") as f:
        subsequences=f.readlines()
    return subsequences

def test_create_klog_from_sequence():
    klog_size=3
    klog_overlap=True

    train = True
    specific_out_dir = "./tests/out/test_create_klog_from_sequence"
    Path(specific_out_dir).mkdir(parents=True, exist_ok=True)
    train_log_sequence_file = "./tests/data/issue_test/1_sentence.vec"
    klog = Klog(train_log_sequence_file, specific_out_dir)
    klog_train_file = klog.prepare_klog_file("training", klog_size, 0, True, False)
    with open(klog_train_file.pop()) as f:
        line = f.readline()
    print("line ", line)
    assert(line.split()[0] == "__label__someTest")

    assert(line=="__label__someTest\t1t2t3t 2t3t4t 3t4t5t\n")

def test_create_sentence_longer_than_sequence():
    klog_size=3
    klog_overlap=True
    sentence_size=40

    train = True
    specific_out_dir = "./tests/out/test_create_klog_from_sequence"
    Path(specific_out_dir).mkdir(parents=True, exist_ok=True)
    train_log_sequence_file = "./tests/data/issue_test/1_sentence.vec"
    klog = Klog(train_log_sequence_file, specific_out_dir)
    klog_train_file = klog.prepare_klog_file("training", klog_size, sentence_size, True, False)
    with open(klog_train_file.pop()) as f:
        line = f.readline()
    print("line ",line)
    assert(line.split()[0] == "__label__someTest")

    assert(line=="__label__someTest\t1t2t3t 2t3t4t 3t4t5t\n")

def test_few_examples_shorter_than_klog_and_sentence():
    klog_size=4
    klog_overlap=True
    sentence_size=6

    train = True
    specific_out_dir = "./tests/out/test_few_examples_shorter_than_sentence"
    Path(specific_out_dir).mkdir(parents=True, exist_ok=True)
    train_log_sequence_file = "./tests/data/few_shorter_than_sentence/ut_log_as_sentence.vec"
    klog = Klog(train_log_sequence_file, specific_out_dir)
    klog_train_file = klog.prepare_klog_file("training", klog_size, sentence_size, True, False)
    with open(klog_train_file.pop()) as f:
        line = f.readline()
    print("line ",line)
    assert(line.split()[0] == "__label__AxcContainerConfUncompressedWisdomTest")

    assert(line=="__label__AxcContainerConfUncompressedWisdomTest\t389t389t\n")


def test_create_klog_from_sequence_shorter_than_klog_size():
    klog_size=3
    klog_overlap=True

    train = True
    specific_out_dir = "./tests/out/test_create_klog_from_sequence_shorter_than_klog_size"
    Path(specific_out_dir).mkdir(parents=True, exist_ok=True)
    train_log_sequence_file = "./tests/data/issue_test/2_sentence.vec"
    klog = Klog(train_log_sequence_file, specific_out_dir)
    klog_train_file = klog.prepare_klog_file("training", klog_size, 0, True, False)
    with open(klog_train_file.pop()) as f:
        line = f.readline()
    assert(line.split()[0] == "__label__someTest")
    assert(line.split()[1]=="1t2t")

def test_create_overlaping_klogs_for_train_set():
    klog_size=3
    klog_overlap=True

    train = True
    specific_out_dir = "./tests/out/test_create_overlaping_klogs_for_train_set"
    Path(specific_out_dir).mkdir(parents=True, exist_ok=True)
    train_log_sequence_file = "./tests/data/issue_test2/ut_log_as_sentence.vec"
    klog = Klog(train_log_sequence_file, specific_out_dir)
    klog_train_file = klog.prepare_klog_file("training", klog_size, 0, True, False)
    klog_res = klog_train_file.pop()
    assert(klog_res == "./tests/out/test_create_overlaping_klogs_for_train_set/klog3/klog_overlap_sentence_nooverlap.klog")
    with open(klog_res) as f:
        line = f.readline()
    assert(line.split('\t')[0] == "__label__ClipperWisdomTest_LTE20x2")
    assert(line.split('\t')[1].split()[0] == "406t406t249t")
    assert(line.split('\t')[1].split()[-1] == "409t422t423t")

def test_create_overlaping_klogs_in_sentence_for_train_set():
    klog_size=3
    klog_overlap=True
    sentence_size=5

    train = True
    specific_out_dir = "./tests/out/test_create_overlaping_klogs_in_sentence_for_train_set"
    Path(specific_out_dir).mkdir(parents=True, exist_ok=True)
    train_log_sequence_file = "./tests/data/issue_test2/ut_log_as_sentence.vec"
    klog = Klog(train_log_sequence_file, specific_out_dir)
    klog_train_file = klog.prepare_klog_file("training", klog_size, sentence_size, True, False)
    with open(klog_train_file.pop() )as f:
        lines = f.readlines()
    print(lines)
    assert(lines[0].split('\t')[0] == "__label__ClipperWisdomTest_LTE20x2")
    assert(lines[1].split('\t')[0] == "__label__ClipperWisdomTest_LTE20x2")
    assert(lines[0].split('\t')[1].split()[0] == "406t406t249t")
    assert(lines[0].split('\t')[1].split()[-1] == "407t407t408t")
    assert(lines[-1].split('\t')[1].split()[-1] == "420t420t421t")

def test_create_overlaping_klogs_in_sentence_for_train_set():
    klog_size=3
    klog_overlap=True
    sentence_size=5

    train = True
    specific_out_dir = "./tests/out/test_create_overlaping_klogs_in_sentence_for_train_set"
    Path(specific_out_dir).mkdir(parents=True, exist_ok=True)
    train_log_sequence_file = "./tests/data/issue_test2/ut_log_as_sentence_3.vec"
    klog_train_file = klog.prepare_klog_file("training", klog_size, sentence_size, True, False)
    with open(klog_train_file.pop() )as f:
        lines = f.readlines()
    print(lines)
    assert(lines[0].split('\t')[0] == "__label__ClipperWisdomTest_LTE20x2")
    assert(lines[1].split('\t')[0] == "__label__ClipperWisdomTest_LTE20x2")
    assert(lines[0].split('\t')[1].split()[0] == "406t406t249t")
    assert(lines[0].split('\t')[1].split()[-1] == "407t407t408t")
    assert(lines[-1].split('\t')[1].split()[-1] == "420t420t421t")

def test_create_overlaping_klogs_in_sentence_for_train_set():
    klog_size=3
    klog_overlap=True
    sentence_size=5

    train = True
    specific_out_dir = "./tests/out/test_create_overlaping_klogs_in_sentence_for_train_set"
    Path(specific_out_dir).mkdir(parents=True, exist_ok=True)
    train_log_sequence_file = "./tests/data/issue_test2/ut_log_as_sentence_3.vec"
    klog = Klog(train_log_sequence_file, specific_out_dir)
    klog_train_file = klog.prepare_klog_file("training", klog_size, sentence_size, True, False)
    with open(klog_train_file.pop()) as f:
        lines = f.readlines()
    assert(lines[0].split()[0] == "__label__ClipperWisdomTest_LTE20x2")
    assert(lines[1].split()[0] == "__label__ClipperWisdomTest_LTE20x2")
    assert(lines[0].split('\t')[1].split()[0] == "406t406t249t")
    assert(lines[0].split('\t')[1].split()[-1] == "407t407t408t")
    assert(lines[-1].split('\t')[1].split()[-1] == "420t420t421t")

def test_create_overlaping_klogs_and_sentences_for_test_set():
    klog_size=3
    klog_overlap=True
    sentence_overlap=False
    sentence_size=5
    level="testing"

    train = False
    specific_out_dir = "./tests/out/test_create_overlaping_klogs_and_sentences_for_test_set"
    Path(specific_out_dir).mkdir(parents=True, exist_ok=True)
    test_log_sequence_file = "./tests/data/issue_test2/runtime_sentence.vec"
    with open(test_log_sequence_file) as f:
        sequence = f.readline()
    klog = Klog(test_log_sequence_file, specific_out_dir)
    klog_train_file = klog.prepare_klog_file(level, klog_size, sentence_size, klog_overlap, sentence_overlap)
    with open(klog_train_file.pop()) as f:
        lines = f.readlines()
    assert(lines[0].split()[0] == "408t409t410t")
    assert(lines[0].split()[-1] == "412t413t414t")
    ns = NumberOfSentences(level,sentence_overlap)
    assert(len(lines) == ns.countSentences(lines,klog_size,sentence_size))

def test_result_file_should_be_overwritten():
    klog_size=3
    klog_overlap=True

    train = True
    specific_out_dir = "./tests/out/test_result_file_should_be_overwritten"
    Path(specific_out_dir).mkdir(parents=True, exist_ok=True)
    train_log_sequence_file = "./tests/data/issue_test2/ut_log_as_sentence.vec"
    klog = Klog(train_log_sequence_file, specific_out_dir)
    res_file1 = klog.prepare_klog_file("testing", klog_size, 0, True, False)
    with open(res_file1[0]) as f:
        lines1 = f.readlines()
    train_log_sequence_file2 = "./tests/data/issue_test2/ut_log_as_sentence_2.vec"
    klog2 = Klog(train_log_sequence_file2, specific_out_dir)
    res_file2 = klog2.prepare_klog_file("testing", klog_size, 0, True, False)
    assert(len(res_file2) == 1)
    with open(res_file2[0]) as f:
        lines2 = f.readlines()
    assert(len(lines1) != len(lines2))
    assert(len(lines2) == 4)
    assert(lines2[1].split()[-1]=="409t422t423t")
    assert(lines2[2].split()[-1]=="415t416t417t")

def test_create_overlaping_klogs_and_sentences_for_two_test_sets():
    klog_size=3
    klog_overlap=True
    sentence_overlap=False
    sentence_size=5
    level="testing"

    train = False
    specific_out_dir = "./tests/out/test_create_overlaping_klogs_and_sentences_for_two_test_sets"
    rmod1_out_file = "./tests/out/test_create_overlaping_klogs_and_sentences_for_two_test_sets/klog3/sentence5/klog_overlap_sentence_nooverlap_NR_rmod1_1runtime_DEFAULT.klog"
    Path(specific_out_dir).mkdir(parents=True, exist_ok=True)
    test_log_sequence_file = "./tests/data/issue_test2/runtime_sentence_2.vec"
    with open(test_log_sequence_file) as f:
        sequence = f.readline()
    klog = Klog(test_log_sequence_file, specific_out_dir)
    klog_train_file = klog.prepare_klog_file(level, klog_size, sentence_size, klog_overlap, sentence_overlap)
    assert(len(klog_train_file) == 2)
    assert(rmod1_out_file in klog_train_file)
    with open(rmod1_out_file) as f:
        lines = f.readlines()
    assert(lines[0].split()[0] == "408t409t410t")
    assert(lines[0].split()[-1] == "412t413t414t")
    ns = NumberOfSentences(level,sentence_overlap)
    assert(len(lines) == ns.countSentences(lines,klog_size,sentence_size))

def test_number_of_sentence_overlaping():
    klog_size=3
    klog_overlap=True
    sentence_overlap=True
    sentence_size=5
    level="testing"

    train = False
    specific_out_dir = "./tests/out/test_number_of_sentence_overlaping"
    Path(specific_out_dir).mkdir(parents=True, exist_ok=True)
    test_log_sequence_file = "./tests/data/issue_test2/ut_log_as_sentence.vec"
    with open(test_log_sequence_file) as f:
        sequence = f.readline()
    klog = Klog(test_log_sequence_file, specific_out_dir)
    klog_train_file = klog.prepare_klog_file(level, klog_size, sentence_size, klog_overlap, sentence_overlap)
    assert(len(klog_train_file) == 1)
    with open(klog_train_file.pop()) as f:
        lines = f.readlines()
    ns = NumberOfSentences(level,sentence_overlap)
    assert(len(lines) == ns.countSentences(lines,klog_size,sentence_size))

def test_number_of_sentence_overlaping_for_2_6():
    klog_size=2
    klog_overlap=True
    sentence_overlap=True
    sentence_size=6
    level = "training"

    train = False
    specific_out_dir = "./tests/out/test_number_of_sentence_overlaping_for_2_6"
    Path(specific_out_dir).mkdir(parents=True, exist_ok=True)
    test_log_sequence_file = "./tests/data/issue_test_overlap/ut_log_as_sentence_2.vec"
    with open(test_log_sequence_file) as f:
        sequences = f.readlines()
    klog = Klog(test_log_sequence_file, specific_out_dir)
    klog_train_file = klog.prepare_klog_file(level, klog_size, sentence_size, klog_overlap, sentence_overlap)
    assert(len(klog_train_file) == 1)
    with open(klog_train_file.pop()) as f:
        lines = f.readlines()
    ns = NumberOfSentences(level,sentence_overlap)
    assert(len(lines) == ns.countSentences(sequences,klog_size,sentence_size))

def test_number_of_sentence_overlaping_for_10_21():
    klog_size=10
    klog_overlap=True
    sentence_overlap=True
    sentence_size=21
    level = "training"

    train = False
    specific_out_dir = "./tests/out/test_number_of_sentence_overlaping_for_10_21"
    Path(specific_out_dir).mkdir(parents=True, exist_ok=True)
    test_log_sequence_file = "./tests/data/issue_test_overlap/ut_log_as_sentence_2.vec"
    with open(test_log_sequence_file) as f:
        sequences = f.readlines()
    klog = Klog(test_log_sequence_file, specific_out_dir)
    klog_train_file = klog.prepare_klog_file(level, klog_size, sentence_size, klog_overlap, sentence_overlap)
    assert(len(klog_train_file) == 1)
    with open(klog_train_file.pop()) as f:
        lines = f.readlines()
    ns = NumberOfSentences(level,sentence_overlap)
    assert(len(lines) == ns.countSentences(sequences,klog_size,sentence_size))


