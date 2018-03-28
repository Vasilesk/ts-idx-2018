#!/usr/bin/env python
import argparse
import document_pb2
import struct
import gzip
import sys

from docindex import Docindex
from doc2words import extract_words

class DocumentStreamReader:
    def __init__(self, paths):
        self.paths = paths

    def open_single(self, path):
        return gzip.open(path, 'rb') if path.endswith('.gz') else open(path, 'rb')

    def __iter__(self):
        for path in self.paths:
            with self.open_single(path) as stream:
                while True:
                    sb = stream.read(4)
                    if sb == '':
                        break

                    size = struct.unpack('i', sb)[0]
                    msg = stream.read(size)
                    doc = document_pb2.document()
                    doc.ParseFromString(msg)
                    yield doc


def parse_command_line():
    parser = argparse.ArgumentParser(description='compressed documents reader')
    parser.add_argument('encoding', nargs=1, help='Encoding method (varbyte|simple9)')
    parser.add_argument('files', nargs='+', help='Input files (.gz or plain) to process')
    return parser.parse_args()


if __name__ == '__main__':
    di = Docindex()
    args = parse_command_line()
    reader = DocumentStreamReader(args.files)
    # print args.encoding
    # print args.files
    for doc in reader:
        # print "%s\t%d bytes" % (doc.url, len(doc.text))
        words = extract_words(doc.text)
        di.add_doc(doc.url, words)
        # for word in words:
        #     print(word)
        # print di.data
        # break

    di.dump('main.pickle', 'data.pickle')
