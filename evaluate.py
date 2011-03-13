#!/usr/bin/env python

"""Evaluates the classifier on the given training set.  Will automatically and
   deterministically hold out a subset for this evaluation.

   Two optional integer-valued options, --intercept and --denominator, control
   which subset gets held out.  The size of the heldout set roughly correlates
   inversely with the --denominator, and it will fluctuate randomly with
   different values of --intercept.  They default to 12 and 4, respectively.
"""

from pprint           import pprint
from feature_counting import file2heldout_feature_count_files
from optparse         import OptionParser
from maxent           import MaxentModel
from evaluation       import *

option_parser = OptionParser()
option_parser.add_option('--denominator', '-d')
option_parser.add_option('--intercept',   '-i')
option_parser.add_option('--raw_out',     '-r')
(options, [corpus_path]) = option_parser.parse_args()

denominator = options.denominator or 12
intercept   = options.intercept   or 4
denominator, intercept = int(denominator), int(intercept)

accuracy, precisions, recalls, f1s, raw = evaluate(corpus_path, denominator, intercept)

if options.raw_out:
	out_file = open(options.raw_out, 'w')
	for (row_in_corpus, (desired, predicted)) in raw.items():
		out_line = [str(row_in_corpus), '	', str(desired), '	', str(predicted), '\n']
		map(out_file.write, out_line)

print "Accuracy: " + str(accuracy)
print "Precisions:"
pprint(precisions)
print "Recalls:"
pprint(recalls)
print("F scores:")
pprint(f1s)
