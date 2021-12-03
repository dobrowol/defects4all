import subprocess
class FastTextTrainer:

    def __init__(self, fasttext_dir, in_dir, klog_size):
        specific_train_in_dir = in_dir +"/klog"+str(klog_size)
        self.filename = specific_train_in_dir+"/klog_overlap_sentence_nooverlap.klog"
        self.model_file = specific_train_in_dir+"/klog_model"
        self.fasttext_dir = fasttext_dir

    def train(self):
        subprocess.call("%s/fasttext supervised -input %s -output %s" %(self.fasttext_dir, self.filename, self.model_file), shell=True)
        return self.model_file+".bin"

