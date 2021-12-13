import os
from pathlib import Path

def create_raw_vector_representation(dir):
    for filename in os.listdir(dir):
        vec_lines = []
        i=0
        if filename.endswith(".log") or filename.endswith(".res"):
            with open(dir  + filename) as f:
                lines = f.readlines()
            for line in lines:
                vec_lines.append(line.split('[')[0])
                i = i + 1
            out_dir = dir + "sequence"
            if not os.path.exists(out_dir):
                os.mkdir(out_dir)
            vec_path = out_dir +"/ut_raw_log_as_sentence.vec"
            with open(vec_path, "a+") as f:
                f.write(label + " ")
                for item in vec_lines:
                    if item != "None":
                        f.write(item + " ")
                f.write("\n")

def getFileName(filename, level):
    if level == "TestSuite":
        return (filename.split(".")[0]).split('_')[0]
    else:
         return filename.split(".")[0]

def create_fasttext_sequence_representation(directory,level):
    print("create_fasttext_sequence_representation")
    out_dir = directory + "/sequence"
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    vec_path = out_dir +"/ut_log_as_sentence.vec"
    out_file =  open(vec_path, "w")
    for filename in Path(directory).glob("*.drain"):
        vec_lines = []
        i=0
        print("sequencing ", filename)
        with open(filename) as f:
            lines = f.readlines()
        for line in lines:
            vec_lines.append(line.split('[')[0])
            i = i + 1
        label = "__label__" + getFileName(filename.name,level)
        out_file.write(label + " ")
        for item in vec_lines:
            if item != "None":
                out_file.write(item + " ")
        out_file.write("\n")
    out_file.close()
    return vec_path


