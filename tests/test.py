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
    print scores['accuracy']
    assert isnan(scores['accuracy']) == False