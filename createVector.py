max_num_lines=0
import os
train_directory = "./parsed_logs/issue1/train/"
test_directory = "./parsed_logs/issue1/test/"


def create_vector_representation(dir):
    for filename in os.listdir(dir):
        vec_lines = []
        i=0
        if filename.endswith(".log"):
            with open(dir  + filename) as f:
                lines = f.readlines()
            for line in lines:
                vec_lines.append(line.split('[')[0])
                i = i + 1
            out_dir = dir + "result"
            if not os.path.exists(out_dir):
                os.mkdir(out_dir)
            vec_path = out_dir +"/" + filename + ".vec"
            with open(vec_path, "a+") as f:
                for item in vec_lines:
                    if item != "None":
                        f.write(item + "\n")


create_vector_representation(train_directory)
create_vector_representation(test_directory)
