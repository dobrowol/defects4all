import re
from defects4all.string_to_cluster import get_cluster_position

def find_all_similar_blocks2(sequence, subsequences):
    similar_block_at_line = {}
    from tqdm import tqdm
    for subsequence in tqdm(subsequences):
        subseq_split = subsequence.split()
        subseq_id = subseq_split[0]
        subs_list = subseq_split[1:]
        len_subs_list = len(subs_list)
        index_matches = {}
        i = 0
        split_seq = sequence.split()
        for i in tqdm(range((len(subs_list)))):
            start = None
            for j in range(len(split_seq)):
                if split_seq[j]==subs_list[i]:
                    if start is None:
                        start = j
                elif start is not None:
                    index_matches[start]=j-1
                    start = None
        for ind in index_matches:
            if ind in similar_block_at_line:
                if similar_block_at_line[ind][1]<index_matches[ind]:
                    similar_block_at_line[ind]=[subseq_id, index_matches[ind]]
            else:
                similar_block_at_line[ind]=[subseq_id, index_matches[ind]]
                
    return similar_block_at_line 
            





def find_all_similar_blocks(sequence, subsequences):
    similar_block_at_line = {}
    from tqdm import tqdm
    for subsequence in tqdm(subsequences):
        subseq_split = subsequence.split()
        subseq_id = subseq_split[0]
        subs_list = subseq_split[1:]
        len_subs_list = len(subs_list)
        index_matches = {}
        i = 0
        split_seq = sequence.split()
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
