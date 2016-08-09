# IMPORTS
from utils import getType
import csv
import numpy as np
import random

# SAMPLE
class Sample:
	def __init__(self,features,label):
		# Label is INT
		# Feature vector is float
  		width = len(features)
  		self.label = label
  		self.prediction = 0
  		self.support = None

		# Missing values are None
  		for index, value in enumerate(features):
  			if value == '?':
  				features[index] = None
  		
  		self.features = np.array(features).astype(np.float)

	def decidePrediction(self):
  		self.prediction = np.argmax(self.support)
			