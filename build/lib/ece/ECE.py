"""
**ECE** is an Exposer Ensemble Classifier.

### Usage

To create an ensemble, all you need is to load a dataset, prepare dictionary with demanded configuration and use them to initiate object.

	dataset = Dataset('data/iris.csv','iris')
	configuration = {
		'radius': radius, 
		'grain': grain, 
		'limit': limit, 
		'dimensions': dimensions,
		'eecApproach': EECApproach.random,
		'exposerParticipation': ExposerParticipation.lone
	}
	ensemble = EEC(dataset,configuration)

For a process of classification you can simply use ensemble to create predictions. Dictionary with scores is provided by a function `score()` being a member of `dataset` object.

	ensemble.predict()
	scores = dataset.score()

"""
from Sample import *
from Dataset import *
from Exposer import *

import itertools
import random

SEED = 123
random.seed(SEED)

# === EEC Approach ===
class ECEApproach(Enum):
	brutal = 1
	random = 2
	heuristic = 3

# === Exposer Ensemble Classifier
class ECE:
	# ==== Preparing an ensemble
	def __init__(self, dataset, configuration):
		self.approach = configuration['eceApproach']
		self.exposerVotingMethod = configuration['exposerVotingMethod']
		self.dimensions = configuration['dimensions']

		self.dataset = dataset
		self.configuration = configuration
		self.combinations = []

		# ===== Brutal approach
		for dimension in self.dimensions:
			given_range = range(0, dataset.features)
			combinations = itertools.combinations(given_range, dimension)
			self.combinations += list(combinations)

		# ===== Random approach		
		if self.approach == ECEApproach.random:
			limit = self.configuration['limit']
			random.shuffle(self.combinations)
			self.combinations = self.combinations[0:limit]

		# ===== Heuristic approach
		if self.approach == ECEApproach.heuristic:
			limit = self.configuration['limit']
			pool = self.configuration['pool']
			random.shuffle(self.combinations)
			self.combinations = self.combinations[0:pool]
			e_pool = []
			for combination in self.combinations:
				configuration = {
					'grain': 4,
					'radius': 1,
					'exposerVotingMethod': ExposerVotingMethod.lone,
					'chosenLambda': list(combination)
				}
				e_pool.append(Exposer(self.dataset,configuration))

			self.combinations = []
			i_pool = []
			for label in xrange(0,self.dataset.classes):
				n_pool = sorted(e_pool, key=lambda exposer: exposer.thetas[label], reverse=True)

				n_pool = n_pool[0:(limit/self.dataset.classes)]

				for exposer in n_pool:
					self.combinations.append((exposer.chosenLambda))
				

	# === Prediction
	def predict(self):
		self.dataset.clearSupports()
		for combination in self.combinations:
			chosen_lambda = list(combination)
			exposerConfiguration = {'chosenLambda': chosen_lambda}
			exposerConfiguration.update(self.configuration)
			exposer = Exposer(self.dataset,exposerConfiguration)
			exposer.predict()
