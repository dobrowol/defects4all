import pandas as pd
from pathlib import Path

def describe_datasets(input_dir):
    for path in Path(input_dir).rglob('*.klog'):
        print(path)
        f= open(path,"r")
        klogs_list = {"klogs": []}
        for line in f.readlines():
            print(line)
            klogs = line.split('\t')[1]
            klogs_list["klogs"].extend(klogs.split())
        f.close()
        dataset = pd.DataFrame(klogs_list, columns=["klogs"])
        
        print ("describing ", path)
        #dataset = pd.read_csv(path, sep='\t')
        #pd.dataset.iloc[:, 2]
        print(dataset.klogs.value_counts())
        print(dataset.describe())

#describe_datasets("./klogs")
