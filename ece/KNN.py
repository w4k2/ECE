from Dataset import *
from Classifier import *

from enum import Enum
import numpy as np
import math
import operator
import png
import functools
import colorsys

class KNN(Classifier):
	def __init__(self, dataset, configuration):
		Classifier.__init__(self,dataset)
		self.k = configuration['k']

	# === Learning ===
	def learn(self):
		pass

	def predict(self):
		for sample in self.dataset.test:
			winners = []
			entry_threshold = 2
			for source in self.dataset.samples:
				distance = np.linalg.norm(sample.features-source.features)
				if distance < entry_threshold:
					winners.append((source, distance))

				if len(winners) > self.k:
					winners.sort(key=lambda distance: distance[1])
					winners = winners[0:self.k]
					entry_threshold = winners[-1][1]

			for winner in winners:
				sample.support[winner[0].label] += 1 #.705 - winner[1]
			
			sample.decidePrediction()
