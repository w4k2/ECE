# ECE [![Build Status](https://travis-ci.org/w4k2/ECE.svg?branch=master)](https://travis-ci.org/w4k2/ECE) [![Code Climate](https://codeclimate.com/github/w4k2/ECE/badges/gpa.svg)](https://codeclimate.com/github/w4k2/ECE)

**Exposer** is a data structure drawing from both <em>histogram</em> and a <em>scatter plot</em>. Like in <em>histogram</em>, the range of values is divided into a series of intervals, but like in a <em>scatter plot</em> the combination of features is analyzed. The rule of bin adjacency is here broken, so object may fall into more than one of them.

## Quick start

### Exposer

To create an _exposer_, all you need is to load a dataset, prepare dictionary with demanded configuration and use them to initiate object.

    dataset = Dataset('data/iris.csv','iris')
    configuration = {
        'radius': .5,
        'grain': 15,
        'chosenLambda': [2, 3]
    }
    exposer = Exposer(dataset, configuration)

For a process of classification, first is it required to clear supports for all samples in dataset. Later you can use _exposer_ to create predictions. Dictionary with scores is provided by a function `score()` being a member of `dataset` object.

    dataset.clearSupports()
    exposer.predict()
    scores = dataset.score()

### Ensemble of Exposers [ECE]

To create an ensemble, all you need is to load a dataset, prepare dictionary with demanded configuration and use them to initiate object.

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

For a process of classification you can simply use ensemble to create predictions. Dictionary with scores is provided by a function `score()` being a member of `dataset` object.

    ensemble.predict()
    scores = dataset.score()

## Models

### `ExposerVotingMethod`

- lone
- theta1
- theta2
- theta3
- thetas

### `ECEApproach`

- brutal
- random
- heuristic
