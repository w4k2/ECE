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
		self.dataset = dataset 								# Zbior danych
		self.exposerParticipation = exposerParticipation 	# Udzial wag w glosowaniu
		self.grain = configuration['grain']					# Liczba kwantow
		self.radius = configuration['radius']				# Promien oddzialywania
		self.chosen_lambda = chosen_lambda					# Wektor cech
		self.dimensions = len(self.chosen_lambda)			# Liczba wymiarow

		# Tworzymy pusta macierz
		self.matrix = [0] * (int) (math.pow(self.grain,self.dimensions) * self.dataset.classes)
		
		# Wektor pomocniczy do wyliczania pozycji
		self.g = [1] * self.dimensions
		for i in xrange(1,self.dimensions):
			self.g[i] = self.g[i-1] * self.grain
				
		# Naswietlamy macierz
		radius_m = int(self.radius * self.grain)
		base_vectors = self.base_vectors(radius_m)
		for sample in dataset.samples:
			label = sample.label
			features = [sample.features[index] for index in chosen_lambda]
			location = np.multiply(features, self.grain).astype(int)

			for base_vector in base_vectors:
				vector = map(operator.add, base_vector[0], location)
				overflow = False
				for i in xrange(0,self.dimensions):
					if vector[i] < 0 or vector[i] >= self.grain:
						overflow = True
						continue
				if overflow:
					continue

				influence = base_vector[1]
				pos = self.position(vector,label)
				self.matrix[pos] += influence

		self.matrix = np.array(self.matrix).reshape(self.grain**self.dimensions,-1)
		self.matrix /= np.amax(self.matrix, axis=0)

		# Wyliczamy thety
		self.thetas = [0] * self.dataset.classes
		thetas_count = [1] * self.dataset.classes

		treshold = .5
		for vector in self.matrix:
			#print vector
			for index, value in enumerate(vector):
				if value > treshold:
					t = np.sum(vector) - value
					self.thetas[index] += t
					thetas_count[index] += 1
		self.thetas = map(operator.div, self.thetas, thetas_count)
		self.theta = np.amin(self.thetas)
#		print "thetas = %s [%f]" % (self.thetas, self.theta)
#		print "thetas c = %s" % thetas_count


	def base_vectors(self,radius_m):
		# Tym przyspieszymy sobie algorytm
		# Dziala tak samo, a jedyny negatywny skutek to skokowosc w promieniu.

		g = 2 * radius_m + 1
		gross = pow(g,self.dimensions)
		move = [- radius_m] * self.dimensions

		point = [0] * self.dimensions

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
			distance = math.sqrt(sum([n**2 for n in map(operator.sub,point,u)]))
			if distance < radius_m:
				base_vectors.append((list(u), (radius_m - distance)/radius_m))

		return base_vectors
			
	def position(self,p,label=0):
		acc = 0
		for i in xrange(1,self.dimensions+1):
			acc += p[i-1] * self.g[i-1]
		return label + self.dataset.classes * acc

	def predict(self):
		for sample in self.dataset.test:
			features = [sample.features[index] for index in self.chosen_lambda]
			location = np.multiply(features, self.grain).astype(int)
			for index, element in enumerate(location):
				if location[index] == self.grain:
					location[index] = self.grain - 1

			pos = self.position(location) / self.dataset.classes
			support = self.matrix[pos]

			if self.exposerParticipation == ExposerParticipation.lone:
				sample.support += support

			if self.exposerParticipation == ExposerParticipation.theta1:
				sample.support += self.theta * np.array(support)

			if self.exposerParticipation == ExposerParticipation.theta2:
				sample.support += map(operator.mul, self.thetas, support)

			sample.decidePrediction()
		
		return 0

	def png(self,filename):
		image = []
		for y in xrange(0,self.grain):
			row = ()
			for x in xrange(0,self.grain):
				pos = x + y * self.grain
				pos = self.position([x, y])
				pix = np.array(self.matrix[pos/self.classes] * 255).astype(int)
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
