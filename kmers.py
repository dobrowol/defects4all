
def createKmersAndStuff(sequences, kmer_size):
    kmers = []
    kmer_vocab = {}
    index = 0;
    kmers_in_line = {}
    for sequence in sequences:
        tokens = sequence.split()
        kmer = ""
        kmer_in_line = {}
        if len(tokens) - kmer_size <= 0:
            for token in tokens:
                kmer += token+"t"
            if kmer not in kmer_in_line:
                kmer_in_line[kmer] = 1
            else:
                kmer_in_line[kmer] += 1

        for i in range(len(tokens) - kmer_size):
            k = ""
            for j in range(kmer_size):
                k += tokens[i+j]+"t"
            if k not in kmer_in_line:
                kmer_in_line[k] = 1
            else:
                kmer_in_line[k] += 1
            kmer += k + ' '
        kmers.append(kmer)
        for km, _ in kmer_in_line.items():
            if km not in kmer_vocab:
                kmer_vocab[km] = 1
            else:
                kmer_vocab[km] += 1
        kmers_in_line[index] = kmer_in_line
        index += 1

    return kmers, kmer_vocab, kmers_in_line


def createKmersFromSequence(sequence, kmer_size):
    tokens = sequence.split(' ')
    kmer = ""
    if len(tokens) - kmer_size <= 0:
        for token in tokens:
            kmer += token+"t"

    for i in range(len(tokens) - kmer_size):
        k = ""
        for j in range(kmer_size):
            k += tokens[i+j]+"t"
        kmer += k + ' '
    return kmer


def createKmers(sequences, kmer_size):
    kmers = []
    index = 0;
    for sequence in sequences:
        kmers.append(createKmersFromSequence(sequence, kmer_size)) 
    return kmers
