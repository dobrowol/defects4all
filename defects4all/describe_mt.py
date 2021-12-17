import pandas as pd
from pathlib import Path

def describe_mt(input_dir):
    for path in input_dir.glob('*.vec'):
        out_file = str(path)+".csv"
        print("mt statistics for ", path)
        data = pd.read_csv(path, sep='\t',names=["test_suite","sequence"])
        data["sequence_length"]= data["sequence"].str.split().apply(len)
        print("sequence length counts")
        data.sequence_length.value_counts().to_csv(out_file, index=True, header=True)
        print("sequence length mean")
        out_agg_file = str(path)+"agg.csv"
        data.sequence_length.agg(['min', 'max', 'mean', 'median']).to_csv(out_agg_file, index=True, header=True)
