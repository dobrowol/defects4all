class Klog:
    def __init__(self, klog_size, klog_overlap, sentence_size=0, sentence_overlap=False):
        self.klog_size=klog_size
        self.klog_overlap=klog_overlap
        self.sentence_size=sentence_size
        self.sentence_overlap=sentence_overlap

    def createKlogsFromSequence(self, sequence):
        klog = ""
        if len(sequence) - self.klog_size <= 0:
            for token in sequence:
                klog += token+"t"
    
        increment = 1
        if not self.klog_overlap:
            increment = self.klog_size

        i = 0 
        while i <=len(sequence) - self.klog_size:
            k = ""
            for j in range(self.klog_size):
                k += sequence[i+j]+"t"
            klog += k + ' '
            i += increment
        return klog.rstrip()
    
    def prepare_klog_file(self, train, in_file, out_dir):
        if self.klog_overlap:
            ko = "klog_overlap"
        else:
            ko = "klog_nooverlap"
    
        if self.sentence_overlap:
            so = "sentence_overlap"
        else:
            so = "sentence_nooverlap"
    
        out_file = out_dir + "/"+ko + "_" + so
        with open(in_file) as f:
            lines = f.read().splitlines()
            i = 0
            klogs = {}
            for line in lines:
                klogs[line.split()[0]] = self.createKlogsFromSequence(line.split()[1:])
            if self.sentence_size == 0:
                return self.print_klogs(out_file, klogs)
            else:
                return self.print_sentences_of_klogs(out_file, klogs, train)
    
    def print_klogs(self, out_file, klogs):
        out_file = out_file+".klog"
        with open(out_file, 'w') as out_f:
            for label,klog in klogs.items():
                out_f.write(label +" ")
                for k in klog.split(): 
                    out_f.write(k+" ")
                out_f.write("\n")
        return [out_file]
    
    def print_sentences_of_klogs(self, out_file, klogs, train):
        out_files = []
        for label,klog in klogs.items():
            label_wo_label = label.split("__label__")[1]
            res_file = out_file+"_"+label_wo_label+".klog"
            out_files.append(res_file)
            with open(out_file+"_"+label_wo_label+".klog", 'w') as out_f:
                i = 0
                klog_split = klog.split()
                while i < len(klog_split)-self.sentence_size:
                    if train:
                        out_f.write(label + " ")
                    for j in range(i,i+self.sentence_size):
                        out_f.write(klog_split[j] +" ")
                    out_f.write("\n")
                    if self.sentence_overlap:
                        i += 1
                    else:
                        i += self.sentence_size
        return out_files
