from pathlib import Path
import os
class Klog:
    def __init__(self, in_file, out_dir):
        self.in_file=in_file
        self.out_dir=out_dir

    def _createKlogsFromSequence(self, sequence):
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
    
    def prepare_klog_file(self, phase, klog_size, sentence_size, klog_overlap, sentence_overlap):
        self.klog_size = klog_size
        self.klog_overlap = klog_overlap
        self.sentence_overlap = sentence_overlap
        self.sentence_size = sentence_size
        self.out_dir = self._get_out_dir(self.out_dir, klog_size, sentence_size)
        self.line_creator = self._get_line_creator(phase, sentence_size)
        self.out_file_prefix =  self._get_out_file_prefix(klog_overlap, sentence_overlap)
        klogs_printer = self._get_klogs_printer(sentence_size)
        with open(self.in_file) as f:
            lines = f.read().splitlines()
            i = 0
            klogs = {}
            for line in lines:
                klogs[line.split()[0]] = self._createKlogsFromSequence(line.split()[1:])
            return klogs_printer(self.out_file_prefix, klogs)
    
    def _get_out_dir(self, out_dir, klog_size, sentence_size):
        if klog_size <= 0:
            raise ValueError
        if sentence_size>0:
            od = out_dir +"/klog"+str(klog_size)+"/sentence"+str(sentence_size)
        else:
            od = out_dir +"/klog"+str(klog_size)
        Path(od).mkdir(parents=True, exist_ok=True)
        return od

    def _get_line_creator(self, phase, sentence_size):
        if sentence_size == 0:
            if phase == "training":
                return self._training_line_create
            elif phase == "testing":
                return self._testing_line_create
            else:
                raise ValueError
        else:
            if phase == "training":
                return self._training_sentence_line_create
            elif phase == "testing":
                return self._testing_sentence_line_create
            else:
                raise ValueError

    
    def _training_sentence_line_create(self, out_file, label, klog_split, i):
        out_file.write(label + " ")
        self._testing_sentence_line_create(out_file, label, klog_split, i)
        
    def _testing_sentence_line_create(self, out_file, label, klog_split, i):
        line = ""
        for j in range(i,i+self.sentence_size):
            line += klog_split[j] +" "
        out_file.write(line.rstrip()+"\n")
    
    def _training_line_create(self, out_file, label, klog):
        out_file.write(label + " ")
        self._testing_line_create(out_file, label, klog)
        
    def _testing_line_create(self, out_file, label, klog):
        line = ""
        for k in klog.split():
            line += k + " "
        out_file.write(line.rstrip()+"\n")
    
    def _get_out_file_prefix(self, klog_overlap, sentence_overlap):
        if klog_overlap:
            ko = "klog_overlap"
        else:
            ko = "klog_nooverlap"
    
        if sentence_overlap:
            so = "sentence_overlap"
        else:
            so = "sentence_nooverlap"
    
        return self.out_dir + "/"+ko + "_" + so

    def _get_klogs_printer(self, sentence_size):
        if self.sentence_size == 0:
            return self._print_klogs
        else:
            return self._print_sentences_of_klogs

    def _print_klogs(self, out_file, klogs):
        out_file = out_file+".klog"
        if os.path.isfile(out_file):
            pass
        with open(out_file, 'w') as out_f:
            for label,klog in klogs.items():
                self.line_creator(out_f, label, klog)
        return [out_file]
    
    def _print_sentences_of_klogs(self, out_file, klogs):
        out_files = []
        for label,klog in klogs.items():
            label_wo_label = label.split("__label__")[1]
            res_file = out_file+"_"+label_wo_label+".klog"
            out_files.append(res_file)
            if os.path.isfile(out_file+"_"+label_wo_label+".klog"):
                continue
            with open(out_file+"_"+label_wo_label+".klog", 'w') as out_f:
                i = 0
                klog_split = klog.split()
                while i < len(klog_split)-self.sentence_size:
                    self.line_creator(out_f, label, klog_split, i)
                    if self.sentence_overlap:
                        i += 1
                    else:
                        i += self.sentence_size
        return out_files
