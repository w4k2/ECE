#!/usr/bin/env python
import csv

from Datasets import *
from Exponer import *

filename = 'data/iris.csv'
dbname = 'iris'
dataset = Dataset(filename,dbname)
print dataset

feature_x = 1
feature_y = 3
grain = 50
radius = 0.1

exponer = Exponer(dataset, feature_x, feature_y, grain, radius)

exponer.png("swatch.png")

"""
datasets = []

with open('datasets.csv', 'rb') as file:
	csvDataset = csv.reader(file, delimiter=',', quotechar='\'')
	for row in csvDataset:
		filename = row[0]
		dbname = row[1]
		datasets.append(Dataset('data/' + filename, dbname))

for dataset in datasets:
	print dataset
"""

