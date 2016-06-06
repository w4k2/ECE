#!/usr/bin/env python
"""
Experiment 2

dataset: iris
radius: 30
one exponer ([2,3])

testing grains in 1:50
"""

import csv
import time
import numpy as np

import Dataset
from Exponer import *

start = time.time()

dataset = Dataset('data/iris.csv','iris')

chosen_lambda = [2,3]
grains = xrange(1,51)
radius = 30
folds = xrange(0,5)

summary = []

for fold in folds:
	dataset.setCV(fold)
	summary.append([])
	print "\n| %s, fold %i" % (dataset, fold)
	print "GRA\tACC\tSEN\tSPC\tBAC\n---\t---\t---\t---\t---"
		
	for grain in grains:
		exponer = Exponer(dataset, chosen_lambda, grain, radius)

		dataset.clearSupports()
		predictions = exponer.predict(dataset)
		scores = dataset.score()
		print "%03i\t%02.0f%%\t%02.0f%%\t%02.0f%%\t%02.0f%%" % \
			(grain, \
			scores['accuracy']*100, \
			scores['sensitivity']*100, \
			scores['specificity']*100, \
			scores['bac']*100)

		summary[fold].append(scores)
	#	print "score %.2f" % scores['accuracy']

end = time.time()

print "\n# GENERATING SUMMARY"
filename = "results/experiment_2.csv"
textFile = open(filename, "w")
for index, grain in enumerate(grains):
	accumulator = []
	for fold in folds:
		accumulator.append(summary[fold][index])
	
	accuracy = sum(e['accuracy'] for e in accumulator) / len(accumulator)
	sensitivity = sum(e['sensitivity'] for e in accumulator) / len(accumulator)
	specificity = sum(e['specificity'] for e in accumulator) / len(accumulator)
	bac = sum(e['bac'] for e in accumulator) / len(accumulator)
	
	row = "% 3i, %.3f, %.3f, %.3f, %.3f\n" % (grain, accuracy, sensitivity, specificity, bac)
	textFile.write(row)

textFile.close()

print "%.3f seconds" % (end - start)