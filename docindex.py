import pickle

class Docindex:
    def __init__(self):
        self.doc_last = 0
        self.urls = []

        self.data = dict()

    def get(self, key):
        is_pos = key[0] != '!'
        key = key if is_pos else key[1:]
        if key in self.data:
            stored_data = self.data[key]
        else:
            stored_data = []
        return Partindex(stored_data, is_pos, self.doc_last)

    def add_doc(self, doc_url, words):
        self.doc_last += 1
        self.urls.append(doc_url)

        for word in words:
            # word = word.encode('utf-8')
            if word not in self.data:
                self.data[word] = [self.doc_last]
            else:
                self.data[word].append(self.doc_last)

    def to_file(self, filename):
        with open(filename, 'w') as f:
            pickle.dump(self, f)

    def from_file(self, filename):
        with open(filename, 'r') as f:
            new_data = pickle.load(f)
            self.data = new_data.data
            self.doc_last = new_data.doc_last
            self.urls = new_data.urls

        return self

    def urls_by_inds(self, inds):
        inds = sorted(list(inds))
        return [self.urls[i - 1] for i in inds]

def merge(l1,l2):
    if not l1:  l2
    if not l2:  l1

    result = []
    itx = iter(l1)
    ity = iter(l2)
    x = itx.next()
    y = ity.next()

    try:
        while True:
            while x != y:
                if x < y:
                    result.append(x)
                    x = itx.next()
                else:
                    result.append(y)
                    y = ity.next()
            result.append(x)
            x = itx.next()
            y = ity.next()

    except StopIteration:
        pass

    if x > result[-1]:
        result.append(x)

    if y > result[-1]:
        result.append(y)

    result.extend(itx)
    result.extend(ity)


    return result

def cross(l1,l2):
    if not l1:  return []
    if not l2:  return []

    result = []
    itx = iter(l1)
    ity = iter(l2)
    y = ity.next()
    x = itx.next()

    try:
        while True:
            while x != y:
                if x < y:
                    x = itx.next()
                else:
                    y = ity.next()
            result.append(x)
            x = itx.next()
            y = ity.next()

    except StopIteration:
        pass

    return result

class Partindex:
    def __init__(self, stored_data, is_pos, doc_last):
        stored_data = sorted(stored_data)
        self.data = stored_data
        self.is_pos = is_pos
        self.doc_last = doc_last

    def get_stored(self):
        if self.is_pos:
            return self.data
        else:
            return list([x for x in xrange(1, self.doc_last+1) if x not in self.data])

    def op_and(self, other):
        new_data = cross(self.get_stored(), other.get_stored())
        return Partindex(new_data, True, self.doc_last)

    def op_or(self, other):
        new_data = merge(self.get_stored(), other.get_stored())
        return Partindex(new_data, True, self.doc_last)

    def count(self):
        if self.is_pos:
            return len(self.data)
        else:
            return self.doc_last - len(self.data)

    def __str__(self):
        return str(self.get_stored())

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
