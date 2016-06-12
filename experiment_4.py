#!/usr/bin/env python
"""
Experiment 4

dataset: heart
grain: 10
radius: 100

testing brutal exponers limits from 1:30
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
	print "LIM\tACC\tBAC\n---\t---\t---"

	for limit in limits:
		configuration = {'radius': radius, 'grain': grain, 'limit': limit, 'dimensions': dimensions}
		
		eec = EEC(dataset,configuration,EECApproach.random)
		eec.predict()

		scores = dataset.score()
		print "%03i\t%02.0f%%\t%02.0f%%" % \
			(limit, \
			scores['accuracy']*100, \
			scores['bac']*100)

		summary[fold].append(scores)

end = time.time()

print "\n# GENERATING SUMMARY"
filename = "results/experiment_4.csv"
textFile = open(filename, "w")
for index, limit in enumerate(limits):
	accumulator = []
	for fold in folds:
		accumulator.append(summary[fold][index])
	
	accuracy = sum(e['accuracy'] for e in accumulator) / len(accumulator)
	bac = sum(e['bac'] for e in accumulator) / len(accumulator)
	
	row = "% 3i, %.3f, %.3f\n" % (limit, accuracy, bac)
	textFile.write(row)

textFile.close()


print "%.3f seconds" % (end - start)