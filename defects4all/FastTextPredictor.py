import subprocess
import glob

class FastTextPredictor:

    def __init__(self, fasttext_dir, in_dir, klog_size, sentence_size, model_file):
        self.specific_in_dir = in_dir +"/klog"+str(klog_size)+"/sentence"+str(sentence_size)
        self.file_pattern = self.specific_in_dir+"/klog_overlap_sentence_nooverlap*.klog"
        self.model_file = model_file
        self.fasttext_dir = fasttext_dir

    def get_filename(self,klog_name):
        p = klog_name.split('/')[-1]
        k = p.split('.')[0]
        r = k.split("klog_overlap_sentence_nooverlap_")[1]
        return r

    def predict(self):
        for klog_name in glob.glob(self.file_pattern):
            runtime_name = self.get_filename(klog_name)
            predictions_file = "/predictions_%s.pred"%(runtime_name)
            subprocess.call("%s/fasttext predict %s %s > %s" %(self.fasttext_dir, self.model_file, klog_name, self.specific_in_dir+predictions_file), shell=True)
