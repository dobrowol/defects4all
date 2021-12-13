import subprocess
from pathlib import Path

def remove_duplicated_lines(dir_name):
    for path in Path(dir_name).rglob('*.klog'):
    #proc = Popen("", shell=True,
    #         stdin=None, stdout=None, stderr=None, close_fds=True)
        temp_file = str(path)+".tmp"
        subprocess.call("awk '!seen[$0]++'  %s > %s" %(str(path), str(temp_file)), shell=True)
        subprocess.call("mv %s %s" %(str(temp_file), str(path)), shell=True)
        print(path)
