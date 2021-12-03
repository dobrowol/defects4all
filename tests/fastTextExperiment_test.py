from defects4all.FastTextTrainer import FastTextTrainer
from defects4all.FastTextPredictor import FastTextPredictor
import configparser
import pytest
import os

@pytest.fixture
def fast_text_dir():
    config = configparser.ConfigParser()
    config.sections()
    config.read('defects4all.ini')
    return config['DEFAULT']['FASTTEXT_DIR']


def test_if_model_is_created_during_training(fast_text_dir):
    model_file_check = "./tests/data/fastText/klog3/klog_model.bin"
    if os.path.isfile(model_file_check):
        os.remove(model_file_check)
    in_dir = "./tests/data/fastText/"
    klog_size=3
    fastTextTrainer = FastTextTrainer(fast_text_dir, in_dir, klog_size)
    model_file = fastTextTrainer.train()
    assert(os.path.isfile(model_file_check))

def test_if_prediction_file_created_during_training(fast_text_dir):
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

