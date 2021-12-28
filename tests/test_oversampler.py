from defects4all.oversampler import oversample_dataframe
from defects4all.data_statistics import get_testsuites_names
from defects4all.data_statistics import get_testsuites_samples_count
import pandas as pd

def test_oversample_small_classes():
    oversampled_value=10
    path = "./tests/data/small_sentence_stats/issue_test/klog11/sentence1/klog_overlap_sentence_overlap.klog"
    df = pd.read_csv(path, sep='\t',names= ["test_suite", "klogs_words"])
    undersampled_classes_exists = False
    res = get_testsuites_samples_count(df)
    for key,value in res.items():
        if value < oversampled_value:
            print(key, " with samples count ", value)
            undersampled_classes_exists=True
            break
    assert(undersampled_classes_exists)
    
    oversampled_df = oversample_dataframe(df,oversampled_value)
    res = get_testsuites_samples_count(oversampled_df)
    for key,value in res.items():
        if value < oversampled_value:
            print(key, " was not correctly oversampled")
            assert(False)
