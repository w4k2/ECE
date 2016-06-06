from Datasets import *
import numpy as np
import math
import operator
import png
import functools

class Exponer(object):
	def __init__(self, dataset, chosen_lambda, grain, radius):
		self.grain = grain
		self.radius = radius
		self.chosen_lambda = chosen_lambda
		self.dbname = dataset.dbname
		self.classes = dataset.classes

		self.matrix = [0] * (grain * grain * self.classes)
		radius_m = int(radius * grain)
		print len(self.matrix)

		# Iterujemy probki
		for sample in dataset.samples:
			label = sample.label
			features = [sample.features[index] for index in chosen_lambda]
			location = np.multiply(features, self.grain).astype(int)
			for x in xrange(location[0]-radius_m,location[0]+radius_m):
				for y in xrange(location[1]-radius_m,location[1]+radius_m):
					if x < 0 or x >= grain or y < 0 or y >= grain:
						continue
					point = [float(x) / grain, float(y) / grain]
					distance = math.sqrt(sum([n**2 for n in map(operator.sub,point,features)]))
					if distance < radius:
						influence = radius - distance
						pos = (y + x * self.grain) * self.classes + label
						self.matrix[pos] += influence

		self.matrix = np.array(self.matrix).reshape(grain**2,-1)
		self.matrix /= np.amax(self.matrix, axis=0)

	def predict(self,dataset):
		for sample in dataset.test:
			features = [sample.features[index] for index in self.chosen_lambda]
			location = np.multiply(features, self.grain).astype(int)
			if location[0] == self.grain:
				location[0] = self.grain - 1
			if location[1] == self.grain:
				location[1] = self.grain - 1
			pos = (location[1] + location[0] * self.grain)
			support = self.matrix[pos]
			sample.prediction = np.argmax(support)
			sample.support = support
		
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
		
