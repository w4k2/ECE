#!/usr/bin/env python

import csv
import time
import numpy as np
import itertools
import math

import Dataset
from Exposer import *
from EEC import *

dataset = Dataset('data/iris.csv','iris')

limit = 3
pool = 10
dimensions = [1, 2, 3]
folds = xrange(0,1)
grain = 20
radiuses = xrange(1,30,1)

start = time.time()

for fold in folds:
	dataset.setCV(fold)

	print "\n| %s, fold %i" % (dataset, fold)
	print "RAD\tACC\tBAC\n---\t---\t---"

	for radius_i in radiuses:
		radius = radius_i / 100.
		configuration = {'radius': radius, 'grain': grain, 'limit': limit, 'dimensions': dimensions, 'pool': pool}
		dataset.clearSupports()
		eec = EEC(dataset,configuration)
		eec.predict()

		scores = dataset.score()
		print "%03i\t%02.0f%%\t%02.0f%%" % \
			(radius_i, \
			scores['accuracy']*100, \
			scores['bac']*100)

end = time.time()

print "%.3f seconds" % (end - start)
