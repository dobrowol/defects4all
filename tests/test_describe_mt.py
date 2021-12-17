from defects4all.describe_mt import describe_mt
from pathlib import Path

def test_describe_mt():
    in_dir = Path("./tests/data/dataset_stats")
    describe_mt(in_dir)
