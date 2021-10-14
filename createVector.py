max_num_lines=0
import os
max_file =""
for filename in os.listdir("."):
    if filename.endswith(".log"):
        num_lines = sum(1 for line in open(filename))
        if num_lines > max_num_lines:
            max_num_lines = num_lines
            max_file = filename

print(max_num_lines, " ", max_file)

for filename in os.listdir("."):
    vec_lines = ["0"] * max_num_lines
    i=0
    if filename.endswith(".log"):
        with open(filename) as f:
            lines = f.readlines()
        for line in lines:
            vec_lines[i] = line.split('[')[0] 
            i = i + 1
        out_dir = "result"
        if not os.path.exists("result"):
            os.mkdir(out_dir)
        vec_path = out_dir +"/" + filename + ".vec"
        with open(vec_path, "a+") as f:
            for item in vec_lines:
                f.write(item + "\n")

