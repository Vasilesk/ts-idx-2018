#!/usr/bin/env python
# -*- coding: utf-8 -*-

from docindex import Docindex

if __name__ == '__main__':
    indexer = Docindex().load('main.pickle', 'index/{}.dat')
    indexer.as_server()
