#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pyparsing import *
# from parser import Parser
alpha_ru = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def joiner(x, y, elem):
    return '"' + elem.join([x, y]) + '"'

# def

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
        prev = test_searchdata[prev]

    for operand, action in zip(operands, actions):
        if action == '&':
            # action = lambda x, y: str(len(x) * len(y))
            # action = lambda x, y: joiner(x, y, '&')
            action = lambda x, y: x & y
        elif action == '|':
            # action = lambda x, y: str(len(x) + len(y))
            # action = lambda x, y: joiner(x, y, '|')
            action = lambda x, y: x | y
            # action = sum
        else:
            raise Exception('unknown action {}'.format(action))

        if type(operand) == list:
            operand = reducer(operand)
        elif type(operand) == str:
            # first time only
            operand = test_searchdata[operand]

        prev = action(prev, operand)

    return prev

test_searchdata = {
    'raz': set([1,2,3]),
    'dva': set([2]),
    'tri': set([3]),
}

if __name__ == '__main__':
    # bstart = Word("(", max=1)
    # bend = Word(")", max=1)
    word = Word(alphas + alpha_ru)
    bin_op = Word("&|", max=1)

    expr = Forward()
    bc_value = Group(Suppress("(") + expr + Suppress(")"))
    # bc_value = Suppress("(") + expr + Suppress(")")
    # bc_value = bc_value.setParseAction(lambda s,l,t: [t[0][0] + 's', t[0][1] + 's'])
    trivial = word ^ bc_value

    expr << trivial + ZeroOrMore(bin_op + trivial)
    # expr = expr.setParseAction(lambda s,l,t: reducer(list(t)))

    query = expr
    # query = bin_expr
    for line in sys.stdin:
        parsed = query.parseString(line).asList()
        print reducer(parsed)

    # intNumber = Word(nums).setParseAction( lambda s,l,t: [ int(t[0]) ] )

    # integer = Word( nums ) # simple unsigned integer
    # variable = Word( alphas, max=1 ) # single letter variable, such as x, z, m, etc.
    # arithOp = Word( "+-*/", max=1 ) # arithmetic operators
    # equation = variable + "=" + integer + arithOp + integer # will match "x=2+2", etc.
    # for line in sys.stdin:
    #     # expr = parser.parse(line)
    #     # print(expr.variables())
    #     # print line
    #     print equation.parseString(line)
