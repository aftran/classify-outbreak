#!/usr/bin/env python

"""Trains a maximum entropy model on the given training file.
"""

from optparse import OptionParser
from maxent   import MaxentModel
from datum    import Datum
from features import feature_templates

option_parser = OptionParser()
(_, [corpus_path, out_path]) = option_parser.parse_args()

m = MaxentModel()
m.begin_add_event()
for line in open(corpus_path):
	context = []
	for feature_template in feature_templates:
		datum = Datum(line)
		context.extend(feature_template(datum))
	m.add_event(context, datum.relevant)
#	print context
m.end_add_event()

m.train(100, 'gis', 2)
m.save(out_path)
