#!/usr/bin/env python

"""Converts a GVFI file into a training and heldout feature-counts file."""

from feature_counting import file2heldout_feature_count_files
from optparse         import OptionParser

option_parser = OptionParser()
option_parser.add_option('--denominator', '-d')
(options, [corpus_path, training_path, heldout_path]) = option_parser.parse_args()

if options.denominator:
	denominator = int(options.denominator)
else:
	denominator = 12

file2heldout_feature_count_files(corpus_path, training_path, heldout_path, denominator)
