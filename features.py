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

feature_templates = map(make_searcher, [
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
	'research',
	'prosecut'] # as in 'prosecution' and 'prosecuted'.
	) + [
	# TODO: URL features.
	make_searcher('(epi|pan)demic', 'title'),
	make_searcher('H\dN\d', field='article_snippet', flags=0), # names of flu subtypes, like H1N1
	words_in('title'),
	# TODO: Maybe strip away non-word symbols like in "(ap)" and "prosecutors:".
	# TODO: Maybe get the word STEMS in the title, not the words.
	# TODO: Replace all numbers with a single digit or something.

	]
