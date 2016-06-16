#!/usr/bin/env python

import csv
import time
import numpy as np
import itertools
import sys

import Dataset
from Exposer import *
from EEC import *

start = time.time()

# Load dataset
dataset = Dataset(sys.argv[1],sys.argv[1])

grains = [2, 5, 10]
limits = [1, 5, 10, 50]
radiuses = [5, 15, 30, 100]

fold = 0
dimensionss = [[1], [2], [3], [4], [1,2], [2,3], [3,4], [2,5]]

dataset.setCV(fold)

winning = 0
winner = {}

print "\n| %s, fold %i" % (dataset, fold)
print "RAD GRA LIM\tACC\tBAC\tACC\tBAC\n--- --- ---\t---\t---\t---"
	
for radius_i in radiuses:
	for grain in grains:
		for limit in limits:
			for dimensions in dimensionss:
				radius = radius_i / 100.

				configuration = {'radius': radius, 'grain': grain, 'limit': limit, 'dimensions': dimensions}
				eec = EEC(dataset,configuration,EECApproach.random,ExposerParticipation.lone)
				eec.predict()
				scores = dataset.score()

				if scores['accuracy'] + scores['bac'] > winning:
					winning = scores['accuracy'] + scores['bac']
					winner.update(configuration)
					winner.update(scores)
					print '\n# LEADER\n'

				print "%03i %03i %03i\t%02.2f%%\t%02.2f%% %s" % \
					(radius_i, grain, limit, \
					scores['accuracy']*100, \
					scores['bac']*100, str(dimensions))

end = time.time()

print "%.3f seconds" % (end - start)
print winner 