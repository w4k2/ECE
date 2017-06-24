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
from weles import Ensemble
from weles import Dataset
from weles import Sample
from weles import utils
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

    def __init__(self, dataset, selection=None, scales=None, approach = 1, votingMethod = 1, dimensions = [2], grain = 20, radius = .25, limit = 15, pool = 30, resample = 10000):
        Ensemble.__init__(self, dataset)
        # First, we're collecting four values from passed configuration:
        #
        # - **approach**, described above,
        # - **voting method**, described in _[Exposer](Exposer.html)_ class,
        # - **dimensions**, used as a vector of possible exposer
        # dimensionalities.
        # - **configuration**, used to configure _exposers_.

        self.approach = approach
        self.exposerVotingMethod = votingMethod
        self.dimensions = dimensions
        self.grain = grain
        self.radius = radius
        self.limit = limit
        self.pool = pool
        self.resample = resample

        self.exposers = []
        self.dataset = dataset
        self.selection = selection
        self.scales = scales

        # Later, we're gathering the dataset and creating empty list of
        # lambdas.
        self.combinations = self.composeEnsemble()

        # ##### Brutal approach
        # For every dimensionality from `dimensions` list we're creating a list
        # of all possible combinations and appending them to the combinations
        # list.

    @classmethod
    def cfgTag(cls, ds, approach = 1, votingMethod = 1, dimensions = [2], grain = 5, radius = .1, limit = 15, pool = 30):
        return 'ece_ds_%s_app_%i_vm_%i_dim_%s_g_%i_r_%i_l_%i_p_%i' % (
            ds.db_name,
            approach,
            votingMethod,
            dimensions,
            grain,
            int(1000 * radius),
            limit,
            pool
        )

    def composeEnsemble(self):
        combinations = []
        given_range = range(0, self.dataset.features)
        for dimension in self.dimensions:
            if self.selection:
                combinations += list(
                    itertools.combinations(self.selection, dimension))
            else:
                combinations += list(
                    itertools.combinations(given_range, dimension))

        #print '# Starting combinations'
        #print combinations

        #print '# Using approach %i' % self.approach
        if not self.approach == 1:  # Not brutal
            random.shuffle(combinations)

            #print '# Tossed combinations'
            #print combinations

            # ##### Random approach
            # If the random approach is chosen, a list of combinations is
            # limited to a random subset in a number given by `limit` parameter
            if self.approach == 2: # Is random
                combinations = combinations[0:self.limit]

                #print '# Limited combinations'
                #print combinations

            # ##### Heuristic approach
            # For the heuristic approach is chosen, a list of combinations is
            # limited to a random subset in a number given by the `limit`
            # parameter, established as pool.
            else:
                combinations = combinations[0:self.pool]

                #print '# Pool of combinations'
                #print combinations

                # Later, for every combination in pool, we create an exposer
                # with grain `4` and radius `1`.
                e_pool = [
                    Exposer(
                        dataset = self.dataset,
                        grain = 5,
                        radius = 1,
                        votingMethod = 1,
                        chosenLambda = combination,
                        resample = self.resample
                    )
                    for combination in combinations
                ]
                for exposer in e_pool:
                    exposer.learn()

                #for exposer in e_pool:
                #    print exposer

                rank = {}
                for c in combinations:
                    rank.update({c: 0})

                combinations = []
                # And a limited subset of pool members with highest theta is
                # appended to the list of combinations.
                for label in xrange(len(self.dataset.classes)):
                    n_pool = sorted(
                        e_pool,
                        key=lambda exposer: exposer.thetas[label],
                        reverse=True)
                    #print '\t# Votes for label %i' % label
                    #print '\t%s' % (['%.3f' % e.thetas[label] for e in n_pool])
                    #print '\t%s' % [e.chosenLambda for e in n_pool]
                    for i, e in enumerate(n_pool):
                        combination = e.chosenLambda
                        theta = e.thetas[label]
                        position = i + 1
                        score = (self.pool - i) * theta
                        #print '\t\tposition = %i, theta = %.3f, combination = %s, score = %.3f [%s]' % (
                        #    position,
                        #    theta,
                        #    combination,
                        #    score,
                        #    e
                        #)
                        rank[combination] += score

                #print '\t# Final rank'
                #print '\t%s' % rank
                combinations = [item[0] for item in sorted(rank.items(), key=operator.itemgetter(1), reverse = True)]

            combinations = combinations[0:self.limit]

        #print '# Final combinations'
        #print combinations
        return combinations

    def learn(self):
        #print 'Learning ECE'
        self.dataset.clearSupports()
        self.exposers = []
        for combination in self.combinations:
            e = Exposer(
                dataset = self.dataset,
                chosenLambda = combination,
                scales = self.scales,
                votingMethod = self.exposerVotingMethod,
                grain = self.grain,
                radius = self.radius,
                resample = self.resample
            )
            #print e
            #exposerConfiguration = {'chosenLambda': chosen_lambda}
            #exposerConfiguration.update(self.configuration)
            #exposer = Exposer(self.dataset, exposerConfiguration, self.scales)
            e.learn()
            self.exposers.append(e)
        #print self.exposers

    # ### Prediction
    # Prediction in this case is just creating and configuring exposer for
    # every combination from a list and performing the prediction for every
    # member.
    def predict(self):
        self.dataset.clearSupports()
        for exposer in self.exposers:
            exposer.predict()

    def generatePNGs(self, prefix='exposer_'):
        i = 0
        for exposer in self.exposers:
            i += 1
            foo = '_'.join(map(str, exposer.chosenLambda))
            exposer.png('%s%02i_%s.png' % (prefix, i, foo))
