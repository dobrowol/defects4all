from defects4all.FastTextTrainer import FastTextTrainer
from pathlib import Path
import shutil
import pandas as pd

def test_out_format():
    path = "./tests/data/small_dataset_stats/issue_test/klog2/sentence3/klog_overlap_sentence_overlap.klog"
    out_path = "./tests/out/small_dataset_stats/issue_test/klog2/sentence3/klog_overlap_sentence_overlap.klog"
    Path("./tests/out/small_dataset_stats/issue_test/klog2/sentence3/").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, out_path)
    fastTextTrainer = FastTextTrainer("../fastTextOrig", out_path)
    fastTextTrainer.balance()
    df_balanced = pd.read_csv(out_path, sep='\t',names= ["test_suite", "klogs_words"])
    assert(False)
