import csv

"""Wrapper around the contents of one line in a GVFI-annotated corpus of web
   documents.
"""

non_ignored_classes = ['unrelated', 'just_disease', 'outbreak'] # ignore 'cant_tell' and ''

class Datum:
	def __init__(self, row):
		[
			_, # self._unit_id,
			_, # self._created_at,
			_, # self._golden,
			_, # self._id,
			_, # self._missed,
			_, # self._started_at,
			_, # self._tainted,
			_, # self._channel,
			_, # self._trust,
			_, # self._worker_id,
			_, # self._country,
			_, # self._region,
			_, # self._city,
			_, # self._ip,
			_, # self.country,
			_, # self.disease,
			_, # self.if_a_city_region_town_or_village_name_is_mentioned_in_the_article_please_enter_it_here,
			self.is_related,
			self.article_snippet,
			self.article_url,
			_, # self.country_gold,
			_, # self.disease_gold,
			self.id_article,
			_, # self.is_related_gold,
			self.language,
			self.title
		] = row

from pprint import *

def read_gvfi(path):
	"""Turns a GVFI file into a dictionary from IDs to lists of Datums."""
	csvfile = open(path)
	csvfile.next() # Skip zeroth line because it just has column labels.
	reader = csv.reader(csvfile, dialect=csv.excel)

	result = {}
	for row in reader:
		datum = Datum(row)
		if datum.is_related in non_ignored_classes:
			result.setdefault(datum.id_article, [])
			result[datum.id_article].append(datum)
	return result
