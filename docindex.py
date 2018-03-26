import pickle

class Docindex:
    def __init__(self, data = None):
        self.min_id = -1
        self.max_id = -1

        if data is None:
            self.data = dict()
        else:
            self.data = data
            for word in data:
                max_id = max(data[word])
                min_id = min(data[word])

            self.update_min_max(min_id)
            self.update_min_max(max_id)

    def update_min_max(self, new_id):
        if new_id > self.max_id:
            self.max_id = new_id
        if new_id < self.min_id or self.min_id < 0:
            self.min_id = new_id

    def get(self, key):
        is_pos = key[0] != '!'
        key = key if is_pos else key[1:]
        if key in self.data:
            set_data = self.data[key]
        else:
            set_data = set()
        return Partindex(set_data, is_pos, self.min_id, self.max_id)

    def add_doc(self, doc_id, words):
        self.update_min_max(doc_id)

        for word in words:
            word = word.encode('utf-8')
            if word not in self.data:
                self.data[word] = set()
            self.data[word].add(doc_id)

    def to_file(self, filename):
        with open(filename, 'w') as f:
            pickle.dump(self, f)

    def from_file(self, filename):
        with open(filename, 'r') as f:
            new_data = pickle.load(f)
            self.data = new_data.data
            self.min_id = new_data.min_id
            self.max_id = new_data.max_id

        return self

class Partindex:
    def __init__(self, set_data, is_pos, min_id, max_id):
        self.data = set_data
        self.is_pos = is_pos
        self.min_id = min_id
        self.max_id = max_id

    def get_as_set(self):
        if self.is_pos:
            return self.data
        else:
            return set([x for x in xrange(self.min_id, self.max_id + 1) if x not in self.data])
            # raise Exception('trying to fetch data for negative request')

    def op_and(self, other):
        new_data = self.get_as_set() & other.get_as_set()
        return Partindex(new_data, True, self.min_id, self.max_id)

    def op_or(self, other):
        new_data = self.get_as_set() | other.get_as_set()
        return Partindex(new_data, True, self.min_id, self.max_id)

    def __str__(self):
        return str(self.get_as_set())
