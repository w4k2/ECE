from ece import *
from numpy import *

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
    print dataset
    assert len(dataset.samples) == 50

def test_exposer():
    """Do exposer classify?"""
    dataset = Dataset('data/iris.csv','iris')
    dataset.setCV(0)

    configuration = {
        'radius': .25, 
        'grain': 50,
        'exposerParticipation': ExposerParticipation.lone,
        'chosenLambda': [2, 3]
    }
    exposer = Exposer(dataset, configuration)
    dataset.clearSupports()
    exposer.predict()
    scores = dataset.score()

    print "\n\tACC = %.3f" % scores['accuracy']
    assert isnan(scores['accuracy']) == False


def test_ensemble():
    """Do ensemble classify?"""
    dataset = Dataset('data/iris.csv','iris')
    print "\n"

    participations = [ExposerParticipation.lone, ExposerParticipation.theta1, ExposerParticipation.theta2]
    for participation in participations:
        dataset.setCV(0)
        configuration = {
            'radius': .25, 
            'grain': 50, 
            'limit': 3, 
            'dimensions': [2],
            'eecApproach': ECEApproach.random,
            'exposerParticipation': participation
        }
        ensemble = ECE(dataset,configuration)
    
        ensemble.predict()
        scores = dataset.score()
        
        print "\tACC = %.3f : %s" % ( scores['accuracy'], participation )
        assert isnan(scores['accuracy']) == False