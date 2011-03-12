#!/usr/bin/env python

"""Converts a GVFI file into a training and heldout feature-counts file.
   Two optional integer-valued options, --intercept and --denominator, control
   which subset gets held out.  The size of the heldout set roughly correlates
   inversely with the --denominator, and it will fluctuate randomly with
   different values of --intercept.  They default to 12 and 4, respectively.
"""

from feature_counting import file2heldout_feature_count_files
from optparse         import OptionParser

option_parser = OptionParser()
option_parser.add_option('--denominator', '-d')
option_parser.add_option('--intercept',   '-i')
(options, [corpus_path, training_path, heldout_path]) = option_parser.parse_args()

denominator = options.denominator or 12
intercept   = options.intercept   or 4
denominator, intercept = int(denominator), int(intercept)

file2heldout_feature_count_files(corpus_path, training_path, heldout_path, denominator)
