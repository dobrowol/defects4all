from defects4all.trainingValidatingSplit import splitToTrainingAndValidatingSet
from defects4all.splitTrainingAndTesting import count_lines 

def test_should_split_100_to_desired_sized():
    whole_file = "./tests/data/splitting/100_lines.txt"
    out_dir = "./tests/out/splitting"
    percentage = 0.8
    training, testing = splitToTrainingAndValidatingSet(whole_file, out_dir, percentage)
    assert(count_lines(training) == 80)
