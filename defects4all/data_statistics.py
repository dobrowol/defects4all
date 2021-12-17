import pandas as pd
from pathlib import Path

def describe_words(input_dir, output_dir):
    for path in Path(input_dir).rglob('klog*/sentence1/*.klog'):
        print("word statistics for ", path)
        sub_dirs = str(path.parent).split('/')
        out_dir = Path(output_dir)/sub_dirs[-3]/sub_dirs[-2] 
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir/(str(path.name)+"words.csv")
        df = pd.read_csv(path, sep='\t',names= ["test_suite", "klogs_words"])
        df.klogs_words.value_counts().to_csv(out_file, index=True, header=True)
        out_grouped_file = out_dir/(str(path.name)+"words_by_testsuite.csv")
        res = df.groupby("klogs_words")["test_suite"].nunique().reset_index(name='nunique').sort_values(['nunique'], ascending=False)
        #for key, item in res:
        #    print(res.get_group(key), "\n\n")
        res.to_csv(out_grouped_file, index=False, header=True)
        #print(res)

def describe_sentence(input_dir):
    for path in Path(input_dir).rglob('*.klog'):
        print(path)
        out_file = str(path)+".csv"
        out_agg_file = str(path)+".agg.csv"
        #for line in f.readlines():
        #    print(line)
        #    klogs = line.split('\t')[1]
        #    klogs_list["klogs"].extend(klogs.split())
        dataset = pd.read_csv(path, sep='\t',names=["test_suite", "klogs"])
        
        print ("balance of dataset ", out_file)
        print ("aggregate of dataset ", out_agg_file)
        #dataset = pd.read_csv(path, sep='\t')
        #pd.dataset.iloc[:, 2]
        dataset.test_suite.value_counts().to_csv(out_file, index=True, header=True)
        dataset.test_suite.value_counts().agg(['min', 'max', 'mean', 'median']).to_csv(out_agg_file, index=True, header=True)

#describe_words("./tests/data/small_dataset_stats", "./tests/out/samll_dataset_stats")
