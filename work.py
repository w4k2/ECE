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
dimensialities = xrange(1,4)
folds = xrange(0,1)
grain = 30

start = time.time()

for fold in folds:
	dataset.setCV(fold)

	print "\n| %s, fold %i" % (dataset, fold)
	print "DIM\tACC\tBAC\n---\t---\t---"

	for dimensions in dimensialities:
		configuration = {'radius': .2, 'grain': grain, 'limit': limit, 'dimensions': dimensions, 'pool': pool}
		dataset.clearSupports()
		eec = EEC(dataset,configuration,EECApproach.heuristic,ExposerParticipation.lone)
		eec.predict()

		scores = dataset.score()
		print "%03i\t%02.0f%%\t%02.0f%%" % \
			(dimensions, \
			scores['accuracy']*100, \
			scores['bac']*100)

end = time.time()

print "%.3f seconds" % (end - start)
