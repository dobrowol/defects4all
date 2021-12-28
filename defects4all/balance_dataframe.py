from defects4all.oversampler import oversample_dataframe
from defects4all.undersampler import undersample_dataframe
from defects4all.data_statistics import describe_samples

def balance_dataframe(df):
    data_stats = describe_samples(df)
    oversample_to = int((10*data_stats.max())//100)
    undersample_to = int((50*data_stats.max())//100)
    print("oversample to ", oversample_to)
    print("undersample to ", undersample_to)
    oversampled_df = oversample_dataframe(df, oversample_to)
    balanced_df = undersample_dataframe(oversampled_df, undersample_to)
    return balanced_df
    
    
