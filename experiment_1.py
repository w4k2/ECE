#!/usr/bin/env python
import csv
import time
import numpy as np

import Dataset
from Exponer import *

start = time.time()

dataset = Dataset('data/iris.csv','iris')

chosen_lambda = [2,3]
grain = 15
radiuses = xrange(1,10,1)
folds = xrange(0,5)

summary = []

for fold in folds:
	dataset.setCV(fold)
	summary.append([])
	print "\n| %s, fold %i" % (dataset, fold)
	print "RAD\tACC\tSEN\tSPC\tBAC\n---\t---\t---\t---\t---"
		
	for radius_i in radiuses:
		radius = radius_i / 100.
		exponer = Exponer(dataset, chosen_lambda, grain, radius)

		dataset.clearSupports()
		predictions = exponer.predict(dataset)
		scores = dataset.score()
		print "%03i\t%02.0f%%\t%02.0f%%\t%02.0f%%\t%02.0f%%" % \
			(radius_i, \
			scores['accuracy']*100, \
			scores['sensitivity']*100, \
			scores['specificity']*100, \
			scores['bac']*100)

		summary[fold].append(scores)
	#	print "score %.2f" % scores['accuracy']

end = time.time()

print "%.3f seconds" % (end - start)