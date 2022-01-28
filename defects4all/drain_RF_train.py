"""
Description : Example of using Drain3 to process a real world file
Author      : David Ohana
Author_email: david.ohana@ibm.com
License     : MIT
"""
import json
import logging
import os
import subprocess
import sys
import time
from os.path import dirname
from drain3 import TemplateMiner
from tqdm import tqdm
from pathlib import Path

def parsing_file(in_log_file, template_miner):
    
    line_count = 0
    
    if(in_log_file == "result"):
        return

    in_dir = Path(in_log_file).parents[0]
    with open(in_log_file) as f:
        lines = f.readlines()
    
    start_time = time.time()
    batch_start_time = start_time
    batch_size = 10000
    
    for line in lines:
        line = line.rstrip()
        if len(line) == 0:
            continue
        result = template_miner.add_log_message(line)
        line_count += 1
        if line_count % batch_size == 0:
            time_took = time.time() - batch_start_time
            rate = batch_size / time_took
            batch_start_time = time.time()
        if result["change_type"] != "none":
            result_json = json.dumps(result)
    
    
    sorted_clusters = sorted(template_miner.drain.clusters, key=lambda it: it.size, reverse=True)
    with open(Path(in_dir)/"clusters", 'w+') as out_cluster:
        out_cluster.write(in_log_file)
        for cluster in sorted_clusters:
            out_cluster.write(str(cluster)+'\n')
    time_took = time.time() - start_time
    rate = line_count / time_took
    #template_miner.drain.print_tree()

#template_miner.profiler.report(0)
