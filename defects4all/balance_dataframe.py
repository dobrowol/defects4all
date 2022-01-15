from defects4all.oversampler import oversample_dataframe
from defects4all.undersampler import undersample_dataframe
from defects4all.data_statistics import describe_samples

def balance_dataframe(df):
    data_stats = describe_samples(df)
    oversample_to = int((10*data_stats.max())//100)
    undersample_to = int((50*data_stats.max())//100)
    if oversample_to < 1:
        oversample_to=1
    if undersample_to<1:
        undersample_to=1
    print("oversample to ", oversample_to)
    print("undersample to ", undersample_to)
    oversampled_df = oversample_dataframe(df, oversample_to)
    balanced_df = undersample_dataframe(oversampled_df, undersample_to)
    return balanced_df
    
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
from defects4all.data_statistics import describe_samples
from defects4all.oversampler import get_sampling_strategy as oversampler_strategy
from defects4all.undersampler import get_sampling_strategy as undersampler_strategy
from imblearn.over_sampling import RandomOverSampler 
from imblearn.under_sampling import RandomUnderSampler 


def balance_series(X_train, y_train):
    data_stats = describe_samples (pd.DataFrame({"klogs_words":X_train, "test_suite":y_train}))
    oversample_to = int((10*data_stats.max())//100)
    undersample_to = int((50*data_stats.max())//100)
    oversampling_strategy=oversampler_strategy(pd.DataFrame({"klogs_words":X_train, "test_suite":y_train}), oversample_to)
    undersampling_strategy=undersampler_strategy(pd.DataFrame({"klogs_words":X_train, "test_suite":y_train}), undersample_to)
    X_train_res, y_train_res = RandomOverSampler(sampling_strategy=oversampling_strategy).fit_resample(X_train.values.reshape(-1, 1), y_train)
    X_train_bal, y_train_bal = RandomUnderSampler(sampling_strategy=undersampling_strategy).fit_resample(X_train_res, y_train_res)
    X_train_bal = np.reshape(X_train_bal, -1)
    return X_train_bal, y_train_bal


