"Some baseline features for testing the classifier."

def f1(datum):
	return [datum.relevant]

def f2(datum):
	return [str(len(datum.content) % 8)]

def f3(datum):
	return [str(len(datum.article_url) % 8)]

def f4(datum):
	return [str(len(datum.feed_url) % 8)]

feature_templates = [f1, f2, f3, f4]
