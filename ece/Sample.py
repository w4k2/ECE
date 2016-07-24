# IMPORTS
import csv
import numpy as np
import random

# SAMPLE
class Sample:

	def __init__(self,row):
  		width = len(row)
  		self.label = int(row[width - 1])
  		self.prediction = 0
  		self.support = None
  		self.features = np.array(row[0:width - 1]).astype(np.float)

	def decidePrediction(self):
  		self.prediction = np.argmax(self.support)
			