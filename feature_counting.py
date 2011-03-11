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

def file2feature_count_file(corpus_path, out_path):
	"""Maps a corpus of GVFI examples into its feature-counts
	   representation and outputs it as a file suitable for feeding to the
	   'maxent' command-line program in MMTK.
	"""
	corpus2feature_count_file(read_gvfi(corpus_path))

def corpus2feature_count_file(corpus, out_path):
	featured_corpus = corpus2features(corpus)
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
			outfile.write('	should be ')
			outfile.write(datum.is_related)
			outfile.write('	')
			outfile.write('	'.join(
				[datum.title, datum.article_url, datum.article_snippet]))
			outfile.write('\n')


def split_corpus(corpus, denominator=12):
	"""Hold out every n-th item in the given dictionary.
	   Returns (training, heldout).
	   Determinismic as long as the keys are fully-ordered.
	"""
	training = {}
	heldout  = {}
	i = 4 # initial value unimportant but affects which subset we hold out
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

	corpus2feature_count_file(training, training_path)
	corpus2feature_count_file(heldout, heldout_path)

	corpus2file(training, training_path + '.preimage')
	corpus2file(heldout, heldout_path + '.preimage')
