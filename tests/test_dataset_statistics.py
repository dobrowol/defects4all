from defects4all.data_statistics import klogs_present_in_one_testsuite
from defects4all.data_statistics import klogs_and_coresponding_testsuites
from pathlib import Path
import pandas as pd

def test_should_have_three_unique_klogs():
    path = "./tests/data/small_dataset_stats/issue_test/klog2/sentence1/klog_overlap_sentence_overlap.klog"
    df = pd.read_csv(path, sep='\t',names= ["test_suite", "klogs_words"])
    
    res = klogs_present_in_one_testsuite(df)
    assert(len(res) == 2)
    assert(res["__label__AfeIntestinesTest"] == 3)
    assert(res["__label__ECpriNR5GDualCarrierFixture"] == 1)

def test_one_klog_is_in_two_tests():
    path = "./tests/data/small_sentence_stats/issue_test/klog11/sentence1/klog_overlap_sentence_overlap.klog"
    df = pd.read_csv(path, sep='\t',names= ["test_suite", "klogs_words"])
    res = klogs_and_coresponding_testsuites(df)
    assert(res.loc[res["klogs_words"] == "1236t"]['nunique'][0] == 2)
