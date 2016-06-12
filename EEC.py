from Sample import *
from Dataset import *
from Exposer import *

import itertools
import random

SEED = 123
random.seed(SEED)

class EECApproach(Enum):
	brutal = 1
	random = 2
	heuristic = 3

class EEC:
	def __init__(self, dataset, configuration = {}, approach = EECApproach.brutal, exposerParticipation = ExposerParticipation.lone):
		self.dataset = dataset
		self.approach = approach
		self.configuration = configuration
		self.exposerParticipation = exposerParticipation
		self.dimensions = configuration['dimensions']
		self.combinations = list(itertools.combinations(range(0, dataset.features), self.dimensions))
		
		if approach == EECApproach.random:
			limit = self.configuration['limit']
			random.shuffle(self.combinations)
			self.combinations = self.combinations[0:limit]

		if approach == EECApproach.heuristic:
			limit = self.configuration['limit']
			pool = self.configuration['pool']
			random.shuffle(self.combinations)
			self.combinations = self.combinations[0:pool]
			little_exposers = []
			for combination in self.combinations:
				chosen_lambda = list(combination)
				little_exposer = Exposer(self.dataset,chosen_lambda,{'grain': 4, 'radius': 1})
				little_exposers.append(little_exposer)
			little_exposers = sorted(little_exposers, key=lambda exposer: exposer.theta, reverse=True)
			self.combinations = []
			little_exposers = little_exposers[0:limit]
			for little_exposer in little_exposers:
				self.combinations.append((little_exposer.chosen_lambda))

	def __str__(self):
		return "Ensemble on %s, with %s approach on %i lambdas\nConfigured with: %s" % (self.dataset, self.approach, len(self.combinations), self.configuration)

	def predict(self):
		self.dataset.clearSupports()
		for combination in self.combinations:
			chosen_lambda = list(combination)
			exposer = Exposer(self.dataset,chosen_lambda,self.configuration,self.exposerParticipation)
			exposer.predict()