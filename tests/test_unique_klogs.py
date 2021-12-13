from defects4all.unique_klogs import remove_duplicated_lines

def test_keep_unique_lines():
    with open("./tests/data/unique_klogs/basic.klog", "w") as f:
        f.write("1\n")
        f.write("2\n")
        f.write("3\n")
        f.write("2\n")
        f.write("3\n")
        f.write("4\n")
        f.write("4\n")
        f.write("2\n")
        f.write("1\n")
    remove_duplicated_lines("./tests/data/unique_klogs") 
    with open("./tests/data/unique_klogs/basic.klog") as f:
        lines = f.readlines()
    assert(lines[0] == "1\n")
    assert(lines[1] == "2\n")
    assert(lines[2] == "3\n")
    assert(lines[3] == "4\n")
