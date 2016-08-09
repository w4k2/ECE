from abc import ABCMeta, abstractmethod

class Classifier:
	__metaclass__ = ABCMeta
	def __init__(self, dataset):
		# we're gathering the dataset
		self.dataset = dataset
		self.model = []

	@abstractmethod
	def predict():
		pass

	@abstractmethod
	def learn():
		pass
		