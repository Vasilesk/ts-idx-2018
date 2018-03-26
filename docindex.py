import pickle

class Docindex:
    def __init__(self):
        self.data = dict()
    def add_doc_words(self, doc_id, words):
        for word in words:
            if word not in self.data:
                self.data[word] = set()
            self.data[word].add(doc_id)

    def to_file(self, filename):
        with open(filename, 'w') as f:
            pickle.dump(self.data, f)

    def from_file(self, filename):
        with open(filename, 'r') as f:
            new_data = pickle.load(f)
            self.data.update(new_data)
