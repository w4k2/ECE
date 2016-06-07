from Sample import *
from Dataset import *
from Exponer import *

import itertools

class EECApproach(Enum):
	brutal = 1
	random = 2
	heuristic = 3

class EEC:
	def __init__(self, dataset, configuration = {}, approach = EECApproach.brutal):
		self.dataset = dataset
		self.approach = approach
		self.configuration = configuration
		self.combinations = list(itertools.combinations(range(0, dataset.features), 2))
		
	def __str__(self):
		return "Ensemble on %s, with %s approach on %i lambdas\nConfigured with: %s" % (self.dataset, self.approach, len(self.combinations), self.configuration)

	def predict(self):
		self.dataset.clearSupports()
		for combination in self.combinations:
			chosen_lambda = list(combination)
			exponer = Exponer(self.dataset,chosen_lambda,self.configuration)
			exponer.predict()