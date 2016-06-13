#!/usr/bin/env python
"""
Experiment 7

dataset: iris
grain: 20
exponers: brutal exposers with limit 8

testing radiuses in 1:40
2D vs 3D vs 2+3D
"""

import csv
import time
import numpy as np
import itertools

import Dataset
from Exposer import *
from EEC import *

start = time.time()

# Load dataset
dataset = Dataset('data/iris.csv','iris')

grain = 30
limit = 15
radiuses = xrange(1,40,1)
folds = xrange(0,5)

summary = []

for fold in folds:
	dataset.setCV(fold)
	summary.append([])
	print "\n| %s, fold %i" % (dataset, fold)
	print "RAD\t2D \t3D \t2+3\n---\t---\t---\t---"
	
	for radius_i in radiuses:
		radius = radius_i / 100.

		configuration = {'radius': radius, 'grain': grain, 'limit': limit, 'dimensions': [2]}
		eec = EEC(dataset,configuration,EECApproach.random,ExposerParticipation.theta2)
		eec.predict()
		scores1 = dataset.score()

		configuration = {'radius': radius, 'grain': grain, 'limit': limit, 'dimensions': [3]}
		eec = EEC(dataset,configuration,EECApproach.random,ExposerParticipation.theta2)
		eec.predict()
		scores2 = dataset.score()

		configuration = {'radius': radius, 'grain': grain, 'limit': limit, 'dimensions': [2, 3]}
		eec = EEC(dataset,configuration,EECApproach.random,ExposerParticipation.theta2)
		eec.predict()
		scores3 = dataset.score()

		print "%03i\t%02.0f%%\t%02.0f%%\t%02.0f%%" % \
			(radius_i, \
			scores1['accuracy']*100, \
			scores2['accuracy']*100, \
			scores3['accuracy']*100)

		result = {
			'accuracy1': scores1['accuracy'],
			'accuracy2': scores2['accuracy'],
			'accuracy3': scores3['accuracy']
		}

		summary[fold].append(result)

end = time.time()

print "\n# GENERATING SUMMARY"
filename = "results/experiment_7.csv"
textFile = open(filename, "w")
for index, radius in enumerate(radiuses):
	accumulator = []
	for fold in folds:
		accumulator.append(summary[fold][index])
	
	accuracy1 = sum(e['accuracy1'] for e in accumulator) / len(accumulator)
	accuracy2 = sum(e['accuracy2'] for e in accumulator) / len(accumulator)
	accuracy3 = sum(e['accuracy2'] for e in accumulator) / len(accumulator)
	
	row = "% 3i, %.3f, %.3f, %.3f\n" % (radius, accuracy1, accuracy2, accuracy3)
	textFile.write(row)

textFile.close()

print "%.3f seconds" % (end - start)