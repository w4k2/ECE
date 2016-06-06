#!/usr/bin/env python
import csv
import time

import Dataset
from Exponer import *

start = time.time()

filename = 'data/iris.csv'
dbname = 'iris'
dataset = Dataset(filename,dbname)
print dataset

chosen_lambda = [2,3]
grain = 30
radius = .2

exponer = Exponer(dataset, chosen_lambda, grain, radius)

for x in xrange(0,5):
	dataset.setCV(x)
	exponer = Exponer(dataset, chosen_lambda, grain, radius)
	predictions = exponer.predict(dataset)

	dataset.score()

end = time.time()
print "%.3f seconds" % (end - start)