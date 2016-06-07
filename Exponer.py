from Dataset import *

from enum import Enum
import numpy as np
import math
import operator
import png
import functools

class ExponerParticipation(Enum):
	lone = 1
	theta1 = 2
	theta2 = 3

class Exponer(object):
	def __init__(self, dataset, chosen_lambda, configuration, exponerParticipation = ExponerParticipation.lone):
		self.dataset = dataset
		self.exponerParticipation = exponerParticipation
		self.configuration = configuration
		self.grain = configuration['grain']
		self.radius = configuration['radius']
		self.chosen_lambda = chosen_lambda
		self.dbname = dataset.dbname
		self.classes = dataset.classes

		self.matrix = [0] * (self.grain * self.grain * self.classes)
		radius_m = int(self.radius * self.grain)

		# Iterujemy probki
		for sample in dataset.samples:
			label = sample.label
			features = [sample.features[index] for index in chosen_lambda]
			location = np.multiply(features, self.grain).astype(int)
			for x in xrange(location[0]-radius_m,location[0]+radius_m):
				for y in xrange(location[1]-radius_m,location[1]+radius_m):
					if x < 0 or x >= self.grain or y < 0 or y >= self.grain:
						continue
					point = [float(x) / self.grain, float(y) / self.grain]
					distance = math.sqrt(sum([n**2 for n in map(operator.sub,point,features)]))
					if distance < self.radius:
						influence = self.radius - distance
						pos = (y + x * self.grain) * self.classes + label
						self.matrix[pos] += influence

		self.matrix = np.array(self.matrix).reshape(self.grain**2,-1)
		self.matrix /= np.amax(self.matrix, axis=0)

	def predict(self):
		for sample in self.dataset.test:
			features = [sample.features[index] for index in self.chosen_lambda]
			location = np.multiply(features, self.grain).astype(int)
			if location[0] == self.grain:
				location[0] = self.grain - 1
			if location[1] == self.grain:
				location[1] = self.grain - 1
			pos = (location[1] + location[0] * self.grain)
			support = self.matrix[pos]

			if self.exponerParticipation == ExponerParticipation.lone:
				sample.support += support

			sample.decidePrediction()
		
		return 0

	def png(self,filename):
		image = []
		for y in xrange(0,self.grain):
			row = ()
			for x in xrange(0,self.grain):
				pos = x + y * self.grain
				pix = np.array(self.matrix[pos] * 255).astype(int)
				tup = tuple(pix)
				row += tup
			image += [row]
		
		f = open(filename, 'wb')
		w = png.Writer(self.grain, self.grain)
		w.write(f, image) ; f.close()

	def decisionPNG(self,filename):
		image = []
		for y in xrange(0,self.grain):
			row = ()
			for x in xrange(0,self.grain):
				pos = x + y * self.grain
				pix = np.array(self.matrix[pos] * 255).astype(int)
				decision = np.argmax(pix)
				for index, value in enumerate(pix):
					if index == decision:
						pix[index] = 128 + value/2
					else:
						pix[index] = 0
				#print decision
				tup = tuple(pix)
				row += tup
			image += [row]
		
		f = open(filename, 'wb')
		w = png.Writer(self.grain, self.grain)
		w.write(f, image) ; f.close()
		
