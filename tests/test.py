from ece import *
from numpy import *

def blue():
    return "\033[92m"

def endcolor():
    return '\033[0m'

def test_dataset():
    """Does dataset loads properly?"""
    dataset = Dataset('data/iris.csv','iris')

	# Amount of classes, samples and features
    assert dataset.classes == 3
    assert len(dataset.samples) == 150
    assert dataset.features == 4

    # Proper normalization
    for sample in dataset.samples:
    	for value in sample.features:
    		assert value >= 0 and value <= 1

    # Proper resampling
    dataset = Dataset('data/iris.csv','iris', 50)
    print "%s%s%s" % (blue(), dataset, endcolor())
    assert len(dataset.samples) == 50

def test_exposer():
    """Do exposer classify?"""
    dataset = Dataset('data/wine.csv','wine')
    dataset.setCV(0)

    configuration = {
        'radius': .25, 
        'grain': 20,
        'exposerVotingMethod': ExposerVotingMethod.lone,
        'chosenLambda': [2, 4]
    }
    exposer = Exposer(dataset, configuration)
    dataset.clearSupports()
    exposer.predict()
    scores = dataset.score()

    print  "\n\t%sACC = %.3f%s" % (blue(), scores['accuracy'], endcolor())
    assert isnan(scores['accuracy']) == False


def test_ensemble():
    """How do ensemble classify according to participations?"""
    dataset = Dataset('data/wine.csv','wine')
    print "\n"

    votingMethods = [ExposerVotingMethod.lone, ExposerVotingMethod.theta1, ExposerVotingMethod.theta2, ExposerVotingMethod.theta3, ExposerVotingMethod.thetas]
    for fold in xrange(0,5):
        print "Fold %i" % fold
        for votingMethod in votingMethods:
            dataset.setCV(fold)
            configuration = {
                'radius': 1, 
                'grain': 3, 
                'limit': 20, 
                'dimensions': [2],
                'eceApproach': ECEApproach.random,
                'exposerVotingMethod': votingMethod
            }
            ensemble = ECE(dataset,configuration)
        
            ensemble.predict()
            scores = dataset.score()
            
            print  "\t%sACC = %.3f : %s%s" % (blue(), scores['accuracy'], votingMethod, endcolor())
            assert isnan(scores['accuracy']) == False