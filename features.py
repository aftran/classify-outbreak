from re     import search, IGNORECASE
from string import strip, punctuation
import re
import nltk
import pickle
import xml.sax.saxutils

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

# stemmer = lambda x: x
stemmer = nltk.PorterStemmer().stem

# stems_regexp = '(ing)|(ed)|(ly)|(s)' # Very messy but might work anyway.
# stemmer = nltk.RegexpStemmer(stems_regexp, min=3).stem

# stemmer = nltk.LancasterStemmer().stem
# stemmer = nltk.WordNetLemmatizer().lemmatize

def clean_up(text):
	return nltk.clean_html(xml.sax.saxutils.unescape(text))

def stems_in(field):
	"""Makes a feature for each stem in the given field."""
	def result(datum):
		stemset = set()
		text = clean_up(datum.__dict__[field])
		def mkfeature(string): return field + '_has_stem_' + string
		for word in datum.__dict__[field].split():
			stemset.add(stemmer(strip(word.lower(), punctuation)))
		return map(mkfeature, stemset)
	return result

def subdomain(datum):
	"""Makes a feature for the subdomain.  For example, an article from
	   www2.portal.nature.com will have the subbdomain_portal.nature.com feature.
	"""
	m = re.match('http://(www.?.?\.)?([^/]*)/(([^/]*/)*)', datum.article_url)
	result = []
	if hasattr(m, 'groups') and len(m.groups()) > 1:
		result.append('subdomain_' + m.groups()[1])
	return result

try:	stored_ner_results = pickle.load(open('named_entities.pickle'))
except:
	print "Can't find named_entities.pickle.",
	"To generate it, run: ./bake_for_ner.py <path to your corpus> named_entities.pickle"
	raise

def named_entities(datum):
	"""Makes a feature for each named entity (including its type, like
	   "PERSON" or "ORGANIZATION").  Also makes a feature for whether a
	   certain type of named entity is present.
	"""
	result = []
	datum_ner_results = stored_ner_results[datum.id_article]
	for (entity_type, entity_list) in datum_ner_results.items():
		result.append('has_entities_of_type_' + entity_type)
		for entity in entity_list:
			result.append('has_entity_' + entity_type + '_' + stemmer(entity))
	return result

matcher_features = map(make_searcher, [
	# These seem likely to show up in articles about disease:
	'human',
	'hospitalize',
	'adult',
	'children',
	'cases',
	'positive',
	'fever'
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
	'&lt;a ', # Has a hyperlink.

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
	named_entities,
	make_searcher('(epi|pan)demic', 'title'),
	make_searcher('H\dN\d', field='article_snippet', flags=0), # names of flu subtypes, like H1N1
	stems_in('title'),
	stems_in('article_snippet'),
	# TODO: Maybe strip away non-word symbols like in "(ap)" and "prosecutors:".
	# TODO: Maybe get the word STEMS in the title, not the words.
	# TODO: Replace all numbers with a single digit or something.
	subdomain
	# TODO: Other URL features.
	]
feature_templates = matcher_features + other_features
# feature_templates = [lambda datum: datum.is_related] # For debugging.
