all:
	rm -f *.pyc
	./work.py

experiment_1:
	./experiment_1.py
	./experiment_1.gnu

experiment_2:
	./experiment_2.py
	./experiment_2.gnu

experiment_3:
	./experiment_3.py
	./experiment_3.gnu

experiment_4:
	./experiment_4.py
	./experiment_4.gnu

generator_1:
	./generator_1.py
	convert 	\( exponer_iris_1_1_g_350_r_100.png exponer_iris_1_2_g_350_r_100.png exponer_iris_1_3_g_350_r_100.png exponer_iris_1_4_g_350_r_100.png  +append \) \
				\( exponer_iris_2_1_g_350_r_100.png exponer_iris_2_2_g_350_r_100.png exponer_iris_2_3_g_350_r_100.png exponer_iris_2_4_g_350_r_100.png  +append \) \
				\( exponer_iris_3_1_g_350_r_100.png exponer_iris_3_2_g_350_r_100.png exponer_iris_3_3_g_350_r_100.png exponer_iris_3_4_g_350_r_100.png  +append \) \
				\( exponer_iris_4_1_g_350_r_100.png exponer_iris_4_2_g_350_r_100.png exponer_iris_4_3_g_350_r_100.png exponer_iris_4_4_g_350_r_100.png  +append \) \
				-background none -append   exponers_iris.png
	mkdir -f generator_1
	mv *.png generator_1/
