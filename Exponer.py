from Datasets import *
import numpy as np
import math
import operator
import png

class Exponer(object):
	def __init__(self, dataset, feature_x, feature_y, grain, radius):
		self.grain = grain
		self.radius = radius
		self.feature_x = feature_x
		self.feature_y = feature_y
		self.dbname = dataset.dbname
		self.classes = dataset.classes

		self.matrix = []

		radius_vector = np.array([radius, radius])
		
		for y in xrange(0,grain):
			for x in xrange(0,grain):

				real_vector = np.array([x, y]) / float(grain)
				low = real_vector - radius_vector
				high = real_vector + radius_vector

				brightness = [0] * dataset.classes

				for sample in dataset.samples:
					features = sample.features
					cmp_vector = np.array([features[feature_x], features[feature_y]])

					if 	all(cmp_vector > low) and all(cmp_vector < high):
						distance = math.sqrt(sum(pow(cmp_vector - real_vector,2)))
						if distance < radius:
							brightness[sample.label] += radius - distance

				self.matrix += [brightness]

		maxi = np.amax(self.matrix, axis=0)
		self.matrix /= maxi

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
		
