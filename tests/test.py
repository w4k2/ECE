from eec import *

def test_dataset():
	# "Properly loading dataset"
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
