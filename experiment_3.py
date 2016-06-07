#!/usr/bin/env python
"""
Experiment 3

dataset: iris
grain: 20
exponers: all possible combinations vs one exponer ([2,3])

testing radiuses in 1:30
"""

import csv
import time
import numpy as np
import itertools

import Dataset
from Exponer import *
from EEC import *

start = time.time()

# Load dataset
dataset = Dataset('data/iris.csv','iris')

grain = 20
radiuses = xrange(1,31,1)
folds = xrange(0,5)

summary = []

for fold in folds:
	dataset.setCV(fold)
	summary.append([])
	print "\n| %s, fold %i" % (dataset, fold)
	print "RAD\tACC\tBAC\tACC\tBAC\n---\t---\t---\t---\t---"
	
	for radius_i in radiuses:
		radius = radius_i / 100.

		configuration = {'radius': radius, 'grain': grain}
		eec = EEC(dataset,configuration)
		eec.predict()

		scores = dataset.score()

		chosen_lambda = [2,3]
		exponer = Exponer(dataset,chosen_lambda,configuration)
		dataset.clearSupports()
		exponer.predict()
		scores2 = dataset.score()

		print "%03i\t%02.0f%%\t%02.0f%%\t%02.0f%%\t%02.0f%%" % \
			(radius_i, \
			scores['accuracy']*100, \
			scores['bac']*100,\
			scores2['accuracy']*100, \
			scores2['bac']*100)

		result = {
			'accuracy1': scores['accuracy'],
			'accuracy2': scores2['accuracy'],
			'bac1': scores['bac'],
			'bac2': scores2['bac']
		}

		summary[fold].append(result)

end = time.time()

print "\n# GENERATING SUMMARY"
filename = "results/experiment_3.csv"
textFile = open(filename, "w")
for index, radius in enumerate(radiuses):
	accumulator = []
	for fold in folds:
		accumulator.append(summary[fold][index])
	
	accuracy1 = sum(e['accuracy1'] for e in accumulator) / len(accumulator)
	accuracy2 = sum(e['accuracy2'] for e in accumulator) / len(accumulator)
	bac1 = sum(e['bac1'] for e in accumulator) / len(accumulator)
	bac2 = sum(e['bac2'] for e in accumulator) / len(accumulator)
	
	row = "% 3i, %.3f, %.3f, %.3f, %.3f\n" % (radius, accuracy1, bac1, accuracy2, bac2)
	textFile.write(row)

textFile.close()

print "%.3f seconds" % (end - start)