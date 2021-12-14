import pandas as pd
from pathlib import Path

def describe_mt(input_dir):
    for path in Path(input_dir).glob('*.vec'):
        print("mt statistics for ", path)
        data = pd.read_csv(path, sep='\t',names=["test_suite","sequence"])
        data["sequence_length"]= data["sequence"].str.split().apply(len)
        print("sequence length counts")
        print(data.sequence_length.value_counts())
        print("sequence length mean")
        print(data.sequence_length.agg(['min', 'max', 'mean', 'median']))
