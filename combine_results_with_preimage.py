#!/usr/bin/python

"""Given a preimage and predictions file, combines them into a format
   appropriate for the evalNER script.
"""

from optparse import OptionParser

option_parser = OptionParser()
(_, [preimage_path, predictions_path, out_path]) = option_parser.parse_args()

out_file = open(out_path, 'w')
predictions_file = open(predictions_path)
for line in open(preimage_path):
	out_file.write('a' + line.strip('\n'))
	out_file.write('	')
	out_file.write(predictions_file.readline().strip('\n'))
	out_file.write('\n')
