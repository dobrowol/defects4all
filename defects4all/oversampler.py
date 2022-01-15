from defects4all.data_statistics import get_testsuites_samples_count
from imblearn.over_sampling import RandomOverSampler 
import pandas as pd
import numpy


def get_sampling_strategy(df, value):
    samples_count = get_testsuites_samples_count(df)
    
    sampling_strategy={}
    for sample,count in samples_count.items():
        if count < value:
            sampling_strategy[sample]=value
    return sampling_strategy


# define dataset
def oversample_dataframe(df, value):
    
    #print("y =", numpy.shape(data.test_suite))
    #print("X =", numpy.shape(data.sequence.values.reshape(-1,1)))
    samples_count = get_testsuites_samples_count(df)
    
    sampling_strategy={}
    for sample,count in samples_count.items():
        if count < value:
            sampling_strategy[sample]=value

    y = df.test_suite.values
    X = df.klogs_words.values.reshape(-1,1)
    #print(data.sequence)
    #print(X)
    oversample = RandomOverSampler(sampling_strategy=sampling_strategy)
    X_over, y_over = oversample.fit_resample(X, y)
    X_over = numpy.reshape(X_over, -1)
    #print(X_over)
    #print(numpy.shape(y_over))
    #print(numpy.shape(y))
    #print(y_over)
    frame = {"test_suite": y_over, "klogs_words": X_over} 
    #print(frame)
    data_over = pd.DataFrame(frame)
    return data_over 

#oversample_file("./tests/data/dataset_stats/klog_overlap_sentence_overlap.klog")

