from Sample import *
from utils import getType
import csv
import numpy as np
import random
import re

np.seterr(divide='ignore', invalid='ignore')

SEED = 123
FOLDS = 5
random.seed(SEED)

# DATASET
class Dataset:
	def __init__(self, filename, resample = 0):
		# Load db
		wisepath = re.findall(r"[\w']+", filename)
		self.db_name = wisepath[len(wisepath)-2]
		self.source_samples = []
	  	self.test = []
	  	self.has_header = False
	  	self.header = []
	  	self.confusion_matrix = []

		self.classes = {}
		with open(filename, 'rb') as file:
			csvDataset = csv.reader(file, delimiter=',')
			for row in csvDataset:
				if getType(row[0]) == str:
					self.hasHeader = True
					self.header = row
				else:
					label = row[-1]
					features = row[0:-1]
					if not label in self.classes:
						self.classes.update({label: len(self.classes)})
					self.source_samples.append(Sample(features,self.classes[label]))

		# normalize
		self.normalize()

		# dumb resampling
		if resample:
			random.shuffle(self.source_samples)
			self.source_samples = self.source_samples[0:resample]

		# Count features
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
			sample.support = np.zeros(len(self.classes))

	def __str__(self):
		return "%s dataset" % (self.db_name)

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
		self.confusion_matrix = np.zeros((len(self.classes),len(self.classes))).astype(int)

		for sample in self.test:
			self.confusion_matrix[sample.label,sample.prediction] += 1

		true_positives = np.zeros(len(self.classes)).astype(float)
		false_negatives = np.zeros(len(self.classes)).astype(float)
		false_positives = np.zeros(len(self.classes)).astype(float)
		true_negatives = np.zeros(len(self.classes)).astype(float)
		
		for pro in xrange(0,len(self.classes)):
			true_positives[pro] += self.confusion_matrix[pro,pro]
			for contra in xrange(0,len(self.classes)):
				if pro == contra: continue
				false_negatives[pro] += self.confusion_matrix[pro,contra]
				false_positives[pro] += self.confusion_matrix[contra,pro]
			true_negatives[pro] = sum(sum(self.confusion_matrix)) - true_positives[pro] - false_negatives[pro] - false_positives[pro]

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
		example = np.array(self.source_samples[0].features)		
		# Check if there are any NaN's
		for index, value in enumerate(example):
			if np.isnan(value):
				for sample in self.source_samples:
					if not np.isnan(sample.features[index]):
						example[index] = sample.features[index]
						break

		minimum = np.array(list(example))
		maximum = np.array(list(example))

		for index, sample in enumerate(self.source_samples):
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
			for index, feature in enumerate(sample.features):
				if not np.isnan(feature):
					normalizedFeature = (feature - minimum[index]) / foo[index]
					sample.features[index] = normalizedFeature
