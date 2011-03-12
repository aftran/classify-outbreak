#!/usr/bin/env python

"""Utility functions for counting features in articles."""

from datum    import *
from features import *

def datum2features(datum):
	"""The features for the given datum, in list form."""
	result = []
	for feature_template in feature_templates:
		result.extend(feature_template(datum))
	return result

def corpus2features(corpus):
	"""Copies the given corpus and turns each datum into
	   	(is_related, features),
	   where is_related is its class and features is a list of its
	   features.
	"""
	result = {}
	for (id_article, datums) in corpus.iteritems():
		result[id_article] = map(lambda d: (d.is_related, datum2features(d)), datums)
	return result

def features2feature_count_file(featured_corpus, out_path):
	outfile = open(out_path, 'w')
	for datums in featured_corpus.values():
		for (is_related, featurelist) in datums:
			outfile.write(is_related)
			outfile.write(' ')
			outfile.write(' '.join(featurelist))
			# MMTK crashes if we have no active features:
			if featurelist == []:
				print 'Warning: We have a datum that no features matched.'
				outfile.write('no_other_features_matched_this_article')
			outfile.write('\n')


def corpus2file(corpus, out_path):
	outfile = open(out_path, 'w')
	for datums in corpus.values():
		for datum in datums:
			outfile.write(datum.id_article)
			outfile.write('	')
			outfile.write(datum.is_related)
			outfile.write('\n')

def split_corpus(corpus, denominator=12, intercept = 4):
	"""Hold out every n-th item in the given dictionary.
	   Returns (training, heldout).
	   Determinismic as long as the keys are fully-ordered.
	   Warning: the number of rows in the heldout set will vary wildly as
	   the subset of keys changes, since the keys have different numbers of
	   rows associated with them.  So change the intercept and denominator
	   until the size of the heldout set is good.  Of course, don't just
	   hill-climb on the denominator and intercept.
	"""
	training = {}
	heldout  = {}
	i = intercept % denominator # initial value unimportant but affects which subset we hold out
	for (k,v) in sorted(corpus.items()):
		if i == 0:	heldout[k]  = v
		else:		training[k] = v
		i = (i + 1) % denominator
	return (training, heldout)

def file2heldout_feature_count_files(corpus_path, training_path, heldout_path, denominator):
	"""Compute feature counts, output to training_path, hold out
	   every denominator-th article in the corpus and output it to
	   holdout_path.  An article will never show up in both the training
	   and the heldout file.
	   The size of the heldout set won't necessarily be 1/denominator times
	   the size of the input corpus, since we split the corpus by article
	   rather than annotation instance, and there are often many annotation
	   instances per article.
	   Also outputs the preimages of the training and heldout sets to
	   training_path.preimage and deldout_path.preimage.
	"""
	corpus = read_gvfi(corpus_path)
	(training, heldout) = split_corpus(corpus, denominator)

	training_features = corpus2features(training)
	heldout_features  = corpus2features(heldout)

	features2feature_count_file(training_features, training_path)
	features2feature_count_file(heldout_features,  heldout_path)

	corpus2file(training, training_path + '.preimage')
	corpus2file(heldout,  heldout_path +  '.preimage')
