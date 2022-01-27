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
from drain3.template_miner_config import TemplateMinerConfig
from pathlib import Path

def infering_file(in_log_file, config_file, persistent_file):
        
    in_log_dir = Path(in_log_file).parent
    config = TemplateMinerConfig()
    config.load(config_file)
    config.profiling_enabled = False

    from drain3.file_persistence import FilePersistence

    persistence = FilePersistence(str(persistent_file))

    template_miner = TemplateMiner(persistence, config=config)
    
    if(in_log_file == "result"):
        return

    print("infering file ", in_log_file)
    with open(in_log_file, errors='replace') as f:
        lines = f.readlines()
    
    start_time = time.time()
    batch_start_time = start_time
    batch_size = 10000
    out_dir = in_log_dir
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    out_file = out_dir/(Path(in_log_file).stem + ".drain")
    with open(out_file, 'w+') as out_log_file:
        for line in lines:
            line = line.rstrip()
            if len(line) == 0:
                    continue
            cluster,_ = template_miner.match(line)
            if cluster is None:
                print("not found cluster for", line)
            if cluster is not None:
                out_log_file.write(str(cluster.cluster_id)+' ')
        
    time_took = time.time() - start_time
    #logger.info(f"--- Done processing file in {time_took:.2f} sec. Total of {line_count} lines, rate {rate:.1f} lines/sec, "
    #            f"{len(template_miner.drain.clusters)} clusters")
    
    sorted_clusters = sorted(template_miner.drain.clusters, key=lambda it: it.size, reverse=True)
    with open(out_dir/"clusters", 'w+') as out_cluster:
        for cluster in sorted_clusters:
            out_cluster.write(str(cluster)+'\n')

#template_miner.drain.print_tree()

#template_miner.profiler.report(0)

