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

### Experiment 1

	dataset: iris
	grain: 50
	one exponer ([2,3])

	testing radiuses in 1:99
	
![image](plots/experiment_1.png)