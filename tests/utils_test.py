from defects4all.utils import get_runtime_file_name_from_klog_file

def test_get_name():
    filename = "/dir/second_dir/file_name_runtime.txt"
    assert("runtime" == get_runtime_file_name_from_klog_file(filename))
