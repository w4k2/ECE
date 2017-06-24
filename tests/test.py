from weles import Dataset

from ece import Exposer
from ece import ECE

from ece import ExposerVotingMethod
from ece import ECEApproach

import numpy as np

def blue():
    return "\033[92m"

def endcolor():
    return '\033[0m'

def test_exposer():
    """Do exposer classify?"""
    dataset = Dataset('data/iris.csv')
    dataset.setCV(0)

    exposer = Exposer(dataset, chosenLambda = [0,2])
    exposer.learn()
    dataset.clearSupports()
    exposer.predict()
    scores = dataset.score()

    print "\n\t%sACC = %.3f%s" % (blue(), scores['accuracy'], endcolor())
    assert np.isnan(scores['accuracy']) == False

def test_ensemble():
    """How do ensemble classify according to participations?"""
    dataset = Dataset('data/iris.csv')
    print "\n"

    votingMethods = [ExposerVotingMethod.lone, ExposerVotingMethod.theta1, ExposerVotingMethod.theta2, ExposerVotingMethod.theta3, ExposerVotingMethod.thetas]
    for fold in xrange(0,1):
        print "Fold %i" % fold
        for votingMethod in votingMethods:
            dataset.setCV(fold)
            ensemble = ECE(dataset, votingMethod = votingMethod, resample = 250)
            ensemble.learn()
            dataset.clearSupports()

            ensemble.predict()
            scores = dataset.score()

            print  "\t%sBAC = %.3f%s" % (blue(), scores['bac'], endcolor())
            assert np.isnan(scores['accuracy']) == False
