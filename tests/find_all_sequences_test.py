from defects4all.find_similar_sequences import find_similar_sequences 
class TestFindSimilarSequences(object):
    sequence="__label__Sequence 23 43 45 56 67 888 2 3 4 3 2 1"
    subsequences=["__label__Sub1 23 43",
            "__label__Sub2 2 3 4 3"]
    def test_find_best_sequence_at_0(self):
        res = find_similar_sequences(self.sequence, self.subsequences)
        assert(res[0][0][0] == '__label__Sub1')
