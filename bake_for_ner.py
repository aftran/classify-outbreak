#!/usr/bin/env python

"""Gets the named entities in each article.  Outputs a pickled dict from
   id_article to entity type to a list of entity names.
"""

import nltk
import pickle
from datum    import Datum, read_gvfi
from optparse import OptionParser

option_parser = OptionParser()
(options, [corpus_path, out_path]) = option_parser.parse_args()

corpus = read_gvfi(corpus_path)

def named_entities(datum):
	"""Return a dict from entity type to a list of named entities of that
	   type in the given datum.
	"""
	result = {}
	for sent in nltk.sent_tokenize(datum.article_snippet):
		for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
			if hasattr(chunk, 'node'):
				result.setdefault(chunk.node, [])
				result[chunk.node].append('_'.join(c[0].lower() for c in chunk.leaves()))
	return result

result = dict()
for datums in corpus.values():
	print '.',
	for datum in datums:
		result[datum.id_article] = named_entities(datum)
		break # The rest of the datums are the same article.

pickle.dump(result, open(out_path, 'w'))
