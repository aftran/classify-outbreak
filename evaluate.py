#!/usr/bin/env python

"""Evaluates the classifier on the given training set.  Will automatically and
   deterministically hold out a subset for this evaluation.

   Two optional integer-valued options, --intercept and --denominator, control
   which subset gets held out.  The size of the heldout set roughly correlates
   inversely with the --denominator, and it will fluctuate randomly with
   different values of --intercept.  They default to 12 and 4, respectively.
"""

from feature_counting import file2heldout_feature_count_files
from optparse         import OptionParser
from maxent           import MaxentModel
from evaluation       import *

option_parser = OptionParser()
option_parser.add_option('--denominator', '-d')
option_parser.add_option('--intercept',   '-i')
(options, [corpus_path]) = option_parser.parse_args()

denominator = options.denominator or 12
intercept   = options.intercept   or 4
denominator, intercept = int(denominator), int(intercept)

something_TODO = evaluate(corpus_path, denominator, intercept)
