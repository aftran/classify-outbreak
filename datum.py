"Wrapper around the contents of one line in a GVFI-annotated document."

class Datum:
	def __init__(self, line):
		[self.relevant, self.title, self.content, self.article_url, self.feed_url, self.id_article, self.id_feed, self.language, self.date] = line.split('	')
