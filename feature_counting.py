#!/usr/bin/env python

"""Maps a corpus of GVFI examples into its feature-counts representation and
   outputs it as a file suitable for feeding to the 'maxent' command-line program
   in MMTK.
"""

from datum    import *
from features import *

def datum2features(datum):
	"""The features for the given datum, in list form."""
	result = []
	for feature_template in feature_templates:
		result.extend(feature_template(datum))
	return result

# TODO: Have a function for outputting both a testing and a training corpus, making sure the same article doesn't show up in both.  With a function for splitting a corpus dictionary by key subsets.

def corpus2features(corpus):
	"""Copies the given corpus and turns each datum into a list of its features."""
	result = {}
	for (id_article, datums) in corpus.iteritems():
		result.setdefault(id_article, [])
		result[id_article] = map(datum2features, datums)

	

# def project_to_file(corpus_path, out_path):
# 	corpus = read_gvfi(corpus_path)
# 	outfile = open(out_path, 'w')
# 	for datums in corpus.values():
# 		for datum in datums:
# 			context = []
# 			for feature_template in feature_templates:
# 				context.extend(feature_template(datum))
# 		outfile.write(...)
