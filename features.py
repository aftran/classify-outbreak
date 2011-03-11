from re import search, IGNORECASE

"Some baseline features for testing the classifier."

def make_searcher(substring, field='article_snippet', flags=IGNORECASE):
	"""Returns a feature template function that defines the feature
	   'has_substring_' + substring, which is present whenever the datum
	   contains that substring.  Default by case-insensitive.
	"""
	def result(datum):
		if search(substring, datum.__dict__[field], flags):
			return [field + '_has_substring_' + substring]
		else:
			return []
	return result

feature_templates = [
	make_searcher('confirmed'),
	make_searcher('-associated')
]
