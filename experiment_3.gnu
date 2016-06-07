#!/usr/local/bin/gnuplot
reset

load '_gnuconfigs/experiment_3.cfg'

file = 'results/experiment_3.csv'

set output 'plots/experiment_3.png'

plot  	file 	u ($1):(100*$4) w l ls 1 t 'Single pair', \
		'' 		u ($1):(100*$2) w l ls 2 t 'EEC'
