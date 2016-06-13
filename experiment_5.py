#!/usr/bin/env python
"""
Experiment 5

dataset: heart
grain: 10
radius: 100

testing random exponers limits from 1:30
with all participations
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
dataset = Dataset('data/heart.csv','heart')

grain = 10
radius = 1
limits = xrange(1,31)
folds = xrange(0,5)
dimensions = [2]

summary = []

for fold in folds:
	dataset.setCV(fold)
	summary.append([])
	print "\n| %s, fold %i" % (dataset, fold)
	print "LIM\tLON\tTH1\tTH2\n---\t---\t---\t---"

	for limit in limits:
		configuration = {'radius': radius, 'grain': grain, 'limit': limit, 'dimensions': dimensions}
		
		eec = EEC(dataset,configuration,EECApproach.random,ExposerParticipation.lone)
		eec.predict()
		scores1 = dataset.score()
		
		eec = EEC(dataset,configuration,EECApproach.random,ExposerParticipation.theta1)
		eec.predict()
		scores2 = dataset.score()

		eec = EEC(dataset,configuration,EECApproach.random,ExposerParticipation.theta2)
		eec.predict()
		scores3 = dataset.score()

		print "%03i\t%02.0f%%\t%02.0f%%\t%02.0f%%" % \
			(limit, \
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
filename = "results/experiment_5.csv"
textFile = open(filename, "w")
for index, limit in enumerate(limits):
	accumulator = []
	for fold in folds:
		accumulator.append(summary[fold][index])
	print accumulator

	accuracy1 = sum(e['accuracy1'] for e in accumulator) / len(accumulator)
	accuracy2 = sum(e['accuracy2'] for e in accumulator) / len(accumulator)
	accuracy3 = sum(e['accuracy3'] for e in accumulator) / len(accumulator)

	row = "% 3i, %.3f, %.3f, %.3f\n" % (limit, accuracy1, accuracy2, accuracy3)
	textFile.write(row)

textFile.close()

print "%.3f seconds" % (end - start)