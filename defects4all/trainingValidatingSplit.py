import random 
from pathlib import Path
import os
     
def splitToTrainingAndValidatingSet(in_file, percentage=0.75):
    fin = open(in_file, 'r') 
    in_dir = os.path.dirname(in_file)
    filename = Path(in_file).stem
    ftrain_name = in_dir + "/" + filename + "_train.txt"
    fvalid_name = in_dir + "/" + filename + "_validate.txt"
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
