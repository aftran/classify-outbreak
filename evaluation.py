"""Functions for training and evaluating the classifier."""

from maxent           import MaxentModel
from datum            import Datum, non_ignored_classes, read_gvfi
from features         import feature_templates
from feature_counting import *

def train(corpus, *args):
	projections = {}
	model = MaxentModel()
	model.begin_add_event()
	for datums in corpus.values():
		for datum in datums:
			projection = datum2features(datum)
			model.add_event(datum2features(datum), datum.is_related, long(100 * float(datum._trust)))
			projections[datum.row_in_corpus] = projection
	model.end_add_event()
	model.train(*args)
	return model, projections


def evaluate(corpus_path, denominator, intercept):
        corpus = read_gvfi(corpus_path)
        (training, heldout) = split_corpus(corpus, denominator, intercept)

        model, _ = train(training, 30, 'lbfgs', 2)

	raw = predicted_and_actual_outcomes(model, heldout)

	# predicteds/desireds will be maps from classes (=outcomes) to sets of
	# corpus rows predicted/desired to be in that class:
	predicteds = dict()
	desireds   = dict()
	for outcome in non_ignored_classes:
		for dictionary in predicteds, desireds:
			dictionary[outcome] = set()

	num_correct = 0
	for (row, (desired, predicted)) in raw.items():
		predicteds[predicted].add(row)
		desireds[desired].add(row)
		if desired == predicted:
			num_correct += 1
			# TODO: If we weigh by the annotation's trust, we
			# should use the annotation's trust here (and
			# elsewhere) instead of 1.
	accuracy = float(num_correct) / float(len(raw))
	precisions = dict()
	recalls    = dict()
	f1s        = dict()
	for outcome in non_ignored_classes:
		reference = predicteds[outcome]
		test      = desireds  [outcome]
		precisions[outcome] = nltk.precision(reference, test)
		recalls   [outcome] = nltk.recall   (reference, test)
		f1s       [outcome] = nltk.f_measure(reference, test) # TODO: feed it the right alpha (third arg) for f1.
	return accuracy, precisions, recalls, f1s, raw

def predicted_and_actual_outcomes(model, heldout):
	result = dict()
	for datums in heldout.values():
		for datum in datums:
			projection = datum2features(datum)
			desired = datum.is_related
			distribution = dict(model.eval_all(projection))
			predicted = max(distribution, key=lambda k: distribution[k])
			result[str(datum.row_in_corpus) + '_id' + str(datum.id_article)] = (desired, predicted)
	return result
