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
		self.dbname = wisepath[len(wisepath)-2]
		self.source_samples = []
	  	self.test = []
	  	self.hasHeader = False
	  	self.header = []

		self.classes = -1
		classesHash = {}
		with open(filename, 'rb') as file:
			csvDataset = csv.reader(file, delimiter=',')
			for row in csvDataset:
				if getType(row[0]) == str:
					self.hasHeader = True
					self.header = row
				else:
					label = row[-1]
					features = row[0:-1]
					if not label in classesHash:
						self.classes += 1
						classesHash.update({label: self.classes})
					self.source_samples.append(Sample(features,classesHash[label]))
		self.classes += 1

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

		#print minimum
		#print maximum

		foo = maximum - minimum

		#print foo
		# O tu sobie poradzmy z 0/0
		for index, value in enumerate(foo):
			if value == 0:
				foo[index] = 1

		for sample in self.source_samples:
			for index, feature in enumerate(sample.features):
				if not np.isnan(feature):
					normalizedFeature = (feature - minimum[index]) / foo[index]
					#print "%f -> %f" % (feature, normalizedFeature)
					sample.features[index] = normalizedFeature
