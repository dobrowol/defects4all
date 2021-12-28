from defects4all.data_statistics import get_testsuites_samples_count
from imblearn.under_sampling import RandomUnderSampler 
import pandas as pd
import numpy

# define dataset
def undersample_dataframe(df, value):
    
    #print("y =", numpy.shape(data.test_suite))
    #print("X =", numpy.shape(data.sequence.values.reshape(-1,1)))
    samples_count = get_testsuites_samples_count(df)
    
    sampling_strategy={}
    for sample,count in samples_count.items():
        if count > value:
            sampling_strategy[sample]=value

    y = df.test_suite.values
    X = df.klogs_words.values.reshape(-1,1)
    #print(data.sequence)
    #print(X)
    undersample = RandomUnderSampler(sampling_strategy=sampling_strategy)
    X_under, y_under = undersample.fit_resample(X, y)
    X_under = numpy.reshape(X_under, -1)
    #print(X_under)
    #print(numpy.shape(y_under))
    #print(numpy.shape(y))
    #print(y_under)
    frame = {"test_suite": y_under, "klogs_words": X_under} 
    #print(frame)
    data_under = pd.DataFrame(frame)
    return data_under 

#undersample_file("./tests/data/dataset_stats/klog_underlap_sentence_underlap.klog")

