import difflib
from operator import itemgetter

def find_similar_sequences(sequence, subsequences):
    similarities_at_line = {}
    lenSeq = len(sequence)

    lenSeqStart = len(sequence.split(' ')[0])# skip the __label_name

    lenLines = len(subsequences)
    i = 0
    from tqdm import tqdm
    for line in tqdm(subsequences):
        i += 1
        lenLine = len(line.split())
        subsequence_id = line.split(' ')[0]
        lenLineStart = len(subsequence_id)
        temp = difflib.SequenceMatcher(None,sequence.split()[1:],line.split()[1:])#skip the __label__name
        #m = temp.find_longest_match(lenSeqStart, lenSeq, lenLineStart, lenLine)
        m = temp.get_matching_blocks()
        for match_seq in m:
            ratio = match_seq.size/(lenLine)
        #print (ratio)
            if ratio > 0.02:
                if match_seq.a not in similarities_at_line:
                    similarities_at_line[match_seq.a] = []
                similarities_at_line[match_seq.a].append([subsequence_id, ratio, match_seq])
            #print("adding subsequence ", subsequence_id, " with similarity ", similarity)
    for key, value in similarities_at_line.items():
        similarities_at_line[key] = (sorted(value, key=itemgetter(1),reverse=True))[:3]
    return similarities_at_line 


