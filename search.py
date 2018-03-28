#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pyparsing import *
from docindex import Docindex

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
    elif type(prev) == unicode:
        # first time only
        prev = indexer.get(prev)

    for operand, action in zip(operands, actions):
        if action == '&':
            action = lambda x, y: x.op_and(y)
        elif action == '|':
            action = lambda x, y: x.op_or(y)
        else:
            raise Exception('unknown action {}'.format(action))

        if type(operand) == list:
            operand = reducer(operand)
        elif type(operand) == unicode:
            operand = indexer.get(operand)

        prev = action(prev, operand)

    return prev

class Parser:
    alpha_ru = u'!абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    def __init__(self):
        word = Word(alphas + self.alpha_ru)
        bin_op = Word("&|", max=1)

        expr = Forward()
        bc_value = Group(Suppress("(") + expr + Suppress(")"))
        trivial = word ^ bc_value

        expr << trivial + ZeroOrMore(bin_op + trivial)

        self.expr = expr

    def parseline(self, line):
        return self.expr.parseString(line).asList()

if __name__ == '__main__':
    indexer = Docindex().from_file('main.pickle', 'data.pickle')

    parser = Parser()
    for line in sys.stdin:
        line = line.strip()
        print line
        line = line.decode('utf-8')
        line = line.lower()
        # line = line.encode('utf-8')

        parsed = parser.parseline(line)
        reduced = reducer(parsed)
        print reduced.count()

        result_ids = reduced.get_stored()

        for url in indexer.urls_by_inds(result_ids):
            print(url)
