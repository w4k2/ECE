"""
**ECE** is an Exposer Ensemble Classifier.

### Usage

To create an ensemble, all you need is to load a dataset, prepare dictionary
with demanded configuration and use them to initiate object.

    dataset = Dataset('data/iris.csv','iris')
    configuration = {
        'radius': radius,
        'grain': grain,
        'limit': limit,
        'dimensions': dimensions,
        'eecApproach': ECEApproach.random,
        'exposerVotingMethod': ExposerVotingMethod.lone
    }
    ensemble = ECE(dataset,configuration)

For a process of classification you can simply use ensemble to create
predictions. Dictionary with scores is provided by a function `score()` being a
member of `dataset` object.

    ensemble.predict()
    scores = dataset.score()

"""
from Exposer import *
from ksskml import Ensemble
from ksskml import Dataset
from ksskml import Sample
from ksskml import utils
import itertools
import random


# ### ECE Approach
# There are three approaches possible to build an ensemble.
class ECEApproach(Enum):
    # With **brutal approach** we use all possible combinations for given
    # dimensionalities.
    brutal = 1
    # An **random approach** uses a set of randomly chosen _exposers_ in a
    # number given by the `limit` parameter.
    random = 2
    # Finally, the **heuristic approach** uses set of exposers in a number
    # given by the `limit` parameter with highest `theta` value from
    # pre-generated pool.
    heuristic = 3


# === Exposer Classifier Ensemble
class ECE(Ensemble):
    # ==== Preparing an ensemble

    def __init__(self, dataset, configuration):
        Ensemble.__init__(self, dataset)
        # First, we're collecting four values from passed configuration:
        #
        # - **approach**, described above,
        # - **voting method**, described in _[Exposer](Exposer.html)_ class,
        # - **dimensions**, used as a vector of possible exposer
        # dimensionalities.
        # - **configuration**, used to configure _exposers_.

        self.approach = configuration['eceApproach']
        self.exposerVotingMethod = ExposerVotingMethod.lone
        if 'exposerVotingMethod' in configuration:
            self.exposerVotingMethod = configuration['exposerVotingMethod']
        self.dimensions = configuration['dimensions']
        self.configuration = configuration
        self.exposers = []

        # Later, we're gathering the dataset and creating empty list of
        # lambdas.
        self.combinations = []

        # ##### Brutal approach
        # For every dimensionality from `dimensions` list we're creating a list
        # of all possible combinations and appending them to the combinations
        # list.
        for dimension in self.dimensions:
            given_range = range(0, dataset.features)
            combinations = itertools.combinations(given_range, dimension)
            self.combinations += list(combinations)

        # ##### Random approach
        # If the random approach is chosen, a list of combinations is limited
        # to a random subset in a number given by `limit` parameter.
        if self.approach == ECEApproach.random:
            limit = self.configuration['limit']
            random.shuffle(self.combinations)
            self.combinations = self.combinations[0:limit]

        # ##### Heuristic approach
        # For the heuristic approach is chosen, a list of combinations is
        # limited to a random subset in a number given by the `limit` parameter
        # , established as pool.
        if self.approach == ECEApproach.heuristic:

            limit = self.configuration['limit']
            pool = self.configuration['pool']
            random.shuffle(self.combinations)
            self.combinations = self.combinations[0:pool]
            e_pool = []

            # Later, for every combination in pool, we create an exposer with
            # grain `4` and radius `1`.
            for combination in self.combinations:
                configuration = {
                    'grain': 4,
                    'radius': 1,
                    'exposerVotingMethod': ExposerVotingMethod.lone,
                    'chosenLambda': list(combination)
                }
                e_pool.append(Exposer(self.dataset, configuration))

            for exposer in e_pool:
                exposer.learn()

            self.combinations = []
            i_pool = []
            # And a limited subset of pool members with highest theta is
            # appended to the list of combinations.
            for label in xrange(0, len(self.dataset.classes)):
                n_pool = sorted(
                    e_pool,
                    key=lambda exposer: exposer.thetas[label],
                    reverse=True)
                n_pool = n_pool[0:(limit / len(self.dataset.classes))]
                for exposer in n_pool:
                    self.combinations.append((exposer.chosenLambda))

        for combination in self.combinations:
            chosen_lambda = list(combination)
            exposerConfiguration = {'chosenLambda': chosen_lambda}
            exposerConfiguration.update(self.configuration)
            exposer = Exposer(self.dataset, exposerConfiguration)
            self.exposers.append(exposer)

    def learn(self):
        for exposer in self.exposers:
            exposer.learn()

    # ### Prediction
    # Prediction in this case is just creating and configuring exposer for
    # every combination from a list and performing the prediction for every
    # member.
    def predict(self):
        self.dataset.clearSupports()
        for exposer in self.exposers:
            exposer.predict()
