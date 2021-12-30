import subprocess
from pathlib import Path
from defects4all.balance_dataframe import balance_dataframe
import pandas as pd
import csv
class FastTextTrainer:

    def __init__(self, fasttext_dir, in_file):
        specific_train_in_dir = str(Path(in_file).parent)
        self.filename = in_file
        file_no_ext = Path(in_file).stem
        self.model_file = specific_train_in_dir+"/klog_model_"+file_no_ext
        self.fasttext_dir = fasttext_dir

    def train(self):
        self.balance()
        subprocess.call("%s/fasttext supervised -input %s -output %s -lr 0.1 -epoch 25 -wordNgrams 2" %(self.fasttext_dir, self.filename, self.model_file), shell=True)
        return self.model_file+".bin"

    def balance(self):
        df = pd.read_csv(self.filename, sep='\t',names= ["test_suite", "klogs_words"])
        
        balanced_df = balance_dataframe(df)
        balanced_df.to_csv(self.filename, sep='\t', index=False, header=False)
        print("write balanced DF to ",self.filename)
        
