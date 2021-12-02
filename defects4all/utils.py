def get_runtime_file_name_from_klog_file(klog_file_name):
    filename = klog_file_name.split('/')[-1]
    filename_no_ext = filename.split('.')[0]
    runtime_name = filename_no_ext.split("_")[-1]
    return runtime_name


