#!/usr/bin/env python
import csv
import time

from Datasets import *
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

	#for sample in dataset.test:
	#	print "%s @ %i (%i)" % (str(sample.support), sample.prediction, sample.label)


"""
with open('datasets.csv', 'rb') as file:
	csvDataset = csv.reader(file, delimiter=',', quotechar='\'')
	for row in csvDataset:
		filename = row[0]
		dbname = row[1]
		dataset = Dataset('data/' + filename, dbname)
		print dataset
		chosen_lambda = [0,1]
		for x in xrange(0,15):
			exponer = Exponer(dataset, chosen_lambda, 30, 0.1)


end = time.time()
print "%.3f seconds" % (end - start)
"""