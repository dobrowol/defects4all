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
        print(m)
        for match_seq in m:
            ratio = match_seq.size/(lenLine)
        #print (ratio)
            for i in range(match_seq.a, match_seq.a+match_seq.size):
                if i in similarities_at_line:
                    if  match_seq.size > similarities_at_line[i][2]:
                        similarities_at_line[i] = [subsequence_id, ratio, match_seq.size]
                        print ("adding better subseq %s at position %d with ratio %f"%(subsequence_id, i, ratio))
                else:
                    print ("adding new subseq %s at position %d with ratio %f"%(subsequence_id, i, ratio))
                    similarities_at_line[i] = [subsequence_id, ratio, match_seq.size]

            #print("adding subsequence ", subsequence_id, " with similarity ", similarity)
    #for key, value in similarities_at_line.items():
    #    similarities_at_line[key] = (sorted(value, key=itemgetter(1),reverse=True))[:3]
    return similarities_at_line 
