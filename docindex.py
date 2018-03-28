import io
import pickle

class Docindex:
    def __init__(self):
        self.doc_last = 0
        self.urls = []

        self.data = dict()

    def get(self, key):
        is_pos = key[0] != '!'
        key = key if is_pos else key[1:]
        if key in self.index:
            stored_data = nums_from_varbyte(bytearray(self.index[key]))
        else:
            stored_data = []
        return Partindex(stored_data, is_pos, self.doc_last)

    def add_doc(self, doc_url, words):
        self.doc_last += 1
        self.urls.append(doc_url)

        for word in words:
            # word = word.encode('utf-8')
            if word not in self.data:
                st = Stream()
                st.store(self.doc_last)
                self.data[word] = st
            else:
                self.data[word].store(self.doc_last)

    def dump(self, main, data):
        self.word_next_pos = []
        with open(data, 'w') as f:
            for word in self.data:
                f.write(self.data[word].getvalue())
                self.word_next_pos.append((word, f.tell()))

        del self.data

        with open(main, 'w') as f:
            pickle.dump(self, f)

    def load(self, main, data):
        with open(main, 'r') as f:
            new_data = pickle.load(f)
            self.doc_last = new_data.doc_last
            self.urls = new_data.urls
            word_next_pos = new_data.word_next_pos

        self.index = dict()

        prev_pos = 0
        with open(data, 'r') as f:
            for word, pos in word_next_pos:
                word_bytes = f.read(pos - prev_pos)

                self.index[word] = word_bytes
                prev_pos = pos

        return self

    def urls_by_inds(self, inds):
        inds = sorted(list(inds))
        return [self.urls[i - 1] for i in inds]

class Stream:
    mask = 127
    mask_end = 128

    def __init__(self):
        self.last_num = 0
        self.stream = io.BytesIO(b"")
        self.getvalue = self.stream.getvalue

    def store(self, num):
        to_store = num - self.last_num
        self.last_num = num

        buf = bytearray(1)

        while to_store != 0:
            buf[0] = to_store & self.mask
            self.stream.write(buf)
            to_store = to_store >> 7

        self.stream.seek(-1, 1)
        buf[0] |= self.mask_end
        self.stream.write(buf)

# gets bytearray, returns list of numbers
def nums_from_varbyte(varbyte):
    last_num = 0
    res = []
    mask = 127
    mask_end = 128

    elem = 0
    elem_size = 0
    for x in varbyte:
        elem = elem << 7
        elem += x & mask
        elem_size += 1
        if x & mask_end:
            new_elem = 0
            while elem_size != 0:
                new_elem = new_elem << 7
                new_elem += elem & mask
                elem = elem >> 7
                elem_size -= 1

            last_num = new_elem + last_num
            res.append(last_num)

            elem_size = 0
            elem = 0

    return res

def merge(l1,l2):
    if not l1:
        return l2
    if not l2:
        return l1

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
    if not l1:
        return []
    if not l2:
        return []

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
            return [x for x in xrange(1, self.doc_last+1) if x not in self.data]

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

# class Varbyte_storage:
#     def __init__(self,)

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
