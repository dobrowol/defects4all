from defects4all.data_statistics import describe_datasets

def test_describe_tab_separated_data():
    in_dir = "./tests/data/dataset_stats"
    describe_datasets(in_dir)
