#!/usr/bin/env python

from docindex import Docindex
from doc2words import extract_words

doc_texts = [
    {
        'url': '/get-set-update',
        'text': 'update get set'
    },
    {
        'url': '/get-set',
        'text': 'get set'
    },
    {
        'url': '/set',
        'text': 'set'
    },

]

if __name__ == '__main__':
    di = Docindex()
    for doc in doc_texts:
        print "%s\t%d bytes" % (doc['url'], len(doc['text']))
        words = extract_words(doc['text'])
        di.add_doc(doc['url'], words)
    di.to_file('index.pickle')
