#!/usr/bin/env python
"""
Experiment 3

dataset: iris
grain: 20
exponers: all possible combinations

testing radiuses in 1:30
"""

import csv
import time
import numpy as np
import itertools

import Dataset
from Exponer import *

start = time.time()

dataset = Dataset('data/iris.csv','iris')

grain = 20
radiuses = xrange(1,41,1)
folds = xrange(0,5)

summary = []

for fold in folds:
	dataset.setCV(fold)
	summary.append([])
	print "\n| %s, fold %i" % (dataset, fold)
	print "RAD\tACC\tSEN\tSPC\tBAC\n---\t---\t---\t---\t---"
	
	for radius_i in radiuses:
		radius = radius_i / 100.
		dataset.clearSupports()

		combinations = itertools.combinations(range(0, dataset.features), 2)
		for combination in combinations:
			chosen_lambda = [combination[0], combination[1]]
#			print chosen_lambda
			exponer = Exponer(dataset, chosen_lambda, grain, radius)
			predictions = exponer.predict(dataset)

		scores = dataset.score()
		print "%03i\t%02.0f%%\t%02.0f%%\t%02.0f%%\t%02.0f%%" % \
			(radius_i, \
			scores['accuracy']*100, \
			scores['sensitivity']*100, \
			scores['specificity']*100, \
			scores['bac']*100)

		summary[fold].append(scores)

end = time.time()

print "\n# GENERATING SUMMARY"
filename = "results/experiment_3.csv"
textFile = open(filename, "w")
for index, radius in enumerate(radiuses):
	accumulator = []
	for fold in folds:
		accumulator.append(summary[fold][index])
	
	accuracy = sum(e['accuracy'] for e in accumulator) / len(accumulator)
	sensitivity = sum(e['sensitivity'] for e in accumulator) / len(accumulator)
	specificity = sum(e['specificity'] for e in accumulator) / len(accumulator)
	bac = sum(e['bac'] for e in accumulator) / len(accumulator)
	
	row = "% 3i, %.3f, %.3f, %.3f, %.3f\n" % (radius, accuracy, sensitivity, specificity, bac)
	textFile.write(row)

textFile.close()

print "%.3f seconds" % (end - start)
