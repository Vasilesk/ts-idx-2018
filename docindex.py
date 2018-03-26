import pickle

class Docindex:
    def __init__(self):
        self.doc_last = 0
        self.urls = []

        self.data = dict()
        # self.min_id = -1
        # self.max_id = -1

        # if data is None:
        #     self.data = dict()
        # else:
        #     self.data = data
        #     for word in data:
        #         max_id = max(data[word])
        #         min_id = min(data[word])

            # self.update_min_max(min_id)
            # self.update_min_max(max_id)

    # def update_min_max(self, new_id):
    #     if new_id > self.max_id:
    #         self.max_id = new_id
    #     if new_id < self.min_id or self.min_id < 0:
    #         self.min_id = new_id

    def get(self, key):
        is_pos = key[0] != '!'
        key = key if is_pos else key[1:]
        if key in self.data:
            set_data = self.data[key]
        else:
            set_data = set()
        return Partindex(set_data, is_pos, self.doc_last)

    def add_doc(self, doc_url, words):

        self.doc_last += 1
        self.urls.append(doc_url)
        # self.update_min_max(doc_url)

        for word in words:
            # word = word.encode('utf-8')
            if word not in self.data:
                self.data[word] = set()
            self.data[word].add(self.doc_last)

    def to_file(self, filename):
        with open(filename, 'w') as f:
            pickle.dump(self, f)

    def from_file(self, filename):
        with open(filename, 'r') as f:
            new_data = pickle.load(f)
            self.data = new_data.data
            self.doc_last = new_data.doc_last
            self.urls = new_data.urls
            # self.min_id = new_data.min_id
            # self.max_id = new_data.max_id

        return self

    def urls_by_inds(self, inds):
        # print self.doc_last
        # print len(self.urls)
        # print '....'
        # res = []
        # for i in inds:
        #     print i - 1
        #     res_elem = self.urls[i - 1]
        #     res.append(res_elem)
        # return res
        return [self.urls[i - 1] for i in inds]


class Partindex:
    def __init__(self, set_data, is_pos, doc_last):
        self.data = set_data
        self.is_pos = is_pos
        self.doc_last = doc_last
        # self.min_id = min_id
        # self.max_id = max_id

        # self.iteration = None

    def get_as_set(self):
        if self.is_pos:
            return self.data
        else:
            return set([x for x in xrange(1, self.doc_last+1) if x not in self.data])
            # raise Exception('trying to fetch data for negative request')

    def op_and(self, other):
        new_data = self.get_as_set() & other.get_as_set()
        return Partindex(new_data, True, self.doc_last)

    def op_or(self, other):
        new_data = self.get_as_set() | other.get_as_set()
        return Partindex(new_data, True, self.doc_last)

    def count(self):
        if self.is_pos:
            return len(self.data)
        else:
            return self.doc_last - len(self.data)

    def __str__(self):
        return str(self.get_as_set())

    # def __iter__(self):
    #     return self
    #
    # def next(self):
    #     if self.iteration is None:
    #         self.iteration =
    #     if self.i < self.n:
    #         i = self.i
    #         self.i += 1
    #         return i
    #     else:
    #         raise StopIteration()
