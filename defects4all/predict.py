from pathlib import Path
#from defects4all.drain_file import normalize_file
#from defects4all.drain_file import read_persistence
from defects4all.drain_RF_infer import infering_file
import pickle
import argparse
from defects4all.data_statistics import get_klogs_median_length
import pandas as pd

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
    help="issue name")

args = parser.parse_args()

model = load_model(Path(args.issue)/"random_forest_model.sav")

#normalized_file = normalize_file(args.file, args.issue)
persistence_file = read_persistence(args.issue)
drain_ini = read_config(args.issue)

drained_file = str(Path(args.file).parents[0])+"/"+str(Path(args.file).stem)+".drain"
if not Path(drained_file).is_file():
    drained_file = infering_file(args.file, drain_ini, persistence_file)

window_size = int(get_window_size(args.issue))
print(window_size)

series = pd.read_csv(drained_file, sep=' ', header = None, index_col = 0, squeeze = True)
with open(drained_file) as drained:
    series = drained.read()
    series = series.split(' ')

#predicted = series.rolling(window=window_size).apply(model.predict)
series = series[:-1]
#for i in predicted:
#    print(i)

i = 0
range_size = 1
window_size=100
import statistics
if window_size < len(series):
    range_size = len(series)-window_size
for window_start in range(range_size):
    i += 1
    #print((model.predict_proba([" ".join(series[window_start:window_start+window_size])) >= 0.75).astype(int))
    #print(window.str.join(" "))
    if (model.predict_proba([" ".join(series[window_start:window_start+window_size])])).max(1).item() > 0.5:
        print(model.predict([" ".join(series[window_start:window_start+window_size])]))
    #print(model.predict(window.str.join(" ")))
print("predicted examples ", i)
#    print(model.predict(window))
