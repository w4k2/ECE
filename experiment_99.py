#!/usr/bin/env python
"""
Experiment 6

dataset: heart
grain: 20
exponers: brutal exposers with limit 8

testing radiuses in 1:30
2D vs 3D
"""

import csv
import time
import numpy as np
import itertools

import Dataset
from Exposer import *
from EEC import *

grain = 30
limit = 15
radiuses = xrange(1,31,1)
folds = xrange(0,5)

with open('datasets.csv', 'rb') as file:
	csvDataset = csv.reader(file, delimiter=',', quotechar='\'')
	for row in csvDataset:
		start = time.time()

		filename = row[0]
		dbname = row[1]
		dataset = Dataset('data/' + filename, dbname)
		print dataset

		summary = []

		for fold in folds:
			dataset.setCV(fold)
			summary.append([])
			print "\n| %s, fold %i" % (dataset, fold)
			print "RAD\tACC\tBAC\n---\t---\t---"

			for radius_i in radiuses:
				radius = radius_i / 100.

				configuration = {'radius': radius, 'grain': grain, 'limit': limit, 'dimensions': [2]}

				eec = EEC(dataset,configuration,EECApproach.random)
				eec.predict()
				scores = dataset.score()

				print "%03i\t%02.0f%%\t%02.0f%%" % \
					(radius_i, \
					scores['accuracy']*100, \
					scores['bac']*100)

				summary[fold].append(scores)

		print "\n# GENERATING SUMMARY"
		filename = "results/results_99_%s.csv" % dataset.dbname
		textFile = open(filename, "w")
		for index, radius in enumerate(radiuses):
			accumulator = []
			for fold in folds:
				accumulator.append(summary[fold][index])
			
			accuracy = sum(e['accuracy'] for e in accumulator) / len(accumulator)
			bac = sum(e['bac'] for e in accumulator) / len(accumulator)
			
			row = "% 3i, %.3f, %.3f\n" % (radius, accuracy, bac)
			textFile.write(row)

		textFile.close()

		end = time.time()

		print "%.3f seconds" % (end - start)

