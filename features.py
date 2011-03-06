from re import search

"Some baseline features for testing the classifier."

def make_searcher(substring, field='content'):
	def result(datum):
		if search(substring, datum.__dict__[field]):
			return ['has_substring_' + substring]
		else:
			return []
	return result

def f2(datum):
	return [str(len(datum.content) % 8)]

def f3(datum):
	return [str(len(datum.article_url) % 8)]

def f4(datum):
	return [str(len(datum.feed_url) % 8)]

feature_templates = [make_searcher('confirmed'), f2, f3, f4]
