from Sample import *
import csv
import numpy as np
import random

np.seterr(divide='ignore', invalid='ignore')

SEED = 123
FOLDS = 5
random.seed(SEED)
  	
# DATASET
class Dataset:
	def __init__(self, filename, dbname, resample = 0):
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

		# dumb resampling
		if resample:
			random.shuffle(self.source_samples)
			self.source_samples = self.source_samples[0:resample]

		# Count classes
		for sample in self.source_samples:
			if sample.label > self.classes:
				self.classes = sample.label
		self.classes += 1
	  	self.features = len(self.source_samples[0].features)

	  	# Initialize supports
	  	self.clearSupports()

	  	# Set base sample set
	  	self.samples = self.source_samples

	  	# Prepare CV
	  	indexes = range(0, len(self.source_samples))
		random.shuffle(indexes)

		self.cv = []
		for index, value in enumerate(indexes):
			self.cv.append((value, index % FOLDS))

	def clearSupports(self):
		for sample in self.source_samples:
			sample.support = np.zeros(self.classes)

	def __str__(self):
		return "%s dataset" % (self.dbname)

	def setCV(self,fold):
		self.samples = []
		self.test = []
		for pair in self.cv:
			if pair[1] == fold:
				self.samples.append(self.source_samples[pair[0]])
			else:
				self.test.append(self.source_samples[pair[0]]);

	def score(self):
		# https://en.wikipedia.org/wiki/Confusion_matrix
		confusion_matrix = np.zeros((self.classes,self.classes)).astype(int)

		for sample in self.test:
			confusion_matrix[sample.label,sample.prediction] += 1

		true_positives = np.zeros(self.classes).astype(float)
		false_negatives = np.zeros(self.classes).astype(float)
		false_positives = np.zeros(self.classes).astype(float)
		true_negatives = np.zeros(self.classes).astype(float)
		
		for pro in xrange(0,self.classes):
			true_positives[pro] += confusion_matrix[pro,pro]
			for contra in xrange(0,self.classes):
				if pro == contra: continue
				false_negatives[pro] += confusion_matrix[pro,contra]
				false_positives[pro] += confusion_matrix[contra,pro]
			true_negatives[pro] = sum(sum(confusion_matrix)) - true_positives[pro] - false_negatives[pro] - false_positives[pro]

		sensitivity = true_positives / (true_positives + false_negatives)
		specificity = true_negatives / (false_positives + true_negatives)
		ppv = true_positives / (true_positives + false_positives)
		npv = true_negatives / (true_negatives + false_negatives)
		bac = (sensitivity + specificity) / 2 

		acc = sum(true_positives + true_negatives) / sum(true_positives + true_negatives + false_positives + false_negatives)

		scores = \
		{
			'sensitivity': sensitivity.mean(),
			'specificity': specificity.mean(),
			'ppv': ppv.mean(),
			'npv': npv.mean(),
			'accuracy': acc,
			'bac': bac.mean()
		}

		return scores

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
