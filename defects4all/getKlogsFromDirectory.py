import configparser
import re
from pathlib import Path

def getKlogsFromDirectory(in_dir):
    klogs = {}
    for path in Path(in_dir).rglob('*.klog'):
        pattern = r"klog(\d+)/sentence(\d+)"
        res = re.search(pattern, str(path))
        if res == None:
            pattern = r"klog(\d+)"
            res = re.search(pattern, str(path))
            klogs[res[1]] = [str(path)] 
        else:
            klogs[res[1], res[2]] = [str(path)]
    return klogs
#print(getKlogsFromDirectory("./klogs"))

    
