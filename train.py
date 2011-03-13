#!/usr/bin/env python

"""Trains a maximum entropy model on the given training file.
"""

from optparse         import OptionParser

from evaluation       import *

option_parser = OptionParser()
(_, [corpus_path, out_path]) = option_parser.parse_args()

loaded_corpus = read_gvfi(corpus_path)
m,_ = train(loaded_corpus, 30, 'lbfgs', 2)
m.save(out_path)
