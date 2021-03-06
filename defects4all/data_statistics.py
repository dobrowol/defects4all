import pandas as pd
from pathlib import Path

def klogs_present_in_one_testsuite(df):
    return df.groupby('klogs_words', as_index=False).filter(lambda x: x["test_suite"].nunique() == 1)["test_suite"].value_counts()

import statistics
def get_klogs_average_length(df):
    return statistics.mean(df["klogs_words"].apply(len))

def get_klogs_median_length(df):
    return statistics.median(df["klogs_words"].apply(len))

def klogs_and_coresponding_testsuites(df):
    return df.groupby("klogs_words")["test_suite"].nunique().reset_index(name='nunique').sort_values(['nunique'], ascending=False)

def get_testsuites_names(df):
    g = df.groupby("test_suite")
    return g.groups.keys()

def get_testsuites_samples(df):
    return df.groupby("test_suite")["klogs_words"].value_counts()

def get_testsuites_samples_count(df):
    return df.groupby("test_suite")["klogs_words"].size()

def get_testnames_for_klogs_appeared_once(df, out_dir, in_file):
    out_grouped_testsuite_file = out_dir/(str(in_file)+"_testsuite_by_words.csv")
    out_count_1_grouped_testsuite = out_dir/(str(in_file)+"_count_1_testsuite.csv")
    out_testsuite_words_count_1_file = out_dir/(str(in_file)+"_testsuite_by_words_with_count_1.csv")
    grouped_by_klogs_and_test_suite = df.groupby('klogs_words').filter(lambda x: x["klogs_words"].count()==1)
    res = grouped_by_klogs_and_test_suite.groupby("test_suite")["klogs_words"].nunique()
    tests_with_words_of_count_one = grouped_by_klogs_and_test_suite.groupby("test_suite")["klogs_words"].nunique()
    print(res)
    #for key, item in res:
    #    print(res.get_group(key), "\n\n")
    grouped_by_klogs_and_test_suite.to_csv(out_grouped_testsuite_file, index=False, header=True)
    tests_with_words_of_count_one.to_csv(out_testsuite_words_count_1_file, index=True, header=True)
 
def get_testnames_for_klogs_appeared_max(df, out_dir, in_file):
    out_grouped_testsuite_file = out_dir/(str(in_file)+"_testsuite_by_words.csv")
    out_testsuite_words_count_max = out_dir/(str(in_file)+"_testsuite_by_words_with_count_max.csv")
    unique_tests_for_klogs = df.groupby('klogs_words')["test_suite"].nunique()
    print(df.loc[df.groupby('klogs_words').filter(lambda x: any(x["test_suite"].nunique() == unique_tests_for_klogs["test_suite"].max()))])
    #print(df.loc[df.groupby('klogs_words').filter(lambda x: x["klogs_words"].nunique() == 3)])
    #print(df.loc[df.groupby('klogs_words')["test_suite"].nunique().max()==df.groupby('klogs_words')["test_suite"].nunique()])
    #df.groupby('klogs').agg({'c_a':'nunique'
    #tests_with_words_of_count_max = grouped_by_klogs_and_test_suite.groupby("test_suite")["klogs_words"].nunique()
    #for key, item in grouped_by_klogs_and_test_suite:
    #    print(grouped_by_klogs_and_test_suite.get_group(key), "\n\n")
    #grouped_by_klogs_and_test_suite.to_csv(out_grouped_testsuite_file, index=False, header=True)
    #tests_with_words_of_count_max.to_csv(out_testsuite_words_count_max, index=True, header=True)
 
def create_out_dir(output_dir, input_dir):
    sub_dirs = str(input_dir).split('/')
    out_dir = Path(output_dir)/sub_dirs[-3]/sub_dirs[-2] 
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir

def create_sentence_out_dir(output_dir, input_dir):
    sub_dirs = str(input_dir).split('/')
    out_dir = Path(output_dir)/sub_dirs[-3]/sub_dirs[-2]/sub_dirs[-1] 
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir

def describe_samples(df):
    return df.groupby("test_suite")["klogs_words"].size().describe()
    
def describe_words(input_dir, output_dir):
    for path in Path(input_dir).rglob('klog*/sentence1/*.klog'):
        print("word statistics for ", path)
        out_dir = create_out_dir(output_dir, path.parent)
        out_file = out_dir/(str(path.stem)+"words.csv")
        out_grouped_file = out_dir/(str(path.stem)+"_words_by_testsuite.csv")
        out_file_testuite_with_unique_words= out_dir/(str(path.stem)+"_testsuites_with_unique_words.csv")

        df = pd.read_csv(path, sep='\t',names= ["test_suite", "klogs_words"])

        df.klogs_words.value_counts().to_csv(out_file, index=True, header=True)
        res = klogs_and_coresponding_testsuites(df) 
        res.to_csv(out_grouped_file, index=True, header=True)
        res = klogs_present_in_one_testsuite(df)
        res.to_csv(out_file_testuite_with_unique_words, index=True, header=True)
        #get_testnames_for_klogs_appeared_once(df, out_dir, path.stem)
        #get_testnames_for_klogs_appeared_max(df, out_dir, path.stem)
       #print(res)
   
def describe_sentence(input_dir, output_dir):
    for path in Path(input_dir).rglob('*.klog'):
        print(path)
        out_dir = create_sentence_out_dir(output_dir, path.parent)
        out_file = out_dir/(str(path.stem)+".csv")
        out_agg_file = out_dir/(str(path.stem)+"_agg.csv")
        #for line in f.readlines():
        #    print(line)
        #    klogs = line.split('\t')[1]
        #    klogs_list["klogs"].extend(klogs.split())
        df = pd.read_csv(path, sep='\t',names=["test_suite", "klogs_words"])
        
        out_grouped_file = out_dir/(str(path.stem)+"_words_by_testsuite.csv")
        out_file_testuite_with_unique_words= out_dir/(str(path.stem)+"_testsuites_with_unique_words.csv")
        #res = df.groupby("test_suite")["klogs_words"].nunique()
        #res.to_csv(out_grouped_file, index=True, header=True)
        #print ("balance of df ", out_file)
        #print ("aggregate of df ", out_agg_file)
        #df = pd.read_csv(path, sep='\t')
        #pd.df.iloc[:, 2]
        df.test_suite.value_counts().to_csv(out_file, index=True, header=True)
        df.test_suite.value_counts().agg(['min', 'max', 'mean', 'median']).to_csv(out_agg_file, index=True, header=True)
        res = klogs_and_coresponding_testsuites(df) 
        res.to_csv(out_grouped_file, index=True, header=True)
        res = klogs_present_in_one_testsuite(df)
        res.to_csv(out_file_testuite_with_unique_words, index=True, header=True)
        #get_testnames_for_klogs_appeared_once(df, out_dir, path.stem)

#describe_sentence("./tests/data/sentence_stats", "./tests/out/sentence_stats")
