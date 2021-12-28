from defects4all.balance_dataframe import balance_dataframe
from defects4all.data_statistics import describe_samples
import pandas as pd

def test_balance_dataframe():
    path = "./tests/data/small_sentence_stats/issue_test/klog11/sentence1/klog_overlap_sentence_overlap.klog"
    df = pd.read_csv(path, sep='\t',names= ["test_suite", "klogs_words"])
    before = describe_samples(df)
    balanced_df = balance_dataframe(df)
    
    after = describe_samples(balanced_df)
    assert(50*before.max()//100 == after.max())
