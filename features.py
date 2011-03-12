from re import search, IGNORECASE

"Some baseline features for testing the classifier."

def make_searcher(pattern, field='article_snippet', flags=IGNORECASE):
	"""Returns a feature template function that defines the feature
	   'has_pattern_' + pattern, which is present whenever the datum
	   contains that pattern.  Default by case-insensitive.
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
		return map(mkfeature, wordset) # TODO: The lambda is a stub.
	return result

feature_templates = [
	# These seem likely to show up in articles about disease:
	make_searcher('estimated'),
	make_searcher('exposure'),
	make_searcher('percent'),
	make_searcher('population'),
	make_searcher('virus'),
	make_searcher('disease'),
	make_searcher('outbreak'),
	make_searcher('report'),
	make_searcher('prevention'),
	make_searcher('control'),
	make_searcher('disease'),
	make_searcher('confirmed'),
	make_searcher('diagnosed'),
	make_searcher('diagnosis'),
	make_searcher('associated'),
	make_searcher('emergency'),
	make_searcher('(epi|pan)demic', 'title'),
	make_searcher('season'), # TODO: Maybe exclude 'hurricane'.
	make_searcher('dea(d|th)'),
	# make_searcher('sick'), 	# Doesn't distinguish.
	# make_searcher('\sill\s'), 	# Doesn't distinguish.
	# make_searcher('issued.*advisory'), # Too sparse.
	# Template:
	# make_searcher(''),

	# Things I'm trying out because of their counts:
	make_searcher('president'),
	make_searcher('&lt;img'), # Has a picture.  Good for 'unrelated'.

	# These seem like they would show up in non-outbreak or non-disease articles:
	make_searcher('rival'),
	make_searcher('sport'),
	make_searcher('champ'),
	make_searcher('protest'),
	make_searcher('hurricane'),
	make_searcher('economy'),
	make_searcher('wedding'), # Good but sparse.
	make_searcher('research'),
	make_searcher('prosecut'),

	# TODO: URL features.

	words_in('title')
	# TODO: Maybe strip away non-word symbols like in "(ap)" and "prosecutors:".
	# TODO: Maybe get the word STEMS in the title, not the words.

]
