class Klog:
    def __init__(self, klog_size, klog_overlap, sentence_size=0, sentence_overlap=False):
        self.klog_size=klog_size
        self.klog_overlap=klog_overlap
        self.sentence_size=sentence_size
        self.sentence_overlap=sentence_overlap

    def createKlogsFromSequence(self, sequence):
        tokens = sequence.split(' ')
        kmer = ""
        if len(tokens) - self.klog_size <= 0:
            for token in tokens:
                kmer += token+"t"
    
        i = 1
        while i <len(tokens) - self.klog_size:
            k = ""
            for j in range(self.klog_size):
                k += tokens[i+j]+"t"
            if self.klog_overlap:
                i += 1
            else:
                i += self.klog_size
            kmer += k + ' '
        return kmer
    
    def prepare_klog_file(self, train, in_file, out_dir):
        if self.klog_overlap:
            ko = "klog_overlap"
        else:
            ko = "klog_nooverlap"
    
        if self.sentence_overlap:
            so = "sentence_overlap"
        else:
            so = "sentence_nooverlap"
    
        out_file = out_dir + "/"+ko + "_" + so+".klog"
        with open(in_file) as f:
            lines = f.read().splitlines()
            i = 0
            klogs = {}
            for line in lines:
                klogs[line.split()[0]] = self.createKlogsFromSequence(line)
            with open(out_file, 'a') as out_f:
                for label,klog in klogs.items():
                    klog_split = klog.split()
                    i = 0
                    while i < len(klog_split) - self.sentence_size:
                        if train:
                            out_f.write(label +" ")
                            print("write label ", label)
                        for j in range(i,i+self.sentence_size):
                            out_f.write(klog_split[j] +" ")
                        out_f.write("\n")
                        if self.sentence_overlap:
                            i += 1
                        else:
                            i += self.sentence_size
        print ("created ", out_file)
        return out_file
