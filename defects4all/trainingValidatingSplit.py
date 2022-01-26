import random 
from pathlib import Path
import os
from sklearn.model_selection import train_test_split
import pandas as pd
     
def splitToTrainingAndValidatingSet(in_file, out_dir, percentage=0.75):
    fin = open(in_file, 'r') 
    in_dir = os.path.dirname(in_file)

    out_sub_dir = str(Path(in_file).parent).split('/')
    res_dir = Path(out_dir)/out_sub_dir[-3]/out_sub_dir[-2]/out_sub_dir[-1]
    res_dir.mkdir(parents=True, exist_ok=True)

    filename = Path(in_file).stem
    ftrain_name = res_dir / (filename + "_train.txt")
    fvalid_name = res_dir / (filename + "_validate.txt")
    ftrain = open(ftrain_name, 'w') 
    fvalid = open(fvalid_name, 'w') 
    for line in fin: 
        r = random.random() 
        if r < percentage: 
            ftrain.write(line) 
        else: 
            fvalid.write(line) 
    fin.close() 
    ftrain.close() 
    fvalid.close() 
    return ftrain_name, fvalid_name

def train_test_split_file(in_file, percentage=0.75):
    klogs = pd.read_csv(in_file,  sep='\t', encoding='utf-8', index_col=False)
    klogs.columns = ["label", "klog"] 
    return train_test_split(klogs['klog'],
                            klogs['label'], test_size=0.2)
    
