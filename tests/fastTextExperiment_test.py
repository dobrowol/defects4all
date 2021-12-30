from defects4all.FastTextTrainer import FastTextTrainer
from defects4all.FastTextPredictor import FastTextPredictor
from defects4all.trainingValidatingSplit import splitToTrainingAndValidatingSet
import configparser
import pytest
import os

@pytest.fixture
def fast_text_dir():
    config = configparser.ConfigParser()
    config.sections()
    config.read('defects4all.ini')
    return config['DEFAULT']['FASTTEXT_DIR']


def if_model_is_created_during_training(fast_text_dir):
    model_file_check = "./tests/out/fastText/klog3/klog_model_klog_overlap_sentence_nooverlap.bin"
    RESULT_DIR = "./tests/out/fastText"
    if os.path.isfile(model_file_check):
        os.remove(model_file_check)
    in_file = "./tests/data/fastText/klog3/klog_overlap_sentence_nooverlap.klog"
    training_file, validating_file =splitToTrainingAndValidatingSet(in_file, RESULT_DIR, 0.8)
    fastTextTrainer = FastTextTrainer(fast_text_dir, training_file)
    model_file = fastTextTrainer.train()
    assert(os.path.isfile(model_file_check))

def if_prediction_file_created_during_training(fast_text_dir):
    prediction_file_check = "./tests/data/fastText/runtime/klog3/sentence5/predictions_NR_rmod1_1runtime_DEFAULT.pred"
    model_file = "./tests/data/fastText/klog3/klog_model.bin"
    if os.path.isfile(prediction_file_check):
        os.remove(prediction_file_check)
    in_dir = "./tests/data/fastText/runtime/"
    klog_size=3
    sentence_size=5
    fastTextPredictor = FastTextPredictor(fast_text_dir, in_dir, klog_size, sentence_size, model_file)
    fastTextPredictor.predict()
    assert(os.path.isfile(prediction_file_check))

