from imblearn.over_sampling import RandomOverSampler 
import pandas as pd
import numpy
# define dataset
def oversample_file(in_file):
    out_file = in_file+".over"
    data = pd.read_csv(in_file, sep='\t',names=["test_suite","sequence"])
    #print("y =", numpy.shape(data.test_suite))
    #print("X =", numpy.shape(data.sequence.values.reshape(-1,1)))
    y = data.test_suite.values
    X = data.sequence.values.reshape(-1,1)
    #print(data.sequence)
    #print(X)
    oversample = RandomOverSampler(sampling_strategy='all')
    X_over, y_over = oversample.fit_resample(X, y)
    X_over = numpy.reshape(X_over, -1)
    #print(X_over)
    #print(numpy.shape(y_over))
    #print(numpy.shape(y))
    #print(y_over)
    frame = {"test_suite": y_over, "sequence": X_over} 
    #print(frame)
    data_over = pd.DataFrame(frame)
    data_over.to_csv(out_file, index=False, sep='\t')
    #print(Counter(y_over))
    return out_file

oversample_file("./tests/data/dataset_stats/klog_overlap_sentence_overlap.klog")
    
