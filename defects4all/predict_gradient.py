from pathlib import Path
#from defects4all.drain_file import normalize_file
#from defects4all.drain_file import read_persistence
from defects4all.drain_RF_infer import infering_file
import pickle
import argparse
from defects4all.data_statistics import get_klogs_median_length
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from defects4all.trainingValidatingSplit import train_test_split_file
import numpy as np

def load_model(model_file):
    with open(model_file, 'rb') as fid:
        return pickle.load(fid)

def read_persistence(issue):
    return Path(issue)/"drain3_state.bin"
def read_config(issue):
    return Path(issue)/"drain3.ini"


def get_window_size(issue):
    df = pd.read_csv(Path(issue)/"output.csv", header=None, sep='\t', names=["test_suite", "klogs_words"])
    return get_klogs_median_length(df)

parser = argparse.ArgumentParser(
    description='tool to infer templates from log file')
parser.add_argument("issue", type=str,
    help="issue name")
parser.add_argument("file", type=str,
    help="production log")

args = parser.parse_args()

#model = load_model(Path(args.issue)/"random_forest_model.sav")
model = load_model(Path(args.issue)/"gradient_boost_model.sav")

label_encoder = LabelEncoder()
label_encoder.classes_ = np.load(Path(args.issue)/'label_encoder.sav.npy', allow_pickle=True)

#normalized_file = normalize_file(args.file, args.issue)
persistence_file = read_persistence(args.issue)
drain_ini = read_config(args.issue)

drained_file = str(Path(args.file).parents[0])+"/"+str(Path(args.file).stem)+".drain"
if not Path(drained_file).is_file():
    drained_file = infering_file(args.file, drain_ini, persistence_file)

window_size = int(get_window_size(args.issue))
print(window_size)

#for i in predicted:
#    print(i)
with open(args.file) as drained:
    series = drained.read()
    series = series.split(' ')


i = 0
range_size = 1
window_size=100
import statistics
if window_size < len(series):
    range_size = len(series)-window_size
max_prob = 0
best_window_size = 10
from tqdm import tqdm
#for window in tqdm(range(10, len(series), 100)):
#    for window_start in range(len(series)-window_size):
#        i += 1
#        prob = (model.predict_proba([" ".join(series[window_start:window_start+window_size])])).max(1).item()
#        if prob > max_prob:
#            print("better prob found {} for window {}".format(prob, window))
#            max_prob = prob
#            best_window_size = window
       #print(model.predict([" ".join(series[window_start:window_start+window_size])]))
    #print(model.predict(window.str.join(" ")))
#best_window_size=0
print("best window ", best_window_size, " has prob ", max_prob)

pred_file = str(Path(args.file).parents[0])+"/"+str(Path(args.file).stem)+"_gradient.pred"
pred05_file = str(Path(args.file).parents[0])+"/"+str(Path(args.file).stem)+"gradient_05"+".pred"
pred = open(pred_file,"w")
pred05 = open(pred05_file, "w")
best_window_size=1000
target_label = label_encoder.transform(["__label__org.apache.hadoop.hdfs.server.blockmanagement.TestReplicationPolicy"])[0]
print ("target label", target_label)
for window_start in range(len(series)-best_window_size):
    prob = (model.predict_proba([" ".join(series[window_start:window_start+best_window_size])])).max(1).item()
    label = model.predict([" ".join(series[window_start:window_start+best_window_size])])
    pred.write(str(window_start)+","+str(window_start+best_window_size)+","+label_encoder.inverse_transform([label])[0]+"\n")
    if prob > 0.5:
        pred05.write(str(window_start)+","+str(window_start+best_window_size)+","+label_encoder.inverse_transform([label])[0]+"\n")
        print(prob, window_start, window_start+best_window_size, label_encoder.inverse_transform([label])[0])

pred.close()
pred05.close()
    
