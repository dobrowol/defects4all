import re
from defects4all.string_to_cluster import get_cluster_position

def find_all_similar_blocks(sequence, subsequences):
    similar_block_at_line = {}
    for subsequence in subsequences:
        subseq_split = subsequence.split()
        subseq_id = subseq_split[0]
        subs_list = subseq_split[1:]
        len_subs_list = len(subs_list)
        index_matches = {}
        i = 0
        while i <(len(subs_list)):
            pattern_string = ""
            index_matches[i] = []
            for j in range(i, len_subs_list):
                pattern_string += r" %s"%(subs_list[j])
                pattern_string = pattern_string.lstrip()
                pattern = re.compile(pattern_string)
                matched = [m.start() for m in re.finditer(pattern, sequence)]
                if len(matched)==0:
                    break
                index_matches[i]=matched
            size = j - i
            ratio = size/len_subs_list
            for m in index_matches[i]:
                pos = get_cluster_position(sequence, m)
                if pos in similar_block_at_line:
                    if similar_block_at_line[pos][1]<ratio:
                        for k in range(size):
                            similar_block_at_line[pos+k]=[subseq_id, ratio]
                else:
                    for k in range(size):
                        similar_block_at_line[pos+k]=[subseq_id, ratio]
            i+=1
    return similar_block_at_line 
