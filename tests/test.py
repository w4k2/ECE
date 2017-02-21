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
    dataset = Dataset('data/wine.csv')
    dataset.setCV(0)

    configuration = {
        'radius': .25,
        'grain': 20,
        'chosenLambda': [2, 4]
    }
    exposer = Exposer(dataset, configuration)
    exposer.learn()
    dataset.clearSupports()
    exposer.predict()
    scores = dataset.score()

    print "\n\t%sACC = %.3f%s" % (blue(), scores['accuracy'], endcolor())
    assert np.isnan(scores['accuracy']) == False


def test_scaled_exposer():
    """Do exposer classify using scales?"""
    dataset = Dataset('data/wine.csv')
    dataset.setCV(0)

    configuration = {
        'radius': .25,
        'grain': 20,
        'chosenLambda': [2, 4]
    }
    scales = [.5,.5,1]
    exposer = Exposer(dataset, configuration, scales)
    exposer.learn()
    dataset.clearSupports()
    exposer.predict()
    scores = dataset.score()

    print "\n\t%sACC = %.3f%s" % (blue(), scores['accuracy'], endcolor())
    assert np.isnan(scores['accuracy']) == False
    # .662


def test_missing_exposer():
    """Do exposer classify missing values?"""
    dataset = Dataset('data/hyper.csv')
    dataset.setCV(0)

    configuration = {
        'radius': .25,
        'grain': 20,
        'chosenLambda': [2, 5]
    }
    exposer = Exposer(dataset, configuration)
    exposer.learn()
    dataset.clearSupports()
    exposer.predict()
    scores = dataset.score()

    print  "\n\t%sACC = %.3f%s" % (blue(), scores['accuracy'], endcolor())
    assert np.isnan(scores['accuracy']) == False

def test_ensemble():
    """How do ensemble classify according to participations?"""
    dataset = Dataset('data/wine.csv')
    print "\n"

    votingMethods = [ExposerVotingMethod.lone, ExposerVotingMethod.theta1, ExposerVotingMethod.theta2, ExposerVotingMethod.theta3, ExposerVotingMethod.thetas]
    for fold in xrange(0,1):
        print "Fold %i" % fold
        for votingMethod in votingMethods:
            dataset.setCV(fold)
            configuration = {
                'radius': .2,
                'grain': 10,
                'limit': 20,
                'pool': 40,
                'dimensions': [2],
                'eceApproach': ECEApproach.heuristic,
                'exposerVotingMethod': votingMethod
            }
            ensemble = ECE(dataset,configuration)
            ensemble.learn()
            dataset.clearSupports()

            ensemble.predict()
            scores = dataset.score()

            print  "\t%sACC = %.3f%s" % (blue(), scores['accuracy'], endcolor())
            assert np.isnan(scores['accuracy']) == False

def test_missing_ensemble():
    """How do ensemble classify missing-values data according to participations?"""
    dataset = Dataset('data/hyper.csv')
    print "\n"

    votingMethods = [ExposerVotingMethod.thetas]
    for fold in xrange(0,1):
        print "Fold %i" % fold
        for votingMethod in votingMethods:
            dataset.setCV(fold)
            configuration = {
                'radius': .2,
                'grain': 10,
                'limit': 10,
                'pool': 20,
                'dimensions': [2],
                'eceApproach': ECEApproach.heuristic,
                'exposerVotingMethod': votingMethod
            }
            ensemble = ECE(dataset,configuration)
            ensemble.learn()
            dataset.clearSupports()

            ensemble.predict()
            scores = dataset.score()

            print  "\t%sACC = %.3f%s" % (blue(), scores['accuracy'], endcolor())
            assert np.isnan(scores['accuracy']) == False
