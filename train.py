#!/usr/bin/env python

"""Trains a maximum entropy model on the given training file.
"""

from optparse import OptionParser
from maxent   import MaxentModel
from datum    import *
from features import feature_templates

option_parser = OptionParser()
(_, [corpus_path, out_path]) = option_parser.parse_args()

corpus = read_gvfi(corpus_path)

m = MaxentModel()
m.begin_add_event()

for datums in corpus.values():
	for datum in datums:
		context = []
		for feature_template in feature_templates:
			context.extend(feature_template(datum))
		m.add_event(context, datum.is_related)

m.end_add_event()

m.train(100, 'gis', 2)
m.save(out_path)
