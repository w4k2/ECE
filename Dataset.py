from Sample import *
import csv
import numpy as np
import random

SEED = 123
FOLDS = 5
random.seed(SEED)
  	
# DATASET
class Dataset:
	def __init__(self, filename, dbname):
		# Load db
		self.dbname = dbname
		self.source_samples = []
	  	self.classes = 0
	  	self.test = []
		with open(filename, 'rb') as file:
			csvDataset = csv.reader(file, delimiter=',')
			for row in csvDataset:
				self.source_samples.append(Sample(row))

		# normalize
		self.normalize()

		# Count classes
		for sample in self.source_samples:
			if sample.label > self.classes:
				self.classes = sample.label
		self.classes += 1
	  	self.features = len(self.source_samples[0].features)

	  	# Set base sample set
	  	self.samples = self.source_samples

	  	# Prepare CV
	  	indexes = range(0, len(self.source_samples))
		random.shuffle(indexes)

		self.cv = []
		for index, value in enumerate(indexes):
			self.cv.append((value, index % FOLDS))

	def setCV(self,fold):
		self.samples = []
		self.test = []
		for pair in self.cv:
			if pair[1] == fold:
				self.samples.append(self.source_samples[pair[0]])
			else:
				self.test.append(self.source_samples[pair[0]]);

	def score(self):
		hit = 0
		for sample in self.test:
			if sample.prediction == sample.label:
				hit += 1

		accuracy = float(hit) / float(len(self.test))

		print "Accuracy = %.3f" % accuracy

	def normalize(self):
		minimum = np.array(self.source_samples[0].features)
		maximum = np.array(self.source_samples[0].features)

		for sample in self.source_samples:
			for index, value in enumerate(sample.features):
				if value < minimum[index]:
					minimum[index] = value
				if value > maximum[index]:
					maximum[index] = value

		foo = maximum - minimum

		# O tu sobie poradzmy z 0/0
		for index, value in enumerate(foo):
			if value == 0:
				foo[index] = 1

		for sample in self.source_samples:
			sample.features = (sample.features - minimum) / foo
