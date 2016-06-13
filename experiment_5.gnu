#!/usr/local/bin/gnuplot
reset

load '_gnuconfigs/experiment_5.cfg'

file = 'results/experiment_5.csv'

set output 'plots/experiment_5.png'

plot  	file 	u ($1):(100*$2) w l ls 1 t 'Equal', \
		'' 		u ($1):(100*$3) w l ls 2 t 'Theta 1', \
		'' 		u ($1):(100*$4) w l ls 3 t 'Theta 2'