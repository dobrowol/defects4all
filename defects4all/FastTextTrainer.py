import subprocess
from pathlib import Path
class FastTextTrainer:

    def __init__(self, fasttext_dir, in_file):
        specific_train_in_dir = str(Path(in_file).parent)
        self.filename = in_file
        file_no_ext = Path(in_file).stem
        self.model_file = specific_train_in_dir+"/klog_model_"+file_no_ext
        self.fasttext_dir = fasttext_dir

    def train(self):
        subprocess.call("%s/fasttext supervised -input %s -output %s" %(self.fasttext_dir, self.filename, self.model_file), shell=True)
        return self.model_file+".bin"

