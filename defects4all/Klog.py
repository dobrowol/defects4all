from pathlib import Path
import os
class Klog:
    def __init__(self, in_file, out_dir):
        self.in_file=in_file
        self.out_dir=out_dir

    def prepare_klog_file(self, phase, klog_size, sentence_size, klog_overlap, sentence_overlap):
        self.klog_size = klog_size
        self.klog_overlap = klog_overlap
        self.sentence_increment = self._get_sentence_increment(sentence_overlap, sentence_size)
        self.sentence_size = sentence_size
        current_out_dir = self._get_out_dir(self.out_dir, klog_size, sentence_size)
        self.line_creator = self._get_line_creator(phase, sentence_size)
        self.out_file_prefix =  self._get_out_file_prefix(current_out_dir, klog_overlap, sentence_overlap)
        self.out_filename_constructor = self._get_out_filename_constructor(phase)
        klogs_printer = self._get_klogs_printer(sentence_size)
        with open(self.in_file) as f:
            print (self.in_file)
            lines = f.read().splitlines()
            i = 0
            klogs_labels = []
            klogs = []
            for line in lines:
                print(line)
                ks = self._createKlogsFromSequence(line.split()[1:])
                klogs_labels.append(line.split()[0])
                klogs.append(self._createKlogsFromSequence(line.split()[1:]))
        return klogs_printer(self.out_file_prefix, zip(klogs_labels, klogs))
    
    def _get_sentence_increment(self, sentence_overlap, sentence_size):
        if sentence_overlap:
            return 1
        else:
            return sentence_size

    def _createKlogsFromSequence(self, sequence):
        klog = ""
        if len(sequence) - self.klog_size < 0:
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
                return self._create_one_line_with_label
            elif phase == "testing":
                return self._create_one_line
            else:
                raise ValueError
        else:
            if phase == "training":
                return self._line_create_sentence_with_label
            elif phase == "testing":
                return self._line_create_sentence
            else:
                raise ValueError

    
    def _line_create_sentence_with_label(self, out_file, label, klog_split, i):
        print("create sentence with tab ", label)
        out_file.write(label + "\t")
        self._line_create_sentence(out_file, label, klog_split, i)
        
    def _line_create_sentence(self, out_file, label, klog_split, i):
        line = ""
        end = min(len(klog_split), i+self.sentence_size)
        for j in range(i,end):
            line += klog_split[j] +" "
        out_file.write(line.rstrip()+"\n")
    
    def _create_one_line_with_label(self, out_file, label, klog):
        out_file.write(label + "\t")
        self._create_one_line(out_file, label, klog)
        
    def _create_one_line(self, out_file, label, klog):
        line = ""
        for k in klog.split():
            line += k + " "
        out_file.write(line.rstrip()+"\n")
    
    def _get_out_file_prefix(self, out_dir, klog_overlap, sentence_overlap):
        if klog_overlap:
            ko = "klog_overlap"
        else:
            ko = "klog_nooverlap"
    
        if sentence_overlap:
            so = "sentence_overlap"
        else:
            so = "sentence_nooverlap"
    
        return out_dir + "/"+ko + "_" + so

    def _get_klogs_printer(self, sentence_size):
        if sentence_size == 0:
            return self._print_one_liner_klogs
        else:
            return self._print_sentence_klogs

    def _get_out_filename_constructor(self, phase):
        if phase == "training":
            return self._construct_training_out_filename
        elif phase == "testing":
            return self._construct_testing_out_filename

    def _construct_training_out_filename(self, out_filename, label):
        return out_filename+".klog"

    def _construct_testing_out_filename(self, out_filename, label):
        label_wo_label = label.split("__label__")[1]
        return out_filename+"_"+label_wo_label+".klog"
    
    def _print_one_liner_klogs(self, out_file, klogs):
        out_file = out_file+".klog"
        with open(out_file, 'a+') as out_f:
            for label,klog in klogs:
                self.line_creator(out_f, label, klog)
        return [out_file]


    def _print_sentence_klogs(self, out_file, klogs):
        out_files = set() 
        for label,klog in klogs:
            res_file = self.out_filename_constructor(out_file, label)
            out_files.add(res_file)
            with open(res_file, 'a+') as out_f:
                i = 0
                klog_split = klog.split()
                self.line_creator(out_f, label, klog_split, i)
                i+=self.sentence_increment
                while i < len(klog_split)-self.sentence_size+1:
                    self.line_creator(out_f, label, klog_split, i)
                    i += self.sentence_increment
        return out_files 
