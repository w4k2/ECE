#!/usr/bin/env python

import csv
import time
import numpy as np
import itertools
import math

import Dataset
from Exposer import *
from EEC import *

dataset = Dataset('data/heart.csv','heart')

fold = 0
limits = xrange(1,10)
dataset.setCV(fold)

print "\n| %s, fold %i" % (dataset, fold)
print "LIM\tACC\tBAC\n---\t---\t---"

for limit in limits:
	configuration = {'radius': 0.1, 'grain': 20, 'limit': limit, 'dimensions': 2}
			
	eec = EEC(dataset,configuration,EECApproach.random)
	eec.predict()

	scores = dataset.score()
	print "%03i\t%02.0f%%\t%02.0f%%" % \
		(limit, \
		scores['accuracy']*100, \
		scores['bac']*100)
