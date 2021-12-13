import subprocess
from pathlib import Path
class FastTextValidator:

    def __init__(self, fasttext_dir, model_file, in_file):
        self.filename = in_file
        self.model_file = model_file 
        self.fasttext_dir = fasttext_dir

    def validate(self):
        print("validate ", self.filename)
        subprocess.call("%s/fasttext test %s %s" %(self.fasttext_dir, self.model_file, self.filename), shell=True)
