#!/usr/local/bin/gnuplot
reset

load '_gnuconfigs/experiment_6.cfg'

file = 'results/experiment_6.csv'

set output 'plots/experiment_6.png'

plot  	file 	u ($1):(100*$4) w l ls 2 t '3D', \
		'' 		u ($1):(100*$2) w l ls 1 t '2D'
