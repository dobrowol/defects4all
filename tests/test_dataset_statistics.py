from defects4all.data_statistics import describe_words
from pathlib import Path
import pandas as pd

def test_describe_tab_separated_data():
    in_dir = "./tests/data/small_dataset_stats"
    out_dir = "./tests/out/small_dataset_stats"
    describe_words(in_dir, out_dir)
    out_file = Path(out_dir)/"issue_test/klog2/klog_overlap_sentence_overlap.klogwords_by_testsuite.csv"
    df = pd.read_csv(out_file)
    assert(df.loc[df['klogs_words'] == '289t814t']['nunique'][0] == 3)
