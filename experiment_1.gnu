#!/usr/local/bin/gnuplot
reset

load '_gnuconfigs/experiment_1.cfg'

file = 'results/experiment_1.csv'

set output 'plots/experiment_1.png'

plot  	file 	u ($1):(100*$2) w l ls 6 t 'Accuracy', \
		'' 		u ($1):(100*$5) w l ls 4 t 'Balanced accuracy'
