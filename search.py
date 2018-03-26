#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pyparsing import *
from docindex import Docindex

alpha_ru = '!абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def joiner(x, y, elem):
    return '"' + elem.join([x, y]) + '"'

def reducer(data):
    actions = data[1::2]
    operands = data[2::2]

    if len(actions) != len(operands):
        raise Exception('actions-operands disbalance')

    prev = data[0]
    if type(prev) == list:
        prev = reducer(prev)
    elif type(prev) == str:
        # first time only
        prev = indexer.get(prev)
        # prev = test_searchdata[prev]

    for operand, action in zip(operands, actions):
        if action == '&':
            # action = lambda x, y: str(len(x) * len(y))
            # action = lambda x, y: joiner(x, y, '&')
            # action = lambda x, y: x & y
            action = lambda x, y: x.op_and(y)
        elif action == '|':
            # action = lambda x, y: str(len(x) + len(y))
            # action = lambda x, y: joiner(x, y, '|')
            # action = lambda x, y: x | y
            action = lambda x, y: x.op_or(y)
            # action = sum
        else:
            raise Exception('unknown action {}'.format(action))

        if type(operand) == list:
            operand = reducer(operand)
        elif type(operand) == str:
            operand = indexer.get(operand)
            # operand = test_searchdata[operand]

        prev = action(prev, operand)

    return prev

test_searchdata = {
    'raz': set([1,2,3]),
    'dva': set([2]),
    'tri': set([3]),
}
# indexer = Docindex(test_searchdata)
indexer = Docindex().from_file('index.pickle')

class Parser:
    def __init__(self):
        word = Word(alphas + alpha_ru)
        bin_op = Word("&|", max=1)

        expr = Forward()
        bc_value = Group(Suppress("(") + expr + Suppress(")"))
        trivial = word ^ bc_value

        expr << trivial + ZeroOrMore(bin_op + trivial)

        self.expr = expr

    def parseline(self, line):
        return self.expr.parseString(line).asList()

if __name__ == '__main__':
    parser = Parser()
    for line in sys.stdin:
        line = line.strip()
        print line
        line = line.decode('utf-8')
        line = line.lower()
        line = line.encode('utf-8')

        parsed = parser.parseline(line)
        reduced = reducer(parsed)
        print reduced.count()

        result_ids = reduced.get_as_set()

        for url in indexer.urls_by_inds(result_ids):
            print(url)
