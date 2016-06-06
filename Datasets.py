# IMPORTS
import csv
import numpy as np

# SAMPLE
class Sample:

  def __init__(self,row):
  	width = len(row)
  	self.label = int(row[width - 1])
  	self.prediction = 0
  	self.features = np.array(row[0:width - 1]).astype(np.float)
  	
  def __str__(self):
  	return "CLASS " + str(self.label) + ", of " + str(len(self.features)) + " features"
  	
# DATASET
class Dataset:
	def __init__(self, filename, dbname):
		self.dbname = dbname
		self.samples = []
	  	self.classes = 0
		with open(filename, 'rb') as file:
			csvDataset = csv.reader(file, delimiter=',')
			for row in csvDataset:
				self.samples.append(Sample(row))
		self.normalize()
		for sample in self.samples:
			if sample.label > self.classes:
				self.classes = sample.label
		self.classes += 1

	def __str__(self):
		return self.dbname + " dataset with " + str(len(self.samples)) + " samples of " + str(len(self.samples[0].features)) + " features in " + str(self.classes) + " classes"

	def normalize(self):
		minimum = np.array(self.samples[0].features)
		maximum = np.array(self.samples[0].features)

		for sample in self.samples:
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

#		print "MIN: " + str(minimum)
#		print "MAX: " + str(maximum)
#		print "DIF: " + str(foo)		

		for sample in self.samples:
			sample.features = (sample.features - minimum) / foo
