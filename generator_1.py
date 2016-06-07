#!/usr/bin/env python
import csv
import time
import itertools

from Dataset import *
from Exponer import *

start = time.time()

filename = 'data/iris.csv'
dbname = 'iris'
dataset = Dataset(filename,dbname)
print dataset

grain = 350
radius = 0.1

combinations = itertools.permutations(range(0, dataset.features), 2)	

for chosen_lambda in combinations:	
	print chosen_lambda
	exponer = Exponer(dataset, chosen_lambda, grain, radius)
	exponer.png("exponer_%s_%i_%i_g_%i_r_%03i.png" % (dbname, chosen_lambda[0] + 1, chosen_lambda[1] + 1, grain, radius * 1000))

for x in xrange(0,dataset.features):
	exponer = Exponer(dataset, [x, x], grain, radius)
	exponer.png("exponer_%s_%i_%i_g_%i_r_%03i.png" % (dbname, x + 1, x + 1, grain, radius * 1000))

grain = 75
chosen_lambda = [2, 3]

for radius_i in xrange(25,475,25):
	radius = radius_i / float(1000)	
	print chosen_lambda
	exponer = Exponer(dataset, chosen_lambda, grain, radius)
	exponer.png("exponer_%s_%i_%i_g_%i_r_%03i.png" % (dbname, chosen_lambda[0] + 1, chosen_lambda[1] + 1, grain, radius * 1000))
