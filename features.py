from re import search, IGNORECASE
import nltk

"Features for the classifier."

def make_searcher(pattern, field='article_snippet', flags=IGNORECASE):
	"""Returns a feature template function that defines the feature
	   'has_pattern_' + pattern, which is present whenever the datum
	   contains that pattern.  Defaults to case-insensitive.
	"""
	def result(datum):
		if search(pattern, datum.__dict__[field], flags):
			return [field + '_has_pattern_' + pattern]
		else:
			return []
	return result

def words_in(field):
	"""Makes a feature for each word in the given field."""
	def result(datum):
		wordset = set()
		def mkfeature(string): return field + '_has_word_' + string
		for word in datum.__dict__[field].split():
			wordset.add(word.lower())
		return map(mkfeature, wordset)
	return result

# Since NER is slow, only do it for the first cutoff_for_ner characters of the
# article_snippet:
cutoff_for_ner = 1000
# Again, since NER is slow, only do it for the first
# per_sentence_cutoff_for_ner characters of each sentence:
per_sentence_cutoff_for_ner = 10

def named_entities(datum):
	result = []
	for sent in nltk.sent_tokenize(datum.article_snippet[:cutoff_for_ner]):
		for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent[:per_sentence_cutoff_for_ner]))):
			if hasattr(chunk, 'node'):
				result.append('article_snippet_has_entity_' + chunk.node + '_' +  '_'.join(c[0].lower() for c in chunk.leaves()))
	return result

matcher_features = map(make_searcher, [
	# These seem likely to show up in articles about disease:
	'estimated',
	'exposure',
	'percent',
	'population',
	'virus',
	'disease',
	'outbreak',
	'report',
	'prevention',
	'control',
	'disease',
	'confirmed',
	'diagnosed',
	'diagnosis',
	'associated',
	'emergency',
	'season', # TODO: Maybe exclude 'hurricane'.
	'dea(d|th)',
	'authorities',
	# 'sick', 		# Doesn't distinguish.
	# '\sill\s', 		# Doesn't distinguish.
	# 'issued.*advisory', 	# Too sparse.

	# Things I'm trying out because of their counts:
	'president',
	'&lt;img', # Has a picture.  Good for 'unrelated'.

	# These seem like they would show up in non-outbreak or non-disease articles:
	'rival',
	'sport',
	'champ',
	'protest',
	'hurricane',
	'economy',
	'wedding', # Good but sparse.
	'linux',
	'research',
	'prosecut'] # as in 'prosecution' and 'prosecuted'.
	)

other_features = [
	# TODO: URL features.
	named_entities,
	make_searcher('(epi|pan)demic', 'title'),
	make_searcher('H\dN\d', field='article_snippet', flags=0), # names of flu subtypes, like H1N1
	words_in('title'),
	# TODO: Maybe strip away non-word symbols like in "(ap)" and "prosecutors:".
	# TODO: Maybe get the word STEMS in the title, not the words.
	# TODO: Replace all numbers with a single digit or something.

	]

feature_templates = matcher_features + other_features
