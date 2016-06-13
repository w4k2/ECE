# Exposer Ensemble Classifier

## Requirements

- pypng

## Conception

![image](generator_1/exponer_iris_2_1_g_350_r_100.png)
![image](generator_1/exponer_iris_3_4_g_350_r_100.png)
![image](generator_1/exponer_iris_2_3_g_350_r_100.png)

![image](generator_1/exponers_iris.png)

## Classification

Na oko klasy najmniej mieszaja sie w parze 3:4. Wiec sprobujmy uzyc tego cudu do klasyfikacji.

Najpierw zbadajmy radius.

#### Experiment 1

	dataset: iris
	grain: 50
	one exponer ([2,3])

	testing radiuses in 1:99
	
![image](plots/experiment_1.png)

#### Experiment 2

	dataset: iris
	radius: 30
	one exponer ([2,3])
	
	testing grains in 1:50

![image](plots/experiment_2.png)


## Ensemble of _exponers_

Zwyczajna akumulacja wsparć z wielu eksponerów.

#### Experiment 3
	
	dataset: iris
	grain: 20
	exponers: all possible combinations vs one exponer ([2,3])
	
	testing radiuses in 1:30

![image](plots/experiment_3.png)

## Naive approach to deal with the curse of dimensionality

#### Experiment 4

	dataset: heart
	grain: 10
	radius: 100
	
	testing random exponers limits from 1:30
	
![image](plots/experiment_4.png)

## Self-confidence measure

### One per exponer

### One per class in exponer

## Threedimensional _exponers_

## Joint model

Akumulujmy eksponery 2D i 3D.

## Heuristic approach to deal with the curse of dimensionality