from Dataset import *

from enum import Enum
import numpy as np
import math
import operator
import png
import functools

class ExposerParticipation(Enum):
	lone = 1
	theta1 = 2
	theta2 = 3

class Exposer(object):
	def __init__(self, dataset, chosen_lambda, configuration, exposerParticipation = ExposerParticipation.lone):
		self.dataset = dataset
		self.exposerParticipation = exposerParticipation
		self.configuration = configuration
		
		self.grain = configuration['grain']
		self.radius = configuration['radius']
		self.dimensions = len(chosen_lambda)

		self.chosen_lambda = chosen_lambda
		self.dbname = dataset.dbname
		self.classes = dataset.classes

		self.matrix = [0] * (int) (math.pow(self.grain,self.dimensions) * self.classes)
		radius_m = int(self.radius * self.grain)

		base_vectors = self.base_vectors(radius_m)

		# Iterujemy probki
		for sample in dataset.samples:
			label = sample.label
			features = [sample.features[index] for index in chosen_lambda]
			location = np.multiply(features, self.grain).astype(int)

			for base_vector in base_vectors:
				vector = map(operator.add, base_vector, location)
				overflow = False
				for i in xrange(0,self.dimensions):
					if vector[i] < 0 or vector[i] >= self.grain:
						overflow = True
						continue
				if overflow:
					continue

				point = np.array(vector).astype(float) / self.grain
				distance = math.sqrt(sum([n**2 for n in map(operator.sub,point,features)]))
				if distance < self.radius:
					influence = self.radius - distance
					pos = self.position(vector,label)
					self.matrix[pos] += influence

		self.matrix = np.array(self.matrix).reshape(self.grain**self.dimensions,-1)
		self.matrix /= np.amax(self.matrix, axis=0)

	def base_vectors(self,radius_m):
		g = 2 * radius_m + 1
		gross = pow(g,self.dimensions)
		move = [- radius_m] * self.dimensions

		v = [-1] * self.dimensions
		z = [1] * self.dimensions

		for i in xrange(1,self.dimensions):
			z[i] = z[i-1] * g

		base_vectors = []
		for i in xrange(0,gross):
			for j in xrange(0, self.dimensions):
				if i % z[j] == 0:
					v[j] += 1
				if v[j] == g:
					v[j] = 0
			u = map(operator.add, v, move)
			base_vectors.append(list(u))

		return base_vectors
			
	def position(self,p,label=0):
		acc = 0
		g = 1
		for i in xrange(1,self.dimensions+1):
			acc += p[i-1] * g
		#	print "Step %i: p%i = %i, g%i = %i, acc = %i" % (i, i-1, p[i-1], i-1, g, acc)
			g *= self.grain
		#print "Result %i" % (label + self.classes * acc)
		return label + self.classes * acc

	def predict(self):
		for sample in self.dataset.test:
			features = [sample.features[index] for index in self.chosen_lambda]
			location = np.multiply(features, self.grain).astype(int)
			for index, element in enumerate(location):
				if location[index] == self.grain:
					location[index] = self.grain - 1

			pos = self.position(location) / self.classes
			support = self.matrix[pos]

			#print support

			if self.exposerParticipation == ExposerParticipation.lone:
				sample.support += support

			sample.decidePrediction()
		
		return 0

	def png(self,filename):
		image = []
		for y in xrange(0,self.grain):
			row = ()
			for x in xrange(0,self.grain):
				pos = x + y * self.grain
				pos = self,position([x, y])
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
		
