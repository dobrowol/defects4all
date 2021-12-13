import pandas as pd
from pathlib import Path

def describe_datasets(input_dir):
    for path in Path(input_dir).rglob('klog*/sentence1/*.klog'):
        print("word statistics for ", path)
        df = pd.read_csv(path, sep='\t',names= ["test_suite", "klogs"])
        print(df.klogs.value_counts())
    for path in Path(input_dir).rglob('*.klog'):
        print(path)
        #for line in f.readlines():
        #    print(line)
        #    klogs = line.split('\t')[1]
        #    klogs_list["klogs"].extend(klogs.split())
        dataset = pd.read_csv(path, sep='\t',names=["test_suite", "klogs"])
        
        print ("balance of dataset", path)
        #dataset = pd.read_csv(path, sep='\t')
        #pd.dataset.iloc[:, 2]
        print(dataset.test_suite.value_counts(normalize=True))
        print(dataset.describe())

#describe_datasets("./klogs")
